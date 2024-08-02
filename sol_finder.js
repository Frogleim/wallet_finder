const nacl = require('tweetnacl');
const bs58 = require('bs58');

// Function to generate a Solana keypair from a given private key
function generateKeypair(privateKey) {
    const privateKeyUint8Array = new Uint8Array(32).fill(0);
    privateKeyUint8Array.set(privateKey, 32 - privateKey.length);
    const keypair = nacl.sign.keyPair.fromSeed(privateKeyUint8Array);
    return keypair;
}

// Function to convert a Uint8Array to a hex string
function uint8ArrayToHexString(uint8Array) {
    return Array.prototype.map.call(uint8Array, x => ('00' + x.toString(16)).slice(-2)).join('');
}

// Function to find Solana private keys in the range 1 to 0x3ff
function findSolanaPrivateKeysInRange(start, end) {
    for (let i = start; i <= end; i++) {
        const privateKey = Uint8Array.from(Buffer.from(i.toString(16).padStart(64, '0'), 'hex'));
        const keypair = generateKeypair(privateKey);

        console.log(`Private Key: ${uint8ArrayToHexString(privateKey)}`);
    }
}

// Define the range
const startRange = 20000000000000000;
const endRange = 0x3ffffffffffffffff;

// Find Solana private keys in the defined range
findSolanaPrivateKeysInRange(startRange, endRange);
