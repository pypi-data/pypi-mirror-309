import logging
# Suppress logs below WARNING level
logging.basicConfig(level=logging.WARNING)
import struct
from spl.token.instructions import create_associated_token_account, get_associated_token_address, close_account, CloseAccountParams
from typing import Optional,Union
from solana.transaction import AccountMeta, Transaction
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from .account_utils import payer_keypair,get_payer_keypair
from .isolated_rpcs import *
from abstract_solcatcher import abstract_solana_rate_limited_call
from solana.rpc.types import TxOpts
from solana.rpc.types import TokenAccountOpts
from .utils import *
from .account_utils import *
seeds = [b"event_authority"]
GLOBAL = get_pubKey("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf")
FEE_RECIPIENT = get_pubKey("CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM")
TOKEN_PROGRAM = get_pubKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
ASSOC_TOKEN_ACC_PROG = get_pubKey("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
RENT = get_pubKey("SysvarRent111111111111111111111111111111111")
EVENT_AUTHORITY = get_pubKey("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1")
GLOBAL = get_pubKey("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf")
SYSTEM_PROGRAM = get_pubKey("11111111111111111111111111111111")
PUMP_FUN_PROGRAM_ID = get_pubKey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")
event_authority_pubkey, bump = Pubkey.find_program_address(seeds, PUMP_FUN_PROGRAM_ID)
LAMPORTS_PER_SOL = 1_000_000_000
UNIT_PRICE =  1_000_000
UNIT_BUDGET =  100_000
