import requests,time, json, struct, os, base58, sys, base64
from utils import isListZero,Pubkey,get_sigKey
from account_utils import check_existing_token_account
from solana.rpc.types import TokenAccountOpts, TxOpts
from solana.transaction import Transaction
from abstract_utilities import get_any_value,safe_json_loads
from abstract_apis import postRpcRequest
from abstract_solcatcher import *
from abstract_solcatcher.database_calls.checkManager import rate_limit
from solders.hash import Hash
def call_solcatcher_api(method,*args,**kwargs):
  return CheckSolcatcher().call_solcatcher_api(method,*args,**kwargs)
def rate_limit(method=None,status_code=False):
  return CheckSolcatcher().get_rate_url(method=method,status_code=status_code)
def log_response(method=None,response=None,status_code=False):
  return CheckSolcatcher().log_response(method=method,response=response,status_code=status_code)
def rate_limit_solcatcher_api(method,*args,**kwargs):
  response = call_solcatcher_api(method,*args,**kwargs)
  logged_response = log_response(method=method,response=response,status_code=kwargs.get('status_code'))
  return response
def exec_request(method,params):
    url = CheckSolcatcher().rateLimiter.get_url(method)
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }
    
    response = postRpcRequest(
        url=url,
        **payload
    )
    rate_limit(method,response)
    return response
def get_value(response_json):
    try:
        account_info = response_json.get("value", {})
        return account_info
    except Exception as e:
        print(f"Error in retrieving account info: {e}")
        return None
def getAccountInfo(mint_str: str) -> dict:
    # Prepare the RPC request payload
    
    method,params = "getAccountInfo",[mint_str, {"encoding": "base64"}]  # Use base64 for direct decoding
    # Send the transaction
    
    response_json = exec_request(method,params)
    # Parse the JSON response
    return get_value(response_json)

def get_account_by_owner(payer, mint_str: str) -> dict:
    method,params = "getTokenAccountsByOwner",[payer, {"mint": mint_str}, {"encoding": "jsonParsed"}]
    response_json = exec_request(method,params)
    accounts = response_json.get("value", {})
    if accounts:
        return accounts[0]  # Return the first account found
    return None

def get_block_hash():
    recent_blockhash = call_solcatcher_api('get_latest_blockhash').get('value',{}).get('blockhash')
    recent_blockhash = Hash.from_string(recent_blockhash)
    return recent_blockhash

def get_account_by_owner(payer,mint_str: str) -> dict:
    # Prepare the RPC request payload
    method,params = "getTokenAccountsByOwner",[payer, {"mint":mint_str},{"encoding": "jsonParsed"}]
    # Send the transaction
    response_json = exec_request(method,params)
    response_json = isListZero(response_json).get('value', isListZero(response_json))
    response_json = isListZero(response_json).get('data', isListZero(response_json))
    # Return the result or the entire response in case of error
    return response_json
def get_token_balance(mint_str: str,pubkey_str):
    method,params = "getTokenAccountsByOwner",[pubkey_str,{"mint": mint_str},{"encoding": "jsonParsed"}]
    response_json = exec_request(method,params)
    ui_amount = get_any_value(response_json, "uiAmount")
    return float(ui_amount)
def sendTransaction(txn: Transaction, payer_keypair,commitment=None, opts=TxOpts(skip_preflight=True)) -> dict:
    # Sign the transaction
    txn.sign(payer_keypair)
    # Serialize the transaction to a base64 string
    txn_base64 = base58.b58encode(txn.serialize()).decode('utf-8')
    # Prepare the RPC request payload
    method,params = "sendTransaction",[txn_base64, {"skipPreflight": opts.skip_preflight, "preflightCommitment":commitment or  "finalized"}]
    # Return the result or the entire response in case of error
    return exec_request(method,params)
def get_transaction(signature,commitment,maxSupportedTransactionVersion=0,max_supported_transaction_version=0):
    # Prepare the RPC request payload
    method,params = "getTransaction",[signature, {"commitment":commitment or "finalized","maxSupportedTransactionVersion":maxSupportedTransactionVersion or  max_supported_transaction_version}]
    # Return the result or the entire response in case of error
    return exec_request(method,params)
def confirm_txn(txn_sig, max_retries=20, retry_interval=3):
    retries = 0
    txn_sig = get_sigKey(txn_sig)
    while retries < max_retries:
            print(txn_sig)
            txn_res = get_transaction(str(txn_sig), commitment="confirmed", max_supported_transaction_version=0)
            if txn_res:
                txn_res = safe_json_loads(txn_res)
                if isinstance(txn_res,dict):
                    txn_json = txn_res.get('meta')
                    if txn_json and isinstance(txn_json,dict):
                        if txn_json['err'] is None:
                            print("Transaction confirmed... try count:", retries+1)
                            return True
                        print("Error: Transaction not confirmed. Retrying...")
                        if txn_json['err']:
                            print("Transaction failed.")
                            return False

    print("Max retries reached. Transaction confirmation failed.")
    return None
