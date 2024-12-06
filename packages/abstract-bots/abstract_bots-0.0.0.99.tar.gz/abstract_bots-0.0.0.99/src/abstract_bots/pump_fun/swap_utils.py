def pump_fun_buy(mint_str: str, sol_in: float = 0.001, slippage: int = 25) -> bool:
    coin_data = get_coin_data(mint_str)
    print("Coin Data:", coin_data)

    if not coin_data:
        print("Failed to retrieve coin data...")
        return False

    payer_keypair = Keypair.from_base58_string(get_env_value(key='AMM_P'))
    owner = payer_keypair.pubkey()
    print("Owner Public Key:", owner)

    mint = Pubkey.from_string(mint_str)
    token_account, token_account_instructions = check_existing_token_account(owner, mint)
    print("Token Account:", token_account)

    if not token_account:
        print("Failed to retrieve or create token account.")
        return False

    virtual_sol_reserves = coin_data['virtual_sol_reserves']
    virtual_token_reserves = coin_data['virtual_token_reserves']
    sol_in_lamports = sol_in * LAMPORTS_PER_SOL
    amount = int(sol_in_lamports * virtual_token_reserves / virtual_sol_reserves)
    print("Calculated Amount:", amount)

    buildTxn(mint, amount, slippage, token_account, sol_in, token_account_instructions, buy=True)

    time.sleep(2)

    return True
pump_fun_buy("4dCfQ7pSPihS4LnZjYgXznjJ3yEEwQbKQTbCfin9pump")
