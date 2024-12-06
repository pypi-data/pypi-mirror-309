import os

def get_rpc_endpoint() -> str:
    HELIUS_API_KEY=os.getenv("HELIUS_API_KEY")
    assert HELIUS_API_KEY, "HELIUS_API_KEY is not set in the environment variables"
    return f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
