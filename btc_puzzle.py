import hashlib
import base58
from tqdm import tqdm
from numba import cuda, jit
import numpy as np

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

# Numba JIT-compiled function to perform the check in parallel
@cuda.jit
def check_private_keys(start, end, target_address, found_key, found_address):
    idx = cuda.grid(1)
    key_int = start + idx
    
    if key_int <= end:
        private_key_hex = f'{key_int:064x}'
        private_key_bytes = np.frombuffer(bytes.fromhex(private_key_hex), dtype=np.uint8)
        
        # Generate public key and address
        sk = ecdsa.SigningKey.from_string(private_key_bytes.tobytes(), curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        public_key_bytes = b'\x04' + vk.to_string()

        sha256_bpk = hashlib.sha256(public_key_bytes).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        hashed_public_key = b'\x00' + ripemd160_bpk

        checksum_full = hashlib.sha256(hashlib.sha256(hashed_public_key).digest()).digest()
        checksum = checksum_full[:4]

        binary_address = hashed_public_key + checksum
        address = base58.b58encode(binary_address).decode('utf-8')
        
        if address == target_address:
            found_key[0] = private_key_hex
            found_address[0] = address

# Allocate memory for result storage
found_key = cuda.device_array(1, dtype=np.object)
found_address = cuda.device_array(1, dtype=np.object)

# Define the number of threads and blocks
threads_per_block = 256
blocks_per_grid = (end80 - start70 + 1 + (threads_per_block - 1)) // threads_per_block

# Launch the kernel
check_private_keys[blocks_per_grid, threads_per_block](start70, end80, target_bitcoin_address, found_key, found_address)

# Retrieve results
found_key = found_key.copy_to_host()
found_address = found_address.copy_to_host()

if found_key[0] is not None and found_address[0] is not None:
    print(f'\nPrivate Key: {found_key[0]}')
    print(f'Bitcoin Address: {found_address[0]}')
else:
    print('Target Bitcoin address not found in the specified range.')
