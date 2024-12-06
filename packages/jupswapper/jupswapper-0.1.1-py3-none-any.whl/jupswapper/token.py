import requests
TOKEN_BY_MINT_URL = "https://tokens.jup.ag/token/"

# import requests_cache
# Create a session with caching
# session = requests_cache.CachedSession('demo_cache')
# response = session.get('https://httpbin.org/get')

def get_token_by_mint(mint: str) -> dict:
    url = TOKEN_BY_MINT_URL + mint
    response = requests.get(url)
    if response.status_code != 200:
        print(response.text)
        raise ValueError(f"Request failed with status code {response.status_code}")
    return response.json()

def get_decimals(mint: str) -> int:
    token_data = get_token_by_mint(mint)
    decimals = token_data.get('decimals', None)
    if decimals is None:
        raise ValueError(f"Decimals not found for mint {mint}")
    return decimals