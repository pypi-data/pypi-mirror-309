from solders.pubkey import Pubkey
def get_coin_data(mint_str):
    return get_pump_fun_data(str(mint_str))      
def get_virtual_reserves(bonding_curve: Pubkey):
    bonding_curve_struct = Struct(
        Padding(8),
        "virtualTokenReserves" / Int64ul,
        "virtualSolReserves" / Int64ul,
        "realTokenReserves" / Int64ul,
        "realSolReserves" / Int64ul,
        "tokenTotalSupply" / Int64ul,
        "complete" / Flag
    )
    
    try:
        account_info = client.get_account_info(bonding_curve)
        data = account_info['value']['data']
        parsed_data = bonding_curve_struct.parse(data)
        return parsed_data
    except Exception:
        return None
def derive_bonding_curve_accounts(mint_str: str):
    try:
        mint = Pubkey.from_string(mint_str)
        bonding_curve, _ = Pubkey.find_program_address(
            ["bonding-curve".encode(), bytes(mint)],
            PUMP_FUN_PROGRAM
        )
        associated_bonding_curve = get_associated_token_address(bonding_curve, mint)
        return bonding_curve, associated_bonding_curve
    except Exception:
        return None, None
def getKeys(coin_data,token_account,owner,buy=True):
        coin_data = get_pump_fun_data(str(mint_str))
        MINT = Pubkey.from_string(coin_data['mint'])
        BONDING_CURVE = Pubkey.from_string(coin_data['bonding_curve'])
        ASSOCIATED_BONDING_CURVE = Pubkey.from_string(coin_data['associated_bonding_curve'])
        ASSOCIATED_USER = Pubkey.from_string(str(token_account))
        USER = Pubkey.from_string(str(payer_keypair.pubkey()))
        PUMP_FUN_TOKEN_PROGRAM_SWITCH = PUMP_FUN_TOKEN_PROGRAM if buy else PUMP_FUN_ASSOC_TOKEN_ACC_PROG
        PUMP_FUN_RENT_PROGRAM_SWITCH = PUMP_FUN_RENT if buy else PUMP_FUN_TOKEN_PROGRAM
        # Build account key list 
        keys = [
            AccountMeta(pubkey=PUMP_FUN_GLOBAL, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_FEE_RECIPIENT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=MINT, is_signer=False, is_writable=False),
            AccountMeta(pubkey=BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_BONDING_CURVE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOCIATED_USER, is_signer=False, is_writable=True),
            AccountMeta(pubkey=USER, is_signer=True, is_writable=True),
            AccountMeta(pubkey=PUMP_FUN_SYSTEM_PROGRAM, is_signer=False, is_writable=False), 
            AccountMeta(pubkey=PUMP_FUN_TOKEN_PROGRAM_SWITCH, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_RENT_PROGRAM_SWITCH, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_EVENT_AUTHORITY, is_signer=False, is_writable=False),
            AccountMeta(pubkey=PUMP_FUN_PROGRAM, is_signer=False, is_writable=False)
        ]
        return keys
