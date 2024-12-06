import struct
from solana.transaction import AccountMeta, Transaction
from spl.token.instructions import create_associated_token_account, get_associated_token_address, close_account, CloseAccountParams
from solders.instruction import Instruction #type: ignore
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price #type: ignore
from account_utils import get_payer_keypair
from constants import *
from isolated_rpcs import sendTransaction,get_token_balance,get_block_hash,confirm_txn
from abstract_solcatcher import *
from solana.rpc.types import TokenAccountOpts,TxOpts
from coin_data import get_pump_fun_data
from typing import Optional, Union
from abstract_solana import *
from abstract_database import *
from abstract_solana import Client,get_insert_list
from abstract_apis import postRequest,getRequest,postRpcRequest,get_async_response,postRequest

def start_txn(data,keys,owner,token_account_instructions):
    swap_instruction = Instruction(get_pubkey(PUMP_FUN_PROGRAM), bytes(data), keys)
    # Construct and sign transaction
    recent_blockhash = get_block_hash()
    txn = Transaction(recent_blockhash=recent_blockhash, fee_payer=owner)
    txn.add(set_compute_unit_price(UNIT_PRICE))
    txn.add(set_compute_unit_limit(UNIT_BUDGET))
    if token_account_instructions:
        txn.add(token_account_instructions)
    txn.add(swap_instruction)
    return txn
def get_coin_data(mint_str,coin_data,payer_keypair=None,fileName=None,envKey=None):
    
    payer_keypair = payer_keypair or get_payer_keypair(fileName=fileName,envKey=envKey)
    owner = payer_keypair.pubkey()
    mint = get_pubkey(mint_str)
    # Attempt to retrieve token account; if not, prepare to create it
    token_account = get_associated_token_address(owner, mint)
    
    account_data = call_solcatcher_db_api('get_token_accounts_by_owner', owner, TokenAccountOpts(mint))
    token_account_instructions = None
   
    if not account_data.get('value'):
        # If token account does not exist, create the associated token account
        print("Creating new associated token account...")
        token_account_instructions = create_associated_token_account(owner, owner, mint)
    return owner, owner, mint,token_account,token_account_instructions
def send_txn(txn,payer_keypair=None,fileName=None,envKey=None):
    payer_keypair = payer_keypair or get_payer_keypair(fileName=fileName,envKey=envKey)
    txn.sign(payer_keypair)
    # Send and confirm transaction
    txn_sig = sendTransaction(txn, payer_keypair, opts=TxOpts(skip_preflight=True))
    print("Transaction Signature", txn_sig)
    return txn_sig
def buy(mint_str: str, sol_in: float = 0.001, slippage: int = 25,payer_keypair=None,fileName=None,envKey=None) -> bool:
    try:
        # Get coin data
        coin_data = get_pump_fun_data(mint_str)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return False
        payer_keypair = payer_keypair or get_payer_keypair()
        owner = payer_keypair.pubkey()
        mint = Pubkey.from_string(mint_str)
        
        # Attempt to retrieve token account; if not, prepare to create it
        token_account = get_associated_token_address(owner, mint)
        account_data = rate_limit_solcatcher_api('get_token_accounts_by_owner', owner, TokenAccountOpts(mint))
        token_account_instructions = None

        if not account_data.get('value'):
            # If token account does not exist, create the associated token account
            print("Creating new associated token account...")
            token_account_instructions = create_associated_token_account(owner, owner, mint)

        # Calculate amount of tokens to buy
        virtual_sol_reserves = coin_data['virtual_sol_reserves']
        virtual_token_reserves = coin_data['virtual_token_reserves']
        sol_in_lamports = sol_in * LAMPORTS_PER_SOL
        amount = int(sol_in_lamports * virtual_token_reserves / virtual_sol_reserves)

        # Calculate max SOL cost with slippage
        max_sol_cost = int(sol_in * (1 + slippage / 100) * LAMPORTS_PER_SOL)
        print("Max SOL Cost:", max_sol_cost / LAMPORTS_PER_SOL)

        # Define account keys for the transaction
        keys = [
            AccountMeta(pubkey=get_pubkey(GLOBAL), is_signer=False, is_writable=False),
            AccountMeta(pubkey=get_pubkey(FEE_RECIPIENT), is_signer=False, is_writable=True),
            AccountMeta(pubkey=get_pubkey(coin_data['mint']), is_signer=False, is_writable=False),
            AccountMeta(pubkey=get_pubkey(coin_data['bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=get_pubkey(coin_data['associated_bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=get_pubkey(token_account), is_signer=False, is_writable=True),
            AccountMeta(pubkey=get_pubkey(owner), is_signer=True, is_writable=True),
            AccountMeta(pubkey=get_pubkey(SYSTEM_PROGRAM), is_signer=False, is_writable=False), 
            AccountMeta(pubkey=get_pubkey(ASSOC_TOKEN_ACC_PROG), is_signer=False, is_writable=False),
            AccountMeta(pubkey=get_pubkey(TOKEN_PROGRAM), is_signer=False, is_writable=False),
            AccountMeta(pubkey=get_pubkey(EVENT_AUTHORITY), is_signer=False, is_writable=False),
            AccountMeta(pubkey=get_pubkey(PUMP_FUN_PROGRAM), is_signer=False, is_writable=False)
        ]

        # Construct the swap instruction
        data = bytearray()
        data.extend(bytes.fromhex("66063d1201daebea"))  # Replace with actual instruction identifier
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', max_sol_cost))
        swap_instruction = Instruction(get_pubkey(PUMP_FUN_PROGRAM), bytes(data), keys)

        # Construct and sign transaction
        txn = Transaction(recent_blockhash=get_block_hash(), fee_payer=owner)
        txn.add(set_compute_unit_price(UNIT_PRICE))
        txn.add(set_compute_unit_limit(UNIT_BUDGET))
        if token_account_instructions:
            txn.add(token_account_instructions)
        txn.add(swap_instruction)

        # Sign and send transaction
        txn.sign(payer_keypair)
        txn_sig = sendTransaction(txn, payer_keypair, opts=TxOpts(skip_preflight=True))
        print("Transaction Signature:", txn_sig)

        return txn_sig
        
    except Exception as e:
        print("Transaction failed:", e)
        return False


def sell(mint_str: str, token_balance: Optional[Union[int, float]] = None, slippage: int = 25, close_token_account: bool = True,payer_keypair=None,fileName=None,envKey=None) -> bool:
    try:
        # Get coin data
        coin_data = get_pump_fun_data(mint_str)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return False

        payer_keypair = payer_keypair or get_payer_keypair()
        owner = payer_keypair.pubkey()
        mint = Pubkey.from_string(mint_str)

        # Check if token account exists; create if necessary
        token_account = get_associated_token_address(owner, mint)
        try:
            account_data = abstract_solana_rate_limited_call('solcatcher', 'get_token_accounts_by_owner', owner, TokenAccountOpts(mint))
            if not account_data.get('value'):  # If no token account exists
                create_account_instr = create_associated_token_account(owner, owner, mint)
                token_account_instructions = [create_account_instr]
        except Exception as e:
            print("Token account check or creation failed:", e)
            return False

        # Calculate token price
        sol_decimal = 10**9
        token_decimal = 10**6
        virtual_sol_reserves = coin_data['virtual_sol_reserves'] / sol_decimal
        virtual_token_reserves = coin_data['virtual_token_reserves'] / token_decimal
        token_price = virtual_sol_reserves / virtual_token_reserves
        print(f"Token Price: {token_price:.20f} SOL")

        # Get token balance if not provided
        if token_balance is None:
            token_balance = get_token_balance(mint_str)
        if token_balance == 0:
            print("No tokens to sell.")
            return False

        # Calculate amount and minimum SOL output
        amount = int(token_balance * token_decimal)
        sol_out = float(token_balance) * token_price
        slippage_adjustment = 1 - (slippage / 100)
        min_sol_output = int(sol_out * slippage_adjustment * LAMPORTS_PER_SOL)

        # Build account key list
        keys = [
            AccountMeta(pubkey=GLOBAL, is_signer=False, is_writable=False),
            AccountMeta(pubkey=FEE_RECIPIENT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['mint']), is_signer=False, is_writable=False),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['associated_bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=owner, is_signer=True, is_writable=True),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False), 
            AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_PROGRAM, is_signer=False, is_writable=False)
        ]

        # Construct the swap instruction
        data = bytearray()
        data.extend(bytes.fromhex("33e685a4017f83ad"))
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', min_sol_output))
        swap_instruction = Instruction(PUMP_FUN_PROGRAM, bytes(data), keys)

        # Construct and sign transaction
        recent_blockhash = get_block_hash()
        txn = Transaction(recent_blockhash=recent_blockhash, fee_payer=owner)
        txn.add(set_compute_unit_price(UNIT_PRICE))
        txn.add(set_compute_unit_limit(UNIT_BUDGET))
        
        if 'token_account_instructions' in locals():
            txn.extend(token_account_instructions)
        
        txn.add(swap_instruction)

        # Conditionally add the close account instruction
        if close_token_account:
            close_instr = close_account(CloseAccountParams(TOKEN_PROGRAM, token_account, owner, owner))
            txn.add(close_instr)

        txn.sign(payer_keypair)

        # Send and confirm transaction
        txn_sig = sendTransaction(txn, payer_keypair, opts=TxOpts(skip_preflight=True))
        print("Transaction Signature", txn_sig)
        confirm = confirm_txn(txn_sig)
        print(confirm)
        return True

    except Exception as e:
        print(f"Sell function encountered an error: {e}")
        return False


    
