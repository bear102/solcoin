for i in range(30):
    import time
    from datetime import datetime, timezone

    submission_time = datetime.now(timezone.utc)

    from solders.pubkey import Pubkey
    from solana.rpc.api import Client
    from solders.keypair import Keypair
    import solcoin
    from solcoin.buy_tokens import *
    from solcoin.buy_tokens import purchase_token


    PUBLIC_KEY = "<redacted>"
    TOKEN_MINT = "Ms7DewGxeSLRzGirwQbiXxrkRdyrdjtPTHRAtgE5bJy"
    mint_pubkey = Pubkey.from_string(TOKEN_MINT)
    client = Client("https://damp-attentive-diagram.solana-mainnet.quiknode.pro/a29c9dba4d5bf000ca1f4bf0140bd5e184ecdad5")  

    tokensOrSolAmount = .00001
    tokensOrSol = 'sol' # 'token' or 'sol'
    SLIPPAGE_PERCENT = 20
    PRIORITY_FEE = .00001

    private_key_base58 = "<redacted>"
    payer_keypair = Keypair.from_base58_string(private_key_base58)

    sig, status = purchase_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE)


    # Start polling
    start_poll = time.time()
    max_attempts = 30
    wait_interval = 0

    for attempt in range(max_attempts):
        status_resp = client.get_signature_statuses([sig])
        status = status_resp.value[0]

        if  status and status.confirmation_status :
            confirmation_time = datetime.now(timezone.utc)
            latency = (confirmation_time - submission_time).total_seconds()
            print(latency)
            break
        time.sleep(wait_interval)
    else:
        print("Transaction not confirmed within timeout.")

    time.sleep(2)