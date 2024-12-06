from .client import get_client
from solders.pubkey import Pubkey
from base58 import b58decode

def get_sol_balance(wallet_address: str) -> float:
    client = get_client()
    decoded_address = b58decode(wallet_address)
    key = Pubkey(decoded_address)
    response = client.get_balance(key) 
    return response.value / 1e9