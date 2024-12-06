import requests
import json
import os
from typing import Union
from pydantic import BaseModel
from ..logger import logger

def get_transaction_url() -> str:
    HELIUS_API_KEY=os.getenv("HELIUS_API_KEY")
    assert HELIUS_API_KEY, "HELIUS_API_KEY is not set in the environment variables"
    return f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_API_KEY}"


class TransactionResponse(BaseModel):
    signature: str
    description: str
    fee: int
    transaction_error: str
    explorer_url: str

def build_transaction_response(data: dict) -> TransactionResponse:
    data = {
        "description": data["description"],
        "fee": int(data["fee"]),
        "transaction_error": json.dumps(data["transactionError"]),
        "signature": data["signature"],
        "explorer_url": f"https://solscan.io/tx/{data['signature']}",
    }
    return TransactionResponse(**data)


def get_transaction(txn_id: str) -> Union[TransactionResponse, None]:
    headers = {
        'Content-Type': 'application/json',
    }
    body = {
        'transactions': [txn_id],
    }
    
    response = requests.post(get_transaction_url(), headers=headers, data=json.dumps(body))
    data = response.json()
    if len(data) == 0:
        logger.info(f"Transaction not found on chain")
        return None
    data = data[0] # there is only one transaction in the response
    transaction_response = build_transaction_response(data)
    return transaction_response
