import time
from web3 import Web3
from eth_account import Account

def generate_private_key(start_key: int) -> str:
    key = start_key.to_bytes(32, byteorder='big')
    return key.hex()

def check_balance(client: Web3, address: str) -> float:
    while True:
        try:
            balance_wei = client.eth.get_balance(address)
            balance_matic = Web3.from_wei(balance_wei, 'ether')
            return balance_matic
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(1)  # Delay to handle rate limit

def save_to_file(data: str, filename: str = "output.txt"):
    with open(filename, 'a') as file:
        file.write(data + '\n')

def main():
    client = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))
    start_key = 400
    stop_key = 0x7ff
    filename = "MATIC.txt"

    for key_int in range(start_key, stop_key + 1):
        private_key_hex = generate_private_key(key_int)
        account = Account.from_key(private_key_hex)
        address = account.address
        
        balance = check_balance(client, address)
        data = f'Address: {address} | Balance: {balance} MATIC | Private Key: {private_key_hex}'
        print(data)
        save_to_file(data, filename)
        time.sleep(1)  # Delay to handle rate limit

if __name__ == '__main__':
    main()
