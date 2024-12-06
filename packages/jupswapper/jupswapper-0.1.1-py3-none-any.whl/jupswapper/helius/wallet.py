import requests
from typing import List
from pydantic import BaseModel
from ..logger import logger
from .endpoint import get_rpc_endpoint

class TokenValue(BaseModel):
    mint: str
    symbol: str
    amount_int: int
    usd_value: float

def extract_token_values(data: dict) -> List[TokenValue]:
    if not data or 'result' not in data:
        return []
    
    readable_data = []
    for item in data['result'].get('items', []):
        mint = item.get('id')
        token_info = item.get('token_info', {})
        symbol = token_info.get('symbol', 'Unknown')
        price_info = token_info.get('price_info', {})
        usd_value = price_info.get('total_price', 0)
        amount_int = token_info.get('balance', 0)
        if usd_value > 0.0001: # filter out dust 
            readable_data.append(TokenValue(mint=mint, symbol=symbol, usd_value=usd_value, amount_int=amount_int))
    
    return readable_data

def get_token_values_for_wallet(wallet_address: str) -> List[TokenValue]:
    url = get_rpc_endpoint()
    
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "getAssetsByOwner",
        "params": {
            "ownerAddress": wallet_address,
            "page": 1,
            "limit": 1000,
            "displayOptions": {
                "showFungible": True
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        result = response.json()
        token_values = extract_token_values(result)
        return token_values
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching wallet assets: {e}")
        return []   
    