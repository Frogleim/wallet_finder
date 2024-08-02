import warnings

warnings.filterwarnings(action='ignore')

from ecdsa import SigningKey, SECP256k1
import tronpy
from tronpy.keys import PrivateKey
import time

def private_key_to_tron_address(private_key_hex):
    private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    public_key_bytes = public_key.to_string()
    address = tronpy.keys.public_key_to_base58check_addr(public_key_bytes)
    return address

def check_trx_balance(client, address):
    try:
        balance = client.get_account_balance(address)
        return balance
    except Exception as e:
        print(f"Error checking TRX balance for {address}: {e}")
        return None

def check_usdt_balance(client, address):
    try:
        contract = client.get_contract('Tether USD')
        balance = contract.functions.balanceOf(address)
        return balance
    except Exception as e:
        print(f"Error checking USDT balance for {address}: {e}")
        return None

def main():
    client = tronpy.Tron()
    start = int("0000000000000000000000000000000000000000000000000000000000000400", 16)
    end = int("00000000000000000000000000000000000000000000000000000000000007ff", 16)

    with open('tron_addresses.txt', 'w') as file:
        for private_key_int in range(start, end + 1):
            private_key_hex = f'{private_key_int:064x}'
            address = private_key_to_tron_address(private_key_hex)
            
            trx_balance = check_trx_balance(client, address)
            usdt_balance = check_usdt_balance(client, address)
            
            if trx_balance is not None or usdt_balance is not None:
                output = (f"Private Key: {private_key_hex}, Address: {address}, "
                          f"TRX Balance: {trx_balance}, USDT Balance: {usdt_balance}\n")
                print(output)
                file.write(output)
                time.sleep(2)

if __name__ == "__main__":
    main()
