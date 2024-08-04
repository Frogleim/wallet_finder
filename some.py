import hashlib
from tronpy import Tron
from tronpy.keys import PrivateKey
from binascii import unhexlify

# Initialize Tron
client = Tron()

# Your Tron wallet address
address = 'TGZZerZxgReTirdNEXXUpBA39bz469FUtH'

def get_transactions(client, address):
    # Get transactions related to the address
    transactions = client.get_transaction('ae8e0db981f3d6b9ad3bde34537e5f956738e3dd82fd14bb2642fa18647272a4')
    return transactions

def extract_signature(transaction):
    # Extract the signature from the transaction
    signature = transaction['raw_data']['signature']
    return signature[0] if signature else None

def parse_signature(signature_hex):
    # Convert hex signature to bytes
    signature_bytes = unhexlify(signature_hex)
    
    # Parse the DER-encoded signature
    r = int.from_bytes(signature_bytes[:32], 'big')
    s = int.from_bytes(signature_bytes[32:], 'big')
    return r, s

def calculate_message_hash(transaction):
    # Serialize the transaction data
    tx_data = transaction['raw_data_hex']
    
    # Calculate the SHA-256 hash of the transaction data
    z = int(hashlib.sha256(unhexlify(tx_data)).hexdigest(), 16)
    return z

# Example usage
if __name__ == "__main__":
    transactions = get_transactions(client, address)
    
    for tx in transactions:
        signature_hex = extract_signature(tx)
        if signature_hex:
            print(f"Transaction ID: {tx['txID']}")
            print(f"Signature: {signature_hex}")
            
            r, s = parse_signature(signature_hex)
            z = calculate_message_hash(tx)
            
            print(f"r: {r}")
            print(f"s: {s}")
            print(f"z: {z}")
            
            # For demonstration, assume we have one signature
            break
