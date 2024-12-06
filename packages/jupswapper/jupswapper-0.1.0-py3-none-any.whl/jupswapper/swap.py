import requests
import json
import os
import time
from solders.transaction import VersionedTransaction
import base64

from typing import Union
from .swap_model import Swap
from .logger import logger
from .key import get_keypair
from .quote import get_quote
from .sign import sign_transaction
from .await_confirmation import await_confirmation
from .send_transaction import send_transaction
from .helius import TransactionResponse

SWAP_URL = "https://quote-api.jup.ag/v6/swap"

HEADERS = {
    'Content-Type': 'application/json'
}

def get_max_bps() -> int:
    max_bps = int(os.getenv('MAX_BPS', 300))
    assert max_bps > 0, "MAX_BPS must be greater than 0"
    return max_bps

def get_max_retries() -> int:
    max_retries = int(os.getenv('MAX_RETRIES', 5))
    assert max_retries > 0, "MAX_RETRIES must be greater than 0"
    return max_retries

def get_swap_transaction_from_quote(quote: dict) -> dict:
    keypair = get_keypair()
    max_bps = get_max_bps()

    params = {
        'quoteResponse': quote,
        'userPublicKey': str(keypair.pubkey()),
        'dynamicComputeUnitLimit': True,
        'prioritizationFeeLamports': "auto",
        'dynamicSlippage': { "maxBps": max_bps }, 
    }
    response = requests.post(SWAP_URL, headers=HEADERS, data=json.dumps(params))
    if response.status_code != 200:
        logger.error(f"Request failed with status code {response.status_code}")
        raise ValueError(f"Request failed with status code {response.status_code}")
    
    return response.json()

def get_swap_transaction_str_from_quote(quote: dict) -> str:
    transaction = get_swap_transaction_from_quote(quote)
    return transaction["swapTransaction"]

def to_versioned_transaction(transaction_str: str) -> VersionedTransaction:
    swap_transaction_buf = base64.b64decode(transaction_str)
    transaction = VersionedTransaction.from_bytes(swap_transaction_buf)
    return transaction

def get_swap_versioned_transaction_from_quote(quote: dict) -> VersionedTransaction:
    transaction_str = get_swap_transaction_str_from_quote(quote)
    return to_versioned_transaction(transaction_str)

def make_swap(swap: Swap) -> TransactionResponse:
    logger.info(f"Making swap: {swap}")
    quote = get_quote(swap)
    transaction = get_swap_versioned_transaction_from_quote(quote)
    signed_transaction = sign_transaction(transaction)
    signature = send_transaction(signed_transaction)
    transaction_response = await_confirmation(signature)
    return transaction_response


def try_swap(swap: Swap) -> Union[TransactionResponse, None]:
    max_retries = get_max_retries()
    retry_count = 0 
    while retry_count < max_retries:
        try:
            return make_swap(swap)
        except Exception as e:
            logger.error(f"Error making swap: {e}")
        retry_count += 1
        time.sleep(2)
    logger.error(f"Failed to make swap after {max_retries} retries")
    return None
