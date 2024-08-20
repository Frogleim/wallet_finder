from ecdsa import SigningKey, SECP256k1
import hashlib
import base58

def private_key_to_tron_address(private_key_hex):
    # Step 1: Generate the public key
    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    public_key_bytes = b'\x04' + sk.verifying_key.to_string()  # Uncompressed public key format
    
    # Step 2: Generate the 20-byte address using SHA-256 and RIPEMD-160
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    
    # Step 3: Prepend the TRON network identifier (0x41)
    network_id = b'\x41'
    tron_address_with_net = network_id + ripemd160_hash
    
    # Step 4: Calculate the checksum
    checksum = hashlib.sha256(hashlib.sha256(tron_address_with_net).digest()).digest()[:4]
    
    # Step 5: Combine the address and checksum, then encode using Base58Check
    tron_address_bytes = tron_address_with_net + checksum
    tron_address = base58.b58encode(tron_address_bytes)
    
    return tron_address.decode()

# Example usage with the given private key
private_key_hex = "0000000000000000000000000000000000000000000000000000000000000001"
tron_address = private_key_to_tron_address(private_key_hex)
print("TRON Address:", tron_address)
