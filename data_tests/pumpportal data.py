from solana.rpc.api import Client
client = Client("https://damp-attentive-diagram.solana-mainnet.quiknode.pro/a29c9dba4d5bf000ca1f4bf0140bd5e184ecdad5")  
from solders.signature import Signature

for i in range(10):
    import time
    from datetime import datetime, timezone

    submission_time = datetime.now(timezone.utc)
    import requests
    from solders.transaction import VersionedTransaction
    from solders.keypair import Keypair
    from solders.commitment_config import CommitmentLevel
    from solders.rpc.requests import SendVersionedTransaction
    from solders.rpc.config import RpcSendTransactionConfig

    response = requests.post(url="https://pumpportal.fun/api/trade-local", data={
        "publicKey": "<redacted>",
        "action": "buy",             # "buy" or "sell"
        "mint": "Ms7DewGxeSLRzGirwQbiXxrkRdyrdjtPTHRAtgE5bJy",     # contract address of the token you want to trade
        "amount": .00001,            # amount of SOL or tokens to trade
        "denominatedInSol": "true", # "true" if amount is amount of SOL, "false" if amount is number of tokens
        "slippage": 20,              # percent slippage allowed
        "priorityFee": 0.00001,        # amount to use as priority fee
        "pool": "pump"               # exchange to trade on. "pump", "raydium", "pump-amm" or "auto"
    })

    keypair = Keypair.from_base58_string("<redacted>")
    tx = VersionedTransaction(VersionedTransaction.from_bytes(response.content).message, [keypair])

    commitment = CommitmentLevel.Confirmed
    config = RpcSendTransactionConfig(preflight_commitment=commitment)
    txPayload = SendVersionedTransaction(tx, config)

    response = requests.post(
        url="https://damp-attentive-diagram.solana-mainnet.quiknode.pro/a29c9dba4d5bf000ca1f4bf0140bd5e184ecdad5",
        headers={"Content-Type": "application/json"},
        data=SendVersionedTransaction(tx, config).to_json()
    )
    txSignature = response.json()['result']


    # Start polling
    start_poll = time.time()
    max_attempts = 30
    wait_interval = 0

    for attempt in range(max_attempts):
        status_resp = client.get_signature_statuses([Signature.from_string(txSignature)])
        status = status_resp.value[0]

        if  status and status.confirmation_status :
            confirmation_time = datetime.now(timezone.utc)
            latency = (confirmation_time - submission_time).total_seconds()
            #print(f"Confirmed at: {confirmation_time.strftime('%H:%M:%S.%f')[:-3]}")
            print(latency)
            break
        time.sleep(wait_interval)
    else:
        print("Transaction not confirmed within timeout.")

    time.sleep(2)