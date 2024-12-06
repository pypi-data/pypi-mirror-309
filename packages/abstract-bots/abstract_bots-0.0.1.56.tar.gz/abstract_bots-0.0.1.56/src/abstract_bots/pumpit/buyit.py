import logging
# Suppress logs below WARNING level
logging.basicConfig(level=logging.WARNING)
import struct
from spl.token.instructions import create_associated_token_account, get_associated_token_address, close_account, CloseAccountParams
from typing import Optional,Union
from solana.transaction import AccountMeta, Transaction
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from account_utils import payer_keypair,get_payer_keypair
from constants import *
from isolated_rpcs import sendTransaction, Hash,get_token_balance
from abstract_solcatcher import abstract_solana_rate_limited_call
from solana.rpc.types import TxOpts
from coin_data import get_pump_fun_data
from solana.rpc.types import TokenAccountOpts

mint = "AX4WqXbNvj8Um8SU1yGiVLFW1P3fwxEQR5gz2uv9pump"
TOKEN_PROGRAM = get_pubkey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
ASSOC_TOKEN_ACC_PROG = get_pubkey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
RENT = Pubkey.from_string("SysvarRent111111111111111111111111111111111")
def get_block_hash():
    recent_blockhash = abstract_solana_rate_limited_call('get_latest_blockhash').get('value', {}).get('blockhash')
    return Hash.from_string(recent_blockhash)

def buy(mint_str: str, sol_in: float = 0.001, slippage: int = 25) -> bool:
   
        # Get coin data
        coin_data = get_pump_fun_data(mint_str)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return False

        owner = payer_keypair.pubkey()
        mint = Pubkey.from_string(mint_str)
        
        # Attempt to retrieve token account; if not, prepare to create it
        token_account = get_associated_token_address(owner, mint)
        account_data = abstract_solana_rate_limited_call('get_token_accounts_by_owner', owner, TokenAccountOpts(mint))
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
            AccountMeta(pubkey=GLOBAL, is_signer=False, is_writable=False),
            AccountMeta(pubkey=FEE_RECIPIENT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['mint']), is_signer=False, is_writable=False),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['associated_bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=owner, is_signer=True, is_writable=True),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_PROGRAM, is_signer=False, is_writable=False)
        ]

        # Construct the swap instruction
        data = bytearray()
        data.extend(bytes.fromhex("66063d1201daebea"))  # Replace with actual instruction identifier
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', max_sol_cost))
        swap_instruction = Instruction(PUMP_FUN_PROGRAM, bytes(data), keys)

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
      
def sell(
    mint_str: str,
    token_balance: Optional[Union[int, float]] = None,
    slippage: int = 25,
    close_token_account: bool = True,

) -> bool:
  
        # Get coin data
        coin_data = get_pump_fun_data(mint_str)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return False

        payer_keypair = get_payer_keypair()
        owner = payer_keypair.pubkey()
        owner = payer_keypair.pubkey()
        mint = get_pubkey(coin_data['mint'])

        # Check if token account exists; create if necessary
        token_account = get_associated_token_address(owner, mint)
        account_data = abstract_solana_rate_limited_call('get_token_accounts_by_owner',  owner, TokenAccountOpts(mint))
        token_account_instructions = None

        if not account_data.get('value'):
            # If token account does not exist, create the associated token account
            print("Creating new associated token account...")
            create_account_instr = create_associated_token_account(owner, owner, mint)
            token_account_instructions = [create_account_instr]

        # Calculate token price
        sol_decimal = 10**9
        token_decimal = 10**6
        virtual_sol_reserves = coin_data['virtual_sol_reserves'] / sol_decimal
        virtual_token_reserves = coin_data['virtual_token_reserves'] / token_decimal
        token_price = virtual_sol_reserves / virtual_token_reserves
        print(f"Token Price: {token_price:.20f} SOL")

        # Get token balance if not provided
        if token_balance is None:
            token_balance = get_token_balance(mint_str,str(owner))
        if token_balance == 0:
            print("No tokens to sell.")
            return False

        seeds = [b"event_authority"]
        PUMP_FUN_PROGRAM_ID = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")
        event_authority_pubkey, bump = Pubkey.find_program_address(seeds, PUMP_FUN_PROGRAM_ID)

        # Calculate amount and minimum SOL output
        amount = int(token_balance * token_decimal)
        sol_out = float(token_balance) * token_price
        slippage_adjustment = 1 - (slippage / 100)
        min_sol_output = int(sol_out * slippage_adjustment * LAMPORTS_PER_SOL)
        # Build account key list with corrected order
        keys = [
            AccountMeta(pubkey=GLOBAL, is_signer=False, is_writable=False),
            AccountMeta(pubkey=FEE_RECIPIENT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['mint']), is_signer=False, is_writable=False),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=Pubkey.from_string(coin_data['associated_bonding_curve']), is_signer=False, is_writable=True),
            AccountMeta(pubkey=token_account, is_signer=False, is_writable=True),
            AccountMeta(pubkey=owner, is_signer=True, is_writable=True),
            AccountMeta(pubkey=get_pubkey(SYSTEM_PROGRAM), is_signer=False, is_writable=False), 
            AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=get_pubkey(PUMP_FUN_PROGRAM), is_signer=False, is_writable=False)
        ]
        # Construct the swap instruction
        data = bytearray()
        data.extend(bytes.fromhex("33e685a4017f83ad"))  # Replace with actual instruction identifier for 'sell'
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', min_sol_output))
        swap_instruction = Instruction(get_pubkey(PUMP_FUN_PROGRAM), bytes(data), keys)

        # Construct and sign transaction
        recent_blockhash = get_block_hash()
        txn = Transaction(recent_blockhash=recent_blockhash, fee_payer=owner)
        txn.add(set_compute_unit_price(UNIT_PRICE))
        txn.add(set_compute_unit_limit(UNIT_BUDGET))

        if token_account_instructions:
            txn.extend(token_account_instructions)

        txn.add(swap_instruction)

        # Conditionally add the close account instruction
        if close_token_account:
            close_instr = close_account(CloseAccountParams(
                program_id=get_pubkey(TOKEN_PROGRAM),
                account=token_account,
                dest=owner,
                owner=owner
            ))
            txn.add(close_instr)

        txn.sign(payer_keypair)

        # Send and confirm transaction
        txn_sig = sendTransaction(txn, payer_keypair, opts=TxOpts(skip_preflight=True))
        print("Transaction Signature:", txn_sig)

        return txn_sig



   
sell(mint)
