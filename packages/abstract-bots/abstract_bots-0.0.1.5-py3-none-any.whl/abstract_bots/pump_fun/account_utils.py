from solana.rpc.api import Client
from solders.keypair import Keypair #type: ignore
from abstract_security import *
from solders.pubkey import Pubkey
def load_from_private_key(env_key=None):
    envKey = env_key or 'AMM_P'
    env_value = get_env_value(key=envKey)
    if env_value:
        return Keypair.from_base58_string(env_value)
def check_existing_token_account(owner: Pubkey, mint: Pubkey):
    try:
        account_data = get_account_by_owner(str(owner), str(mint))
        if account_data:
            token_account = account_data['pubkey']
            print(f"Existing token account found: {token_account}")
            return token_account, None
        else:
            print("No existing token account found. Creating a new one...")
            token_account = get_associated_token_address(owner, mint)
            token_account_instructions = create_associated_token_account(owner, owner, mint)
            return token_account, token_account_instructions
    except Exception as e:
        print(f"Error checking or creating token account: {e}")
        return None, None
def load_keypair_from_file(filename):
    curr = os.path.join(sys.path[0], 'data',  filename)
    with open(curr, 'r') as file:
        secret = json.load(file)
        secret_key = bytes(secret)
        print(base58.b58encode(secret_key))
        return Keypair.from_bytete_key()
def get_payer_keypair(fileName=None,envKey=None):

    payerKeypair = None
    if fileName:
        payerKeypair = load_keypair_from_file(filename)
    if payerKeypair is None:
        payerKeypair = load_from_private_key(env_key=envKey)
    return payerKeypair
payer_keypair =  load_from_private_key()
