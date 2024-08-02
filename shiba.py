from ecdsa import SigningKey, SECP256k1
from web3 import Web3
import time
import json

# Define the ERC-20 token contract address and ABI (example with USDT)
TOKEN_ADDRESS = '0xPEPE_TOKEN_CONTRACT_ADDRESS'
TOKEN_ABI = json.loads('''
[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]
''')

def private_key_to_ethereum_address(private_key_hex):
    private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    public_key_bytes = b'\x04' + public_key.to_string()  # Add the prefix for uncompressed public key
    address = Web3.toChecksumAddress(Web3.keccak(public_key_bytes)[-20:])
    return address

def check_balance(web3, contract, address):
    try:
        balance = contract.functions.balanceOf(address).call()
        return balance
    except Exception as e:
        print(f"Error checking balance for {address}: {e}")
        return None

def main():
    web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))
    contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=TOKEN_ABI)
    
    start = int("0000000000000000000000000000000000000000000000000000000000000001", 16)
    end = int("0000000000000000000000000000000000000000000000000000000000003fff", 16)

    with open('pepe_addresses.txt', 'w') as file:
        for private_key_int in range(start, end + 1):
            private_key_hex = f'{private_key_int:064x}'
            address = private_key_to_ethereum_address(private_key_hex)
            
            balance = check_balance(web3, contract, address)
            
            if balance is not None:
                output = (f"Private Key: {private_key_hex}, Address: {address}, Balance: {balance}\n")
                print(output)
                file.write(output)
                time.sleep(1)

if __name__ == "__main__":
    main()
