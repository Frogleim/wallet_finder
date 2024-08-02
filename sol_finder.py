import time
import requests
from bitcoin import *

def generate_private_key(start_key: int) -> str:
    key = start_key.to_bytes(32, byteorder='big')
    return key.hex()

def get_litecoin_address(private_key_hex: str) -> str:
    private_key = private_key_hex
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key, magicbyte=48)  # 48 is the version byte for Litecoin mainnet addresses
    return address

def check_balance(address: str) -> float:
    url = f'https://chain.so/api/v2/get_address_balance/LTC/{address}'
    while True:
        try:
            response = requests.get(url)
            data = response.json()
            print(data)
            balance_ltc = float(data['data']['confirmed_balance'])
            return balance_ltc
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(1)  # Delay to handle rate limit

def save_to_file(data: str, filename: str = "output.txt"):
    with open(filename, 'a') as file:
        file.write(data + '\n')

def main():
    start_key = 400
    stop_key = 0x7ff
    filename = "LTC.txt"

    for key_int in range(start_key, stop_key + 1):
        private_key_hex = generate_private_key(key_int)
        address = get_litecoin_address(private_key_hex)
        
        balance = check_balance(address)
        data = f'Address: {address} | Balance: {balance} LTC | Private Key: {private_key_hex}'
        print(data)
        save_to_file(data, filename)
        time.sleep(1)  # Delay to handle rate limit

if __name__ == '__main__':
    main()
