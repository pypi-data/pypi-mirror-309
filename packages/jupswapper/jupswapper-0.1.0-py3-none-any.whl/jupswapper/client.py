from solana.rpc.api import Client
from .helius import get_rpc_endpoint

def get_client() -> Client:
    url = get_rpc_endpoint()
    return Client(url)

_client = None
def _get_client() -> Client:
    global _client
    if _client is None:
        _client = make_client()
    return _client
