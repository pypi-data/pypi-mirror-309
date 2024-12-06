from .constants import *
from .coin_data import get_pump_fun_data
def buy(mint_str: str, sol_in: float = 0.001, slippage: int = 25) -> bool:
   
        # Get coin data
        coin_data = get_pump_fun_data(mint_str)
        if not coin_data:
            print("Failed to retrieve coin data...")
            return False
        payer_keypair = get_payer_keypair()
        owner = payer_keypair.pubkey()
        mint = Pubkey.from_string(mint_str)
        # Attempt to retrieve token account; if not, prepare to create it
        token_account = get_associated_token_address(owner, mint)
        account_data = get_token_accounts_by_owner(owner,mint)
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
            AccountMeta(pubkey=PUMP_FUN_PROGRAM_ID, is_signer=False, is_writable=False)
        ]

        # Construct the swap instruction
        data = bytearray()
        data.extend(bytes.fromhex("66063d1201daebea"))  # Replace with actual instruction identifier
        data.extend(struct.pack('<Q', amount))
        data.extend(struct.pack('<Q', max_sol_cost))
        swap_instruction = Instruction(PUMP_FUN_PROGRAM_ID, bytes(data), keys)

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
