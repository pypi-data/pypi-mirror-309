from jupswapper import Swap, SOL_MINT, BONK_MINT, try_swap

swap = Swap(from_mint=SOL_MINT, to_mint=BONK_MINT, amount=0.01)
transaction_response = try_swap(swap)
print(transaction_response)