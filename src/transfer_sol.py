from solana.rpc.api import Client
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import segment.analytics as analytics
analytics.write_key ="Hc1M2mUsboWKTg68tRiVNY2LLWOs32ra"

def make_transfer(client, private_key_base58_string, receiver_public_key_string, sol_amount, allow_analytics=True):

    sender = Keypair.from_base58_string(private_key_base58_string)

    receiver_public_key = Pubkey.from_string(receiver_public_key_string) 

    transfer_ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=receiver_public_key, lamports=int(sol_amount* 10**9)))


    transaction = Transaction()
    transaction.add(transfer_ix)

    client1 = Client("https://api.mainnet-beta.solana.com")  
    recent_blockhash = client1.get_latest_blockhash().value.blockhash


    transaction.recent_blockhash = recent_blockhash

    transaction.sign(sender)

    serialized_tx = transaction.serialize()

    resp = client.send_raw_transaction(serialized_tx), int(sol_amount* 10**9)

    if allow_analytics:
        try:
            analytics.track('transfer', 'Transfer Sol', {
                'sol_amount': str(sol_amount),
                })
        except:
            pass
    return resp

