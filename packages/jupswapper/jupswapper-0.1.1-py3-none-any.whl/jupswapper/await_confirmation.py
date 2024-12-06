import os
import time
from solders.signature import Signature

from .logger import logger
from .helius import get_transaction, TransactionResponse

def get_max_retries() -> int:
    max_retries = int(os.getenv('AWAIT_CONFIRMATION_MAX_RETRIES', 14))
    assert max_retries > 0, "AWAIT_CONFIRMATION_MAX_RETRIES must be greater than 0"
    return max_retries

def get_retry_delay() -> int:
    retry_delay = int(os.getenv('AWAIT_CONFIRMATION_RETRY_DELAY', 2))
    assert retry_delay > 0, "AWAIT_CONFIRMATION_RETRY_DELAY must be greater than 0"
    return retry_delay

def await_confirmation(signature: Signature) -> TransactionResponse:
    max_retries = get_max_retries()
    retry_delay = get_retry_delay()
    retries = 0
    time.sleep(retry_delay + 2)
    while retries < max_retries:
        try: 
            logger.info(f"Checking transaction, retry {retries}, signature: {signature}")
            
            transaction = get_transaction(str(signature))
            if transaction is not None:
                logger.info("Transaction confirmed on chain")
                return transaction
            else:
                logger.debug(transaction) 
        except Exception as e:
            logger.error(f"Error getting transaction: {e}")
        retries += 1
        time.sleep(retry_delay)
    raise ValueError(f"Transaction not confirmed after {max_retries} retries")
