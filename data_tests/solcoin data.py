for i in range(10):
    import time
    from datetime import datetime, timezone
    import random

    submission_time = datetime.now(timezone.utc)

    from solders.pubkey import Pubkey
    from solana.rpc.api import Client
    from solders.keypair import Keypair
    import solcoin
    from solcoin.sell_tokens import sell_token


    PUBLIC_KEY = "9Zq4U562Fc1HT7hE4H4m5iRDti2M15ZPrcrwZVTQraea"
    TOKEN_MINT = "Ms7DewGxeSLRzGirwQbiXxrkRdyrdjtPTHRAtgE5bJy"
    mint_pubkey = Pubkey.from_string(TOKEN_MINT)
    client = Client("<redacted - standard quicknode rpc on free plan")  

    tokensOrSolAmount = round(random.uniform(0.00001, 0.0001), 5)
    tokensOrSol = 'sol' # 'token' or 'sol'
    SLIPPAGE_PERCENT = 20
    PRIORITY_FEE = .00001

    private_key_base58 = "<redacted>"
    payer_keypair = Keypair.from_base58_string(private_key_base58)

    sig, status = sell_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE)


    # Start polling
    start_poll = time.time()
    max_attempts = 30
    wait_interval = 0  # in seconds

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

    time.sleep(600)
