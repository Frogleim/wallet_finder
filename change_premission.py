from tronpy import Tron
from tronpy.keys import PrivateKey

client = Tron()
private_key = PrivateKey(bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000002'))

owner_permission = {
    "type": 0,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
        {
            "address": "ADDRESS_OF_ACTIVE_PERMISSION",
            "weight": 1
        }
    ]
}

active_permission = [
    {
        "type": 2,
        "permission_name": "active",
        "threshold": 1,
        "operations": "7fff1fc003b40f11e3dffed3f3c3",
        "keys": [
            {
                "address": "ADDRESS_OF_ACTIVE_PERMISSION",
                "weight": 1
            }
        ]
    }
]

txn = client.trx.account_permission_update(
    owner_address='TDvSsdrNM5eeXNL3czpa6AxLDHZA9nwe9K',
    owner_permission=owner_permission,
    active_permissions=active_permission
)

txn.sign(private_key)
result = txn.broadcast()

print(result)
