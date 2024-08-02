from tronapi import Tron
from tronapi import HttpProvider

# Set up the full node and solidity node
full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = HttpProvider('https://api.trongrid.io')

tron = Tron(full_node=full_node, solidity_node=solidity_node, event_server=event_server)

# Set up the private key and the corresponding address
private_key = '0000000000000000000000000000000000000000000000000000000000000002'
tron.private_key = private_key
tron.default_address = tron.address.from_private_key(private_key)

# Destination address
to_address = 'TDvSsdrNM5eeXNL3czpa6AxLDHZA9nwe9K'

# Amount to send (in SUN, where 1 TRX = 1,000,000 SUN)
amount = 101001723  # 101.001723 TRX in SUN

# Create a transaction
txn = tron.trx.send(to_address, amount)

# Sign the transaction
signed_txn = tron.trx.sign(txn)

# Broadcast the transaction
result = tron.trx.broadcast(signed_txn)

# Check the result
print(result)
