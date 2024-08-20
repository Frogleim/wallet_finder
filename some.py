from web3 import Web3
from eth_account import Account

# Example private key (DO NOT use this in a real wallet)
private_key = "00000000000000000000000000000000000000000000000000000000000000ba"

# Create account from private key
account = Account.from_key(private_key)

# Get public key
public_key = account._key_obj.public_key

print(f"Public Key: {public_key}")
