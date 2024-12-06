from .key import get_keypair
from solders.transaction import VersionedTransaction
from solders.message import to_bytes_versioned

def sign_transaction(transaction: VersionedTransaction) -> VersionedTransaction:
    keypair = get_keypair()
    signatures = [
        keypair.sign_message(to_bytes_versioned(transaction.message)),
    ]
    signed_transaction = VersionedTransaction.populate(
            transaction.message, signatures
    )
    return signed_transaction