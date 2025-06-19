from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.transaction import AccountMeta
from solders.keypair import Keypair
from solana.rpc.types import TxOpts
from solders.instruction import AccountMeta
from solders.instruction import Instruction
from solders.compute_budget import set_compute_unit_limit
from solders.compute_budget import set_compute_unit_price
from spl.token.instructions import create_idempotent_associated_token_account
import requests
from solders.keypair import Keypair
from borsh_construct import CStruct, U64, String
from solders.transaction import Transaction
import segment.analytics as analytics
analytics.write_key ="JEzNQ2jLInUIivS0PhIJCQRiuIzBXZZk"


def calculate_tokens_recieved(bonding_curve_id, client, solamount):
    vtoken = 1073000000
    vsol = 30
    print(vtoken)
    print(vsol)

    return vtoken- vsol * vtoken/(vsol+solamount)



def create_upload_metadata(form_data, photopath, mint_pubkey):
    with open(photopath, 'rb') as f:
        file_content = f.read()

    files = {
        'file': ('trglx2Owns.png', file_content, 'image/png')
    }

    metadata_response = requests.post("https://pump.fun/api/ipfs", data=form_data, files=files)
    metadata_response_json = metadata_response.json()

    return {
        'name': form_data['name'],
        'symbol': form_data['symbol'],
        'uri': metadata_response_json['metadataUri'],
        'mint': str(mint_pubkey)
    }


def find_program_address(seeds, program_id):
    """Find a valid program address."""
    return Pubkey.find_program_address(seeds, program_id)

def get_bonding_curve_address(mint_address):
    """Calculate the bonding curve address."""
    seeds = [b"bonding-curve", bytes(mint_address)]
    bonding_curve, _ = find_program_address(seeds, Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"))
    return bonding_curve

def get_associated_bonding_curve_address(bonding_curve_address, mint_address):
    """Calculate the associated bonding curve address."""
    seeds = [
        bytes(bonding_curve_address),
        bytes(Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")),
        bytes(mint_address)
    ]
    associated_bonding_curve, _ = find_program_address(seeds, Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"))
    return associated_bonding_curve

def get_associated_token_address(owner, mint):
    """Get the associated token address for a wallet and a token mint."""
    return Pubkey.find_program_address(
        [bytes(owner), bytes(Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")), bytes(mint)],
        Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
    )[0]

def create_data_instruction3create(token_metadata):
    TransactionData = CStruct(
        "name" / String,      
        "symbol" / String,
        "uri" / String ,
        "mint" / String
    )

    return b'\x18\x1e\xc8(\x05\x1c\x07w' + TransactionData.build(token_metadata) + b'\xa1\x10\xec\xcc\xd0\xe4\xe0\x929\xe9{\xa7#\x86\x8a\xe6\x0bO\x9d\n\xa6\xac\xa1\xaczv\xf8\xcbrZ\x18\x12'


def get_metadata_account(mint_address):
    return Pubkey.find_program_address(
        [bytes("metadata", "utf-8"), bytes(Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")), bytes(mint_address)],
        Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
    )[0]


def create_instruction3create(mint_pubkey, bonding_curve_address, associated_bonding_curve_address, metadata_account, owner_pubkey, data):
    return Instruction (
        accounts=[
        AccountMeta(pubkey=mint_pubkey, is_signer=True, is_writable=True), # mint
        AccountMeta(pubkey=Pubkey.from_string("TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"), is_signer=False, is_writable=False), # mint authority
        AccountMeta(pubkey=bonding_curve_address, is_signer=False, is_writable=True), # bonding curve
        AccountMeta(pubkey=associated_bonding_curve_address, is_signer=False, is_writable=True), # associated bonding curve
        AccountMeta(pubkey=Pubkey.from_string("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf"), is_signer=False, is_writable=False), # global
        AccountMeta(pubkey=Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"), is_signer=False, is_writable=False), # metadata
        AccountMeta(pubkey=metadata_account, is_signer=False, is_writable=True), # metadata account
        AccountMeta(pubkey=owner_pubkey, is_signer=True, is_writable=True), # user
        AccountMeta(pubkey=Pubkey.from_string("11111111111111111111111111111111"), is_signer=False, is_writable=False), # system 
        AccountMeta(pubkey=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"), is_signer=False, is_writable=False), # token program
        AccountMeta(pubkey=Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"), is_signer=False, is_writable=False), # atoken program
        AccountMeta(pubkey=Pubkey.from_string("SysvarRent111111111111111111111111111111111"), is_signer=False, is_writable=False), # rent
        AccountMeta(pubkey=Pubkey.from_string("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1"), is_signer=False, is_writable=False), # event authority
        AccountMeta(pubkey=Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"), is_signer=False, is_writable=False), # pump fun


    ],
        program_id=Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"),
        data=data
    )


def create_instruction4CreateIdempotent(mint_pubkey, owner_pubkey):
    return create_idempotent_associated_token_account(
        payer=owner_pubkey,       # Wallet paying for the transaction
        owner=owner_pubkey,       # Wallet owning the token account
        mint=mint_pubkey            # Token mint address
    )

def create_data_instruction5buy(tokensOrSol, tokensOrSolAmount, TOKEN_PRICE_SOL, SLIPPAGE_PERCENT, calc_tokens_recieved):
    TransactionData = CStruct(
        "amount" / U64,       # Unsigned 64-bit integer (u64) for amount
        "maxSolCost" / U64  # Unsigned 64-bit integer (u64) for minSolOutput
    )

    #tokens
    if tokensOrSol == 'sol':
        tokens = calc_tokens_recieved
        if tokens>1:
            tokens = int(tokens)
    else:
        tokens = tokensOrSolAmount
    calctokens = tokens*10**6

    #slippage
    # min sol output is in lamparts
    if tokensOrSol == 'sol':
        maxSolCost = (SLIPPAGE_PERCENT/100+1)*tokensOrSolAmount
    else:
        maxSolCost = (SLIPPAGE_PERCENT/100+1)*tokensOrSolAmount * TOKEN_PRICE_SOL

    maxSolCost = int(maxSolCost*1000000000)

    encoded_data = TransactionData.build({
        "amount": calctokens,
        "maxSolCost": maxSolCost,
    })

    return b'f\x06=\x12\x01\xda\xeb\xea' + encoded_data

def create_instruction5buy(token_account_pubkey, mint_pubkey, owner_pubkey, data):
    bonding_curve_address = get_bonding_curve_address(mint_pubkey)
    associated_bonding_curve_address = get_associated_bonding_curve_address(bonding_curve_address, mint_pubkey)

    program_6EF8 = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")

    return Instruction (
        accounts=[
        AccountMeta(pubkey=Pubkey.from_string("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf"), is_signer=False, is_writable=False), # global
        AccountMeta(pubkey=Pubkey.from_string("CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM"), is_signer=False, is_writable=True), # pump fun fee account
        AccountMeta(pubkey=mint_pubkey, is_signer=True, is_writable=True), # mint
        AccountMeta(pubkey=bonding_curve_address, is_signer=False, is_writable=True), # pump fun bonding curve
        AccountMeta(pubkey=associated_bonding_curve_address, is_signer=False, is_writable=True), # pump fun vault
        AccountMeta(pubkey=token_account_pubkey, is_signer=False, is_writable=True), # token account
        AccountMeta(pubkey=owner_pubkey, is_signer=True, is_writable=True),  # owner wallet
        AccountMeta(pubkey=Pubkey.from_string("11111111111111111111111111111111"), is_signer=False, is_writable=False), # sys program
        AccountMeta(pubkey=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"), is_signer=False, is_writable=False), # token program
        AccountMeta(pubkey=Pubkey.from_string("SysvarRent111111111111111111111111111111111"), is_signer=False, is_writable=False), # rent
        AccountMeta(pubkey=Pubkey.from_string("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1"), is_signer=False, is_writable=False), # event authority
        AccountMeta(pubkey=program_6EF8, is_signer=False, is_writable=False),
    ],
        program_id=program_6EF8,
        data=data
    )


def create_send_transaction(owner_pubkey, priority_fee, payer_keypair, mint_keypair,  instruction3create, instruction4CreateIdempotent, instruction5buy, client):
    culimit = set_compute_unit_limit(220000)
    cuprice = set_compute_unit_price(int(priority_fee*10**15/220000))

    client1 = Client("https://api.mainnet-beta.solana.com")  
    recent_blockhash = client1.get_latest_blockhash().value.blockhash

    tx = Transaction.new_signed_with_payer(
        [culimit, cuprice, instruction3create, instruction4CreateIdempotent, instruction5buy],
        owner_pubkey,
        [payer_keypair, mint_keypair],
        recent_blockhash  # Pass the recent blockhash here
    )

    commitment = 'processed'  # You can use 'finalized', 'confirmed', or 'processed'
    tx_opts = TxOpts(preflight_commitment=commitment)
    return client.send_transaction(tx, opts=tx_opts)

def create_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE, form_data, photopath, mint_keypair, allow_analytics=True):
    bonding_curve_address = get_bonding_curve_address(mint_pubkey)
    associated_bonding_curve_address = get_associated_bonding_curve_address(bonding_curve_address, mint_pubkey)
    metadata_account = get_metadata_account(mint_pubkey)



    owner_pubkey = Pubkey.from_string(PUBLIC_KEY)
    token_metadata = create_upload_metadata(form_data, photopath, mint_pubkey)
    data = create_data_instruction3create(token_metadata)
    instruction3create = create_instruction3create(mint_pubkey, bonding_curve_address, associated_bonding_curve_address, metadata_account, owner_pubkey, data)


    instruction4CreateIdempotent = create_instruction4CreateIdempotent(mint_pubkey, owner_pubkey)


    if tokensOrSol == "sol":
        calc_tokens_recieved = calculate_tokens_recieved(bonding_curve_address, client, tokensOrSolAmount)
    else:
        calc_tokens_recieved = tokensOrSolAmount

    data = create_data_instruction5buy(tokensOrSol, tokensOrSolAmount, .00000002796, SLIPPAGE_PERCENT, calc_tokens_recieved)
    token_account_pubkey = get_associated_token_address(payer_keypair.pubkey(), mint_pubkey)
    instruction5buy = create_instruction5buy(token_account_pubkey, mint_pubkey, owner_pubkey, data)


    response = create_send_transaction(owner_pubkey, PRIORITY_FEE, payer_keypair, mint_keypair,  instruction3create, instruction4CreateIdempotent, instruction5buy, client)
    if allow_analytics:
        try:
            analytics.track('create', 'Create Token', {
                'tokensOrSolAmount': str(tokensOrSolAmount),
                'tokensOrSol': tokensOrSol,
                'TOKEN_PRICE_SOL': .00000002796
                })
        except:
            pass
    return response.value, client.get_signature_statuses([response.value])
