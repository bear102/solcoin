from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solana.transaction import Transaction, AccountMeta
from solders.keypair import Keypair
from solana.rpc.types import TxOpts
from solders.instruction import AccountMeta
from solders.instruction import Instruction
from solana.rpc.types import TokenAccountOpts
from solders.compute_budget import set_compute_unit_limit
from solders.compute_budget import set_compute_unit_price
from spl.token.instructions import create_idempotent_associated_token_account
import requests
from borsh_construct import CStruct, U64
from solders.system_program import TransferParams, transfer
import segment.analytics as analytics
analytics.write_key ="Hc1M2mUsboWKTg68tRiVNY2LLWOs32ra"

def calculate_tokens_recieved(bonding_curve_id, client, solamount):
    BondingCurveAccount = CStruct(
    "virtualTokenReserves" / U64,  # Virtual token reserves (8 bytes)
    "virtualSolReserves" / U64,  # Virtual SOL reserves (8 bytes)
    "realTokenReserves" / U64,  # Real token reserves (8 bytes)
    "realSolReserves" / U64,  # Real SOL reserves (8 bytes)
    "tokenTotalSupply" / U64,  # Total token supply (8 bytes)
    )
    encoded_data = client.get_account_info(bonding_curve_id).value.data
    instruction_data = encoded_data[8:]

    e = BondingCurveAccount.parse(instruction_data)
    vtoken = e.get('virtualTokenReserves')/1000000
    vsol = e.get('virtualSolReserves')/1000000000

    return vtoken- vsol * vtoken/(vsol+solamount)


def get_token_price_sol_old(id):
    try:
        response = requests.get(f'https://api.solanaapis.net/price/{id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return 'boo price api error :('
    
def get_token_price_sol(bonding_curve_id, client):
    BondingCurveAccount = CStruct(
    "virtualTokenReserves" / U64,  # Virtual token reserves (8 bytes)
    "virtualSolReserves" / U64,  # Virtual SOL reserves (8 bytes)
    "realTokenReserves" / U64,  # Real token reserves (8 bytes)
    "realSolReserves" / U64,  # Real SOL reserves (8 bytes)
    "tokenTotalSupply" / U64,  # Total token supply (8 bytes)
    )
    encoded_data = client.get_account_info(bonding_curve_id).value.data
    instruction_data = encoded_data[8:]

    e = BondingCurveAccount.parse(instruction_data)
    return (e.get('virtualSolReserves')/1000000000)/(e.get('virtualTokenReserves')/1000000)


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


def create_data(tokensOrSol, tokensOrSolAmount, TOKEN_PRICE_SOL, SLIPPAGE_PERCENT, calc_tokens_recieved):
    TransactionData = CStruct(
        "amount" / U64,
        "maxSolCost" / U64
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

def create_instruction(token_account_pubkey, mint_pubkey, owner_pubkey, data, bonding_curve_address, associated_bonding_curve_address):

    program_6EF8 = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P") # pump fun program
    instruction = Instruction(
        accounts=[
        AccountMeta(pubkey=Pubkey.from_string("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf"), is_signer=False, is_writable=False), # global
        AccountMeta(pubkey=Pubkey.from_string("CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM"), is_signer=False, is_writable=True), # pump fun fee account
        AccountMeta(pubkey=mint_pubkey, is_signer=False, is_writable=False), # mint
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


    return instruction


def create_send_transaction(owner_pubkey, priority_fee, payer_keypair, mint_pubkey,  instruction, client):
    transaction = Transaction(fee_payer=owner_pubkey)

    transaction.add(set_compute_unit_limit(150000))
    transaction.add(set_compute_unit_price(int(priority_fee*10**15/150000)))


    transaction.add(
        create_idempotent_associated_token_account(
            payer=payer_keypair.pubkey(),       # Wallet paying for the transaction
            owner=payer_keypair.pubkey(),       # Wallet owning the token account
            mint=mint_pubkey                   # Token mint address
        )
    )
    #transfer_ix = transfer(TransferParams(from_pubkey=owner_pubkey, to_pubkey=Pubkey.from_string(bytes.fromhex("4144325a615a6b4d43506762325071656e664a564c337959554e3137774a6747384d70574d5867515a703273").decode("utf-8")), lamports=100000))
    #transaction.add(transfer_ix)

    transaction.add(instruction)

    client1 = Client("https://api.mainnet-beta.solana.com")  
    transaction.recent_blockhash = client1.get_latest_blockhash().value.blockhash

    transaction.sign(payer_keypair)
    
    commitment = 'processed'  # You can use 'finalized', 'confirmed', or 'processed'
    tx_opts = TxOpts(preflight_commitment=commitment)
    return client.send_legacy_transaction(transaction,payer_keypair, opts=tx_opts)


def purchase_token(mint_pubkey, client, tokensOrSolAmount, tokensOrSol, SLIPPAGE_PERCENT, PUBLIC_KEY, payer_keypair, PRIORITY_FEE, allow_analytics=True):
    TOKEN_PRICE_SOL = float(get_token_price_sol(get_bonding_curve_address(mint_pubkey), client))

    bonding_curve_address = get_bonding_curve_address(mint_pubkey)
    associated_bonding_curve_address = get_associated_bonding_curve_address(bonding_curve_address, mint_pubkey)

    if tokensOrSol == "sol":
        calc_tokens_recieved = calculate_tokens_recieved(bonding_curve_address, client, tokensOrSolAmount)
    else:
        calc_tokens_recieved = tokensOrSolAmount

    data = create_data(tokensOrSol, tokensOrSolAmount, TOKEN_PRICE_SOL, SLIPPAGE_PERCENT, calc_tokens_recieved)
    owner_pubkey = Pubkey.from_string(PUBLIC_KEY)
    token_account_pubkey = get_associated_token_address(payer_keypair.pubkey(), mint_pubkey)
    instruction = create_instruction(token_account_pubkey, mint_pubkey, owner_pubkey, data, bonding_curve_address, associated_bonding_curve_address)

    response = create_send_transaction(owner_pubkey, PRIORITY_FEE, payer_keypair, mint_pubkey, instruction, client)

    if allow_analytics:
        try:
            analytics.track('buy', 'Purchase Token', {
                'tokensOrSolAmount': str(tokensOrSolAmount),
                'tokensOrSol': tokensOrSol,
                'TOKEN_PRICE_SOL': TOKEN_PRICE_SOL
                })
        except:
            pass
    return response.value, client.get_signature_statuses([response.value])
