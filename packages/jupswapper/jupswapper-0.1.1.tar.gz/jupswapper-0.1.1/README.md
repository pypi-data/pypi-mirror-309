# jupswapper

A Python package for token swapping and wallet interactions on Solana using Jupiter Aggregator and Helius RPC endpoints.

## Key Features

- 🔄 High-level interface for token swaps
- 💰 Wallet balance checking with USD valuations
- 💸 SOL balance 
- 🛡️ Built-in retry mechanisms for robust transaction handling
- 📊 Automatic slippage protection from Jupiter Aggregator

## Prerequisites

- Python 3.12+
- Solana wallet with some SOL for transaction fees
- Helius API key (for RPC endpoints and transaction tracking)

## Installation

Install `jupswapper` using pip:
    
    pip install jupswapper

## Configuration

Set the following environment variables:

1. `SECRET_WORDS`: Your wallet's recovery phrase
2. `HELIUS_API_KEY`: Your Helius API key (https://helius.dev/)
3. `DERIVE_PATH`: Your wallet's derivation path (default: "m/44'/501'/0'")

We recommend using 1password-cli to inject these variables into your environment at runtime. 

    brew install 1password-cli

## Usage Examples
See `examples/` for the following scripts.

### Performing a Token Swap
```python
from jupswapper import Swap, SOL_MINT, BONK_MINT, try_swap

# Swap 0.01 SOL to BONK
swap = Swap(from_mint=SOL_MINT, to_mint=BONK_MINT, amount=0.01)
transaction_response = try_swap(swap)
print(transaction_response)
```

### Checking Wallet Balance
```python
from jupswapper import get_token_values_for_wallet, get_public_key_as_str, get_sol_balance

wallet_address = get_public_key_as_str()
token_values = get_token_values_for_wallet(wallet_address)

# Print token balances with USD values
for token in token_values:
    print(f"{token.symbol}: {token.amount_int} (${token.usd_value})")

# Get SOL balance
sol_balance = get_sol_balance(wallet_address)
print(f"SOL balance: {sol_balance}")
```

## Environment Variables

- `MAX_BPS`: Maximum basis points for slippage (default: 300)
- `MAX_RETRIES`: Maximum retry attempts for transactions (default: 5)
- `AWAIT_CONFIRMATION_MAX_RETRIES`: Maximum retries for transaction confirmation (default: 14)
- `AWAIT_CONFIRMATION_RETRY_DELAY`: Delay between confirmation retries (default: 2 seconds)


## Disclaimer
Use at your own risk. Always test with small amounts. 
