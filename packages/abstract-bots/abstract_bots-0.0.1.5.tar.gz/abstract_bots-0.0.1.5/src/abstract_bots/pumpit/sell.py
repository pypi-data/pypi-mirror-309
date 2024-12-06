from .constants import *
from .coin_data import get_pump_fun_data
def sell(mint_str: str,token_balance: Optional[Union[int, float]] = None,slippage: int = 25,close_token_account: bool = True) -> bool:
  
        # Get coin data
        coin_data = get_pump_fun_data(mint_str)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return False

        payer_keypair = get_payer_keypair()
        owner = payer_keypair.pubkey()
        mint = get_pubkey(coin_data['mint'])

        # Check if token account exists; create if necessary
        token_account = get_associated_token_address(owner, mint)
        account_data = get_token_accounts_by_owner(owner,mint)
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
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False), 
            AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=False),
            AccountMeta(pubkey=EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_PROGRAM_ID, is_signer=False, is_writable=False)
        ]
        # Construct the swap instruction
        data = bytearray()
        data.extend(bytes.fromhex("33e685a4017f83ad"))  # Replace with actual instruction identifier for 'sell'
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', min_sol_output))
        swap_instruction = Instruction(PUMP_FUN_PROGRAM_ID, bytes(data), keys)

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
