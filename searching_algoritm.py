from bip_utils import Bip44, Bip44Coins, Bip44Changes

def guess_derivation_path(public_key, coin_type):
    # Assuming you have the public key and the coin type
    # You can attempt to derive paths and match the public key
    for account in range(10):
        for change in [0, 1]:
            for address_index in range(100):
                bip44_obj = Bip44.FromExtendedKey(public_key, Bip44Coins.ETHEREUM)
                derived_pub_key = bip44_obj.Purpose().Coin().Account(account).Change(change).AddressIndex(address_index).PublicKey().ToAddress()
                if derived_pub_key == public_key:
                    return f"m/44'/{coin_type}'/{account}'/{change}/{address_index}"
    return None

public_key = "0x3e805fa563758c7b2187ee0a7a4e2503495f3686c9351822b054d3844f1724c1e74d9c8f8463ea37ec1daf204a51288acc12918983bf74f00b4eeba071b0594b"
coin_type = 60  # For Ethereum

path = guess_derivation_path(public_key, coin_type)
if path:
    print(f"Derivation Path: {path}")
else:
    print("Derivation path not found.")
