from solders.pubkey import Pubkey
from solana.transaction import Signature
from abstract_utilities import safe_json_loads
def isListZero(list_obj):
    if isinstance(list_obj,list) and len(list_obj)>0:
        return list_obj[0]
    return list_obj
def get_pubkey(address):
    # Convert address string to Pubkey, with error handling
    if isinstance(address, Pubkey):
        return address
    address = str(address)
    try:
        return Pubkey.from_string(address)
    except Exception as e:
        print(f"Invalid address format: {e}")
        return None
def get_pubKey(address):
    # Convert address string to Pubkey, with error handling
    if isinstance(address, Pubkey):
        return address
    address = str(address)
    try:
        return Pubkey.from_string(address)
    except Exception as e:
        print(f"Invalid address format: {e}")
        return None
def get_sigKey(txn_sig):
    if isinstance(txn_sig, Signature):
        return txn_sig
    txn_sig = str(txn_sig)
    try:
        return Signature.from_string(txn_sig)
    except Exception as e:
        print(f"Invalid address format: {e}")
        return None
