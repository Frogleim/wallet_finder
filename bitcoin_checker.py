import os
import hashlib
import requests
from bit import Key
import time

# Define the range limits
start = int("0000000000000000000000000200000000000000000000000000000000000000", 16)
end = int("00000000000000000000000003ffffffffffffffffffffffffffffffffffffff", 16)

# Blockchain.info API URL
blockchain_info_url = 'https://blockchain.info/balance?active='

# Function to convert an integer to a 64-character hex string
def int_to_hex_str(value):
    return f"{value:064x}"

# Function to generate a Bitcoin address from a private key
def private_key_to_btc_address(private_key_hex):
    key = Key.from_hex(private_key_hex)
    return key.address

# Function to get Bitcoin balance
def get_btc_balance(address):
    url = blockchain_info_url + address
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        balance = data[address]['final_balance'] / 1e8  # Bitcoin balance is returned in Satoshis, convert to BTC
        return balance
    return 0

# Directory to save the files
output_dir = "output_keys"
os.makedirs(output_dir, exist_ok=True)

# Generate the keys in the specified range
keys_per_file = 128
current_file_index = 1
keys = []

for num in range(start, end + 1):
    hex_key = int_to_hex_str(num)
    
    btc_address = private_key_to_btc_address(hex_key)  # Generate Bitcoin address
    btc_balance = get_btc_balance(btc_address)  # Check balance
    keys.append(f"{hex_key},{btc_address},{btc_balance}")
    print(f"{hex_key},{btc_address},{btc_balance}")
    
    if len(keys) == keys_per_file:
        with open(f"{output_dir}/keys_{current_file_index}.txt", "w") as f:
            f.write("\n".join(keys))
        current_file_index += 1
        keys = []
    time.sleep(1.8)  # Adding delay to avoid rate limiting

# Write remaining keys if any
if keys:
    with open(f"{output_dir}/bitcoin_keys_{current_file_index}.txt", "w") as f:
        f.write("\n".join(keys))

print("Key generation and balance check complete.")
