from ecdsa import SigningKey, SECP256k1
import tronpy
from tronpy.keys import PrivateKey
import time
import binascii
import os


def generate_random_private_key():
    random_bytes = os.urandom(32)
    
    # Convert the bytes to a hexadecimal string
    hex_string = binascii.hexlify(random_bytes).decode('utf-8')
    
    return hex_string

def generate_tron_wallet():
    sk = SigningKey.generate(curve=SECP256k1)
    #private_key_hex = sk.to_string().hex()
    private_key_hex = generate_random_private_key()
    private_key = PrivateKey(bytes.fromhex(private_key_hex))
    address = private_key.public_key.to_base58check_address()
    return private_key, address

def check_trx_balance(client, address):
    try:
        balance = client.get_account_balance(address)
        return balance
    except Exception as e:
        print(f"Error checking TRX balance for {address}: {e}")
        return None

def check_usdt_balance(client, address):
    try:
        usdt_contract_address = 'TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj'  # USDT TRC-20 contract address on Tron
        contract = client.get_contract(usdt_contract_address)
        balance = contract.functions.balanceOf(address)
        return balance
    except Exception as e:
        print(f"Error checking USDT balance for {address}: {e}")
        return None

def main():
    client = tronpy.Tron()
    
    while True:
        private_key, address = generate_tron_wallet()
        private_key_hex = private_key.hex()

        trx_balance = check_trx_balance(client, address)
        usdt_balance = check_usdt_balance(client, address)

        output = (f"Private Key: {private_key_hex}, Address: {address}, "
                  f"TRX Balance: {trx_balance}, USDT Balance: {usdt_balance}\n")
        print(output)

        with open('generated_tron_wallets.txt', 'a') as file:
            file.write(output)
        
        # Add delay to avoid rate limiting
        time.sleep(2)

if __name__ == "__main__":
    main()
