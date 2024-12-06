def confirm_txn(txn_sig, max_retries=20, retry_interval=3):
    retries = 0
    
    while retries < max_retries:
        try:
            
            txn_res = get_transaction(signature=str(txn_sig))
            if txn_res:
                print(txn_res)
                print(f"\n\nhttps://solscan.io/tx/{str(txn_sig)}")
                break
            txn_json = safe_json_loads(txn_res.get('transaction',{}).get('meta',{}))
            error = txn_json.get('err')
            if error is None:
                print("Transaction confirmed... try count:", retries+1)
                return True
            print("Error: Transaction not confirmed. Retrying...")
            if error:
                print("Transaction failed.")
                return False
        except Exception as e:
            print("Awaiting confirmation... try count:", retries+1)
            retries += 1
            time.sleep(retry_interval)
    print("Max retries reached. Transaction confirmation failed.")
    return None


def buildTxn(mint, amount, slippage, token_account_pubkey,sol_in,token_account_instructions,buy=True):
    # Get keys for the transaction, pass the token account's pubkey instead of the AccountMeta object
    keys = getKeys(get_coin_data(mint), token_account_pubkey, owner,buy=buy)
    
    if buy:
        # Calculate max_sol_cost
        slippage_adjustment = 1 + (slippage / 100)
        sol_in_with_slippage = sol_in * slippage_adjustment
        max_sol_cost = int(sol_in_with_slippage * LAMPORTS_PER_SOL)
        print("Max Sol Cost:", sol_in_with_slippage)
        hex_data = bytes.fromhex("66063d1201daebea")
        solCost = max_sol_cost
    else:
        # Calculate minimum SOL output
        sol_out = float(token_balance) * float(token_price)
        slippage_adjustment = 1 - (slippage / 100)
        sol_out_with_slippage = sol_out * slippage_adjustment
        min_sol_output = int(sol_out_with_slippage * LAMPORTS_PER_SOL)
        print("Min Sol Output:", sol_out_with_slippage)
        hex_data = bytes.fromhex("33e685a4017f83ad")
        solCost = min_sol_output
    
    data = bytearray()
    data.extend(hex_data)
    data.extend(struct.pack('<Q', amount))
    data.extend(struct.pack('<Q', solCost))
    data = bytes(data)
    swap_instruction = Instruction(PUMP_FUN_PROGRAM, data, keys)
    blockHash = requests.post(url="https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370",data=json.dumps({"id":1,"jsonrpc":"2.0","method":"getLatestBlockhash","params":[{"commitment":"processed"}]}))
    recent_blockhash = get_any_value(blockHash.json(),'blockhash')
    recent_blockhash = Hash.from_string(recent_blockhash)
    txn = Transaction(recent_blockhash=recent_blockhash, fee_payer=owner)
    txn.add(set_compute_unit_price(UNIT_PRICE))
    txn.add(set_compute_unit_limit(UNIT_BUDGET))
    
    if buy:
        if token_account_instructions:
            txn.add(token_account_instructions)
        txn.add(swap_instruction)
    else:
        txn.add(swap_instruction)
        if close_token_account:
            close_account_instructions = close_account(CloseAccountParams(TOKEN_PROGRAM, token_account_pubkey, owner, owner))
            txn.add(close_account_instructions)
    
    txn.sign(payer_keypair)
    # Send and confirm transaction
    txn_sig = sendTransaction(txn, payer_keypair, opts=TxOpts(skip_preflight=True))
    print("Transaction Signature", txn_sig)
    confirm = confirm_txn(txn_sig)
    print(confirm)
