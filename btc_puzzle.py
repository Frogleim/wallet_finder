import ecdsa
import hashlib
import base58
from tqdm import tqdm

# Function to convert a hex string to a byte array
def hex_to_byte_array(hex_string):
    return bytes.fromhex(hex_string)

# Function to generate a Bitcoin address from a given private key
def private_key_to_bitcoin_address(private_key_hex):
    private_key_bytes = hex_to_byte_array(private_key_hex)
    
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key_bytes = b'\x04' + vk.to_string()

    sha256_bpk = hashlib.sha256(public_key_bytes).digest()
    ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
    hashed_public_key = b'\x00' + ripemd160_bpk

    checksum_full = hashlib.sha256(hashlib.sha256(hashed_public_key).digest()).digest()
    checksum = checksum_full[:4]

    binary_address = hashed_public_key + checksum
    address = base58.b58encode(binary_address).decode('utf-8')
    return private_key_hex, address

# Define the range
start_hex = '20000000000000000'
end_hex = '3ffffffffffffffff'

start = int(start_hex, 16)
end = int(end_hex, 16)

# Calculate 70% to 80% range
range_size = end - start
start70 = start + (range_size * 70) // 100
end80 = start + (range_size * 80) // 100

print(f'Scanning from {hex(start70)} to {hex(end80)}')

# Define the target Bitcoin address (for demonstration purposes, replace with the actual target address)
target_bitcoin_address = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'

# Find Bitcoin private keys in the 70% to 80% range
def find_bitcoin_private_keys_in_range(start, end):
    for i in tqdm(range(start, end + 1), desc="Scanning range", unit="key"):
        private_key_hex = hex(i)[2:].zfill(64)
        private_key, address = private_key_to_bitcoin_address(private_key_hex)
        
        if address == target_bitcoin_address:
            print(f'\nPrivate Key: {private_key}')
            print(f'Bitcoin Address: {address}')
            return private_key, address
    print('Target Bitcoin address not found in the specified range.')

# Scan the range
find_bitcoin_private_keys_in_range(start70, end80)
