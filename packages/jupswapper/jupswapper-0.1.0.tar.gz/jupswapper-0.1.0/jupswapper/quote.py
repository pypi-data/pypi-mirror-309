from .swap_model import Swap
from .token import get_decimals
import requests
from .logger import logger

QUOTE_URL = "https://quote-api.jup.ag/v6/quote"

def get_quote(swap: Swap) -> dict:
    if swap.amount_int is None:
        amount = swap.amount * 10 ** get_decimals(swap.from_mint)
        amount_int = int(amount)
    else:
        amount_int = swap.amount_int

    params = {
        'inputMint': swap.from_mint,
        'outputMint': swap.to_mint,
        'amount': str(amount_int),
        # 'slippageBps': str(50),
        # 'restrictIntermediateTokens': 'true',
    }
    response = requests.get(QUOTE_URL, params=params)
    if response.status_code != 200:
        logger.error(f"Request failed with status code {response.status_code}")
        raise ValueError(f"Request failed with status code {response.status_code}")
    return response.json()