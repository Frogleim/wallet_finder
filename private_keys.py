import os
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1

# Define the range limits
start = int("0000000000000000000000000000000000000000000000020000000000000000", 16)
end = int("000000000000000000000000000000000000000000000003ffffffffffffffff", 16)

# Function to convert an integer to a 64-character hex string
def int_to_hex_str(value):
    return f"{value:064x}"

# Function to perform double SHA-256 hashing
def bin_dbl_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

# Function to generate a Bitcoin address from a private key
def privkey_to_address(privkey_hex):
    privkey_bytes = bytes.fromhex(privkey_hex)
    sk = SigningKey.from_string(privkey_bytes, curve=SECP256k1)
    vk = sk.verifying_key
    pubkey = b'\x04' + vk.to_string()
    sha256 = hashlib.sha256(pubkey).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    extended_ripemd160 = b'\x00' + ripemd160  # Prefix with 0x00 for mainnet
    checksum = bin_dbl_sha256(extended_ripemd160)[:4]
    binary_address = extended_ripemd160 + checksum
    address = base58.b58encode(binary_address).decode()
    return address

# Directory to save the files
output_dir = "output_keys"
os.makedirs(output_dir, exist_ok=True)

# Generate the keys in the specified range
keys_per_file = 128
current_file_index = 1
keys = []

for num in range(start, end + 1):
    hex_key = int_to_hex_str(num)
    bitcoin_address = privkey_to_address(hex_key)  # Generate Bitcoin address
    keys.append(f"{hex_key},{bitcoin_address}")
    
    if len(keys) == keys_per_file:
        with open(f"{output_dir}/keys_{current_file_index}.txt", "w") as f:
            f.write("\n".join(keys))
        current_file_index += 1
        keys = []

# Write remaining keys if any
if keys:
    with open(f"{output_dir}/keys_{current_file_index}.txt", "w") as f:
        f.write("\n".join(keys))
