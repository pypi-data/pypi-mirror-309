from jupswapper import get_token_values_for_wallet, get_public_key_as_str, get_sol_balance
from pprint import pprint

wallet_address = get_public_key_as_str()
token_values = get_token_values_for_wallet(wallet_address)
pprint(token_values)

total_usd_value = sum(token_value.usd_value for token_value in token_values)
print(f"Total USD value: {total_usd_value}")

sol_balance = get_sol_balance(wallet_address)
print(f"SOL balance: {sol_balance}")
