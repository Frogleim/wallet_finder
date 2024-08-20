import ecdsa
import hashlib
import base58

# Define the range for private keys
start_range = int('0000000000000000000000000000000000000000000000000000000000200000', 16)
end_range = int('00000000000000000000000000000000000000000000000000000000003fffff', 16)


def private_key_to_public_key(private_key):
    """ Convert the private key to a public key. """
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(f'{private_key:064x}'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return b'\x04' + vk.to_string()


def public_key_to_address(public_key):
    """ Convert the public key to a Toncoin address. """
    # Use SHA-256 and then RIPEMD-160 for hashing the public key
    sha256 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    hashed_public_key = ripemd160.digest()

    # Toncoin specific prefix, you may need to adjust this depending on Toncoin's address format
    extended_key = b'\x00' + hashed_public_key

    # Calculate the checksum
    first_sha256 = hashlib.sha256(extended_key).digest()
    second_sha256 = hashlib.sha256(first_sha256).digest()
    checksum = second_sha256[:4]

    # Encode the address using Base58
    address = base58.b58encode(extended_key + checksum)
    return address


def find_toncoin_wallet():
    """ Find a Toncoin wallet within the specified range. """
    for private_key in range(start_range, end_range + 1):
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)
        print(f"Private Key: {private_key:064x} -> Address: {address.decode()}")
        if address.decode() == '1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv':
            print('Found')
            break
        # Here you can add any specific condition to check for a valid Toncoin address


if __name__ == "__main__":
    find_toncoin_wallet()
