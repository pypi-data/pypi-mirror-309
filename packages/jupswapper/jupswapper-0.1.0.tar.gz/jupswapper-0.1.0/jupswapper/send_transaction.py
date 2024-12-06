from solana.rpc.api import SendTransactionResp, SimulateTransactionResp
from solders.rpc.responses import RpcSimulateTransactionResult
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from .client import get_client

def send_transaction(transaction: VersionedTransaction) -> Signature:
    client = get_client()
    simulated_response: SimulateTransactionResp = client.simulate_transaction(transaction)
    result: RpcSimulateTransactionResult = simulated_response.value
    error = result.err
    if error is not None:
        raise ValueError(f"Transaction failed to simulate: {error}")
    response: SendTransactionResp = client.send_transaction(transaction)
    return response.value

