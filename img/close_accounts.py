from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.transaction import Transaction, AccountMeta
from solders.keypair import Keypair
from solana.rpc.types import TxOpts, TokenAccountOpts
from solders.instruction import AccountMeta
from solders.instruction import Instruction
from solana.rpc.types import TokenAccountOpts
from solders.compute_budget import set_compute_unit_limit
from solders.compute_budget import set_compute_unit_price
from borsh_construct import CStruct, U64
from spl.token.client import Token
from spl.token.instructions import close_account, CloseAccountParams

# Function to find token accounts owned by the wallet
def get_owned_token_accounts(wallet_pubkey, client):
    tx_opts = TokenAccountOpts(program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"))
    response = client.get_token_accounts_by_owner_json_parsed(wallet_pubkey, tx_opts)
    return response.value    

def close_all_empty_token_accounts(PRIORITY_FEE, wallet_pubkey_string, private_key_base58_string, client):
    payer_keypair = Keypair.from_base58_string(private_key_base58_string)

    wallet_pubkey = Pubkey.from_string(wallet_pubkey_string)

    transaction = Transaction(fee_payer=Pubkey.from_string(wallet_pubkey_string))
    transaction.add(set_compute_unit_limit(150000))
    transaction.add(set_compute_unit_price(int(PRIORITY_FEE*10**15/150000)))

    token_accounts = get_owned_token_accounts(wallet_pubkey, client)

    for account in token_accounts[:2]:
        if account.account.data.parsed['info']['tokenAmount']['amount'] == '0':
            close_account_instruction = close_account(
                CloseAccountParams(
                    program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                    account=account.pubkey,
                    dest=wallet_pubkey,
                    owner=wallet_pubkey
                )
            )
            transaction.add(close_account_instruction)
            
    client1 = Client("https://api.mainnet-beta.solana.com")  
    transaction.recent_blockhash = client1.get_latest_blockhash().value.blockhash

    transaction.sign(payer_keypair)

    commitment = 'processed'  # You can use 'finalized', 'confirmed', or 'processed'
    tx_opts = TxOpts(preflight_commitment=commitment)
    return client.send_legacy_transaction(transaction,payer_keypair, opts=tx_opts)