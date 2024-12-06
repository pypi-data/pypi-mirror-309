import os 
from solders.keypair import Keypair
from mnemonic import Mnemonic
from .logger import logger

mnemo = Mnemonic("english")

def get_derive_path() -> str:
    path = os.getenv('DERIVE_PATH', "m/44'/501'/0'")
    return path

def generate_words() -> str:
    return mnemo.generate(strength=256)

def get_secret_words() -> str:
    words = os.getenv('SECRET_WORDS', None)
    if words is None:
        logger.info("No secret words found, generating new ones")
        words = generate_words()
    return words

def load_keypair() -> Keypair:
    mnemonic = get_secret_words()
    seed = mnemo.to_seed(mnemonic)
    derive_path = get_derive_path()
    keypair = Keypair.from_seed_and_derivation_path(seed, derive_path)
    logger.info("Loaded keypair. Public key: %s", keypair.pubkey())
    return keypair

_global_keypair = None
def get_keypair() -> Keypair:
    global _global_keypair
    if _global_keypair is None:
        _global_keypair = load_keypair()
    return _global_keypair

def get_public_key_as_str() -> str:
    keypair = get_keypair()
    return str(keypair.pubkey())