<p align="center">
  <img src="https://github.com/bear102/solcoin/blob/ad33e6a76674d24d95fd4a864a7afa15ee58127c/img/solcoin.png" alt="Python Tennis Library" width="450">
</p>

<p align="center">
  <a href="https://github.com/bear102/solcoin"><img src="https://img.shields.io/badge/GitHub-bear102-%2312100E.svg?style=flat&logo=github" alt="GitHub"></a>
  <img src="https://img.shields.io/badge/python-blue" alt="Python">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
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
​
import solcoin.buy_tokens as buy
​
PUBLIC_KEY = "your_account_pubkey_string" # ex:G3tmXiWmgnhhjb4N12YK7QgmaqtRaCRaL6i4nx2ueKwr
TOKEN_MINT = "token_mint_string" # ex:6oDn2PDvjtKYoWVp9cNNe1WCepjS8VQzhBRS8qmXpump
mint_pubkey = Pubkey.from_string(TOKEN_MINT)
client = Client("your_RPC_url") # ex:https://api.mainnet-beta.solana.com
​
tokensOrSolAmount = .1 # how many tokens or sol you want to purchase
tokensOrSol = 'sol' # either 'token' or 'sol', whichever unit you want to buy in
SLIPPAGE_PERCENT = 20
PRIORITY_FEE = .000001 
​
private_key_base58 = "private_key_base58_string" # your base58 private key string
payer_keypair = Keypair.from_base58_string(private_key_base58)
​
​
sig, status = buy.purchase_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE, allow_analytics=True)
​
print(sig) # prints the signature of the transaction
print(status) # prints the current status of the transaction
```

### Sell Tokens
```python
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.keypair import Keypair

import solcoin.sell_tokens as sell

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


sig, status = sell.sell_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE, allow_analytics=True)


print(sig) # prints the signature of the transaction
print(status) # prints the current status of the transaction
```
### Create Tokens
```python
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.keypair import Keypair
​
import solcoin.create_tokens as create
​
PUBLIC_KEY = "your_account_pubkey_string" # ex:G3tmXiWmgnhhjb4N12YK7QgmaqtRaCRaL6i4nx2ueKwr
SLIPPAGE_PERCENT = 20
PRIORITY_FEE = .00001
tokensOrSolAmount = .1 # how much you want to buy (initial dev buy)
tokensOrSol = 'sol' # 'token' or 'sol'
client = Client("your_RPC_url") # ex:https://api.mainnet-beta.solana.com
​
# generates a random mint keypair
mint_keypair = Keypair()
mint_pubkey = mint_keypair.pubkey()
# the token mint's pubkey
print(mint_pubkey)
​
private_key_base58 = "private_key_base58_string" # your base58 private key string
payer_keypair = Keypair.from_base58_string(private_key_base58)
​
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
​
sig, status = create.create_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE, form_data, photopath, mint_keypair, allow_analytics=True)
​
print(sig)
print(status)
```
## Fees
0 fees
[Fee Table](https://app.gitbook.com/o/8xxOO6VLhA1jpAKdlogo/s/TdmaylEM2A8iOQ6ExecB/~/changes/4/info/fees)

## Security
- Private keys **never leave your computer** unlike a lot of the competition

- All transactions created, signed, and sent locally

- Fully open source and transparent code at https://github.com/bear102/solcoin
