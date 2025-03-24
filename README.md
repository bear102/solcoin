<p align="center">
  <img src="https://github.com/bear102/solcoin/blob/8d90f203f231d4e512a6663050719d362efdf1e2/img/solcoin.png" alt="Python Tennis Library" width="450">
</p>

Solcoin is a python package with many different solana token transaction
<br>
**Full Docs**: https://solcoin.gitbook.io/docs

## Features
***Main***
* Buy Tokens
* Sell Tokens
* Create Tokens
* Transfer SOL
* close accounts
* WebSocket RPC Listeners

Other
* find token bonding curve from mint
* find token prices from bonding curve
* create pumpfun transaction data

## Quickstart

> More explanation at https://solcoin.gitbook.io/docs/pumpfun-tokens

### Buy Tokens
```python
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.keypair import Keypair

from solcoin import buy_tokens

PUBLIC_KEY = "your_account_pubkey_string" # ex:G3tmXiWmgnhhjb4N12YK7QgmaqtRaCRaL6i4nx2ueKwr
TOKEN_MINT = "token_mint_string" # ex:6oDn2PDvjtKYoWVp9cNNe1WCepjS8VQzhBRS8qmXpump
mint_pubkey = Pubkey.from_string(TOKEN_MINT)
client = Client("your_RPC_url") # ex:https://api.mainnet-beta.solana.com

tokensOrSolAmount = .1 # how many tokens or sol you want to purchase
tokensOrSol = 'sol' # either 'token' or 'sol', whichever unit you want to buy in
SLIPPAGE_PERCENT = 20
PRIORITY_FEE = .000001 

private_key_base58 = "private_key_base58_string" # your base58 private key string
payer_keypair = Keypair.from_base58_string(private_key_base58)


sig, status = buy_coins.purchase_coin(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE)

print(sig) # prints the signature of the transaction
print(status) # prints the current status of the transaction
```

### Sell Tokens
```python
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.keypair import Keypair

from solcoin import sell_tokens

PUBLIC_KEY = "your_account_pubkey_string" # ex:G3tmXiWmgnhhjb4N12YK7QgmaqtRaCRaL6i4nx2ueKwr
TOKEN_MINT = "token_mint_string" # ex:6oDn2PDvjtKYoWVp9cNNe1WCepjS8VQzhBRS8qmXpump
mint_pubkey = Pubkey.from_string(TOKEN_MINT)
client = Client("your_RPC_url") # ex:https://api.mainnet-beta.solana.com

tokensOrSolAmount = 100 # how many tokens or sol or percent of coins you own you want to purchase
tokensOrSol = 'percent' # either 'token' or 'sol' or 'percent, whichever unit you want to buy in
SLIPPAGE_PERCENT = 20
PRIORITY_FEE = .000001 

private_key_base58 = "private_key_base58_string" # your base58 private key string
payer_keypair = Keypair.from_base58_string(private_key_base58)


sig, status = sell_coins.sell_coin(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE)


print(sig) # prints the signature of the transaction
print(status) # prints the current status of the transaction
```
### Create Tokens
```python
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.keypair import Keypair
from solcoin import create_tokens

PUBLIC_KEY = "your_account_pubkey_string" # ex:G3tmXiWmgnhhjb4N12YK7QgmaqtRaCRaL6i4nx2ueKwr
SLIPPAGE_PERCENT = 20
PRIORITY_FEE = .00001
tokensOrSolAmount = .1 # how much you want to buy (initial dev buy)
tokensOrSol = 'sol' # 'token' or 'sol'
client = Client("your_RPC_url") # ex:https://api.mainnet-beta.solana.com

# generates a random mint keypair
mint_keypair = Keypair()
mint_pubkey = mint_keypair.pubkey()
# the token mint's pubkey
print(mint_pubkey)

private_key_base58 = "private_key_base58_string" # your base58 private key string
payer_keypair = Keypair.from_base58_string(private_key_base58)

# metadata about your new token
form_data = {
    'name': "token name",
    'symbol': "tokenSymbol",
    'description': "description of token",
    'twitter': 'https://google.com',
    'telegram': 'https://google.com',
    'website': 'https://google.com',
    'showName': 'true'
}
photopath = r"path\to\cover\photo\example.png"

sig, status = create_tokens.create_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE, form_data, photopath, mint_keypair)

print(sig)
print(status)
```
## Fees
0.0001 sol/tx fee on buying and selling tokens
[Fee Table](https://app.gitbook.com/o/8xxOO6VLhA1jpAKdlogo/s/TdmaylEM2A8iOQ6ExecB/~/changes/4/info/fees)

## Security
- Private keys **never leave your computer** unlike a lot of the competition

- All transactions created, signed, and sent locally

- Fully open source and transparent code at https://github.com/bear102/solcoin
