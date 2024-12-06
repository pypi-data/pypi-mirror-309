import base64
from spl.token.instructions import get_associated_token_address
from construct import Padding, Struct, Int64ul, Flag
from constants import PUMP_FUN_PROGRAM,get_pubKey,Pubkey
from isolated_rpcs import getAccountInfo
# Define the struct format for virtual reserves
bonding_curve_struct = Struct(
    Padding(8),
    "virtual_token_reserves" / Int64ul,
    "virtual_sol_reserves" / Int64ul,
    "real_token_reserves" / Int64ul,
    "real_sol_reserves" / Int64ul,
    "token_total_supply" / Int64ul,
    "complete" / Flag
)

    
def get_virtual_reserves(bonding_curve: Pubkey):
    # Convert Pubkey to string for JSON compatibility
    bonding_curve_str = str(bonding_curve)
    
    account_info = getAccountInfo(bonding_curve_str)
    
    # Check if account info retrieval was successful
    if not account_info or 'data' not in account_info:
        print("Failed to retrieve account info.")
        return None

    try:
        # Decode base64 data and parse it using the struct format
        data_base64 = account_info['data'][0]
        data = base64.b64decode(data_base64)
        parsed_data = bonding_curve_struct.parse(data)
    except Exception as e:
        print(f"Error decoding and parsing data: {e}")
        return None

    return parsed_data

def derive_bonding_curve(mint):
    # Find bonding curve address based on mint
    return Pubkey.find_program_address(["bonding-curve".encode(), bytes(get_pubKey(mint))], PUMP_FUN_PROGRAM)

def derive_bonding_curve_accounts(mint_str: str):
    mint = get_pubKey(mint_str)
    bonding_curve, _ = derive_bonding_curve(mint)
    associated_bonding_curve = get_associated_token_address(bonding_curve, mint)
    return {'bonding_curve': bonding_curve, "associated_bonding_curve": associated_bonding_curve}

def get_pump_fun_data(mint_str: str):
    # Derive bonding curve and associated account
    bonding_curve_data = derive_bonding_curve_accounts(mint_str)
    bonding_curve = bonding_curve_data['bonding_curve']
    associated_bonding_curve = bonding_curve_data['associated_bonding_curve']
    
    # Retrieve virtual reserves
    virtual_reserves = get_virtual_reserves(bonding_curve)
    
    if virtual_reserves is None:
        print("Failed to retrieve virtual reserves data.")
        return None

    # Extract reserves data into dictionary
    txn_data = {
        "mint": mint_str,
        "bonding_curve": str(bonding_curve),
        "associated_bonding_curve": str(associated_bonding_curve),
        "virtual_token_reserves": virtual_reserves.virtual_token_reserves,
        "virtual_sol_reserves": virtual_reserves.virtual_sol_reserves,
        "token_total_supply": virtual_reserves.token_total_supply,
        "complete": virtual_reserves.complete
    }
    
    return txn_data
