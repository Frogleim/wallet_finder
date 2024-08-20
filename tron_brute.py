import tronpy
from tronpy.keys import PrivateKey
import random

# The target TRON address
target_address = 'TDvSsdrNM5eeXNL3czpa6AxLDHZA9nwe9K'


def generate_random_private_key():
    return PrivateKey.fromhex(f'{random.getrandbits(256):064x}')


def find_private_key(target_address):
    attempts = 0
    while True:
        private_key = generate_random_private_key()
        public_key = private_key.public_key
        tron_address = public_key.to_base58check_address()

        attempts += 1
        if tron_address == target_address:
            print(f"Private Key found: {private_key.hex()} after {attempts} attempts")
            break

        if attempts % 100000 == 0:
            print(f"Attempts: {attempts}")


if __name__ == "__main__":
    find_private_key(target_address)
