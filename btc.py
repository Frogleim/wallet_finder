import random
import hashlib
import aiohttp
import asyncio
from termcolor import colored
from bip32utils import BIP32Key
from ecdsa import SigningKey, SECP256k1
import binascii
import base58  # Import base58 module
from pyfiglet import Figlet
import colorama
import requests  # Import requests module
import sys  # Import sys to use sys.stdout.flush()

def lolcat(text):
    fig = Figlet()
    banner = fig.renderText(text)

    lines = banner.split('\n')
    colored_lines = []

    colorama.init(autoreset=True)

    color_list = [colorama.Fore.CYAN, colorama.Fore.BLUE, colorama.Fore.GREEN,
                  colorama.Fore.MAGENTA, colorama.Fore.YELLOW, colorama.Fore.RED]

    selected_colors = random.sample(color_list, 2)

    for line in lines:
        gradient_line = ""
        for i in range(len(line)):
            ratio = i / len(line)
            current_color = selected_colors[0] if ratio <= 0.5 else selected_colors[1]
            gradient_line += "{}{}".format(current_color, line[i])
        colored_lines.append(gradient_line)

    colored_banner = '\n'.join(colored_lines)
    print(colored_banner)

def generate_private_key():
    # Generate a random private key
    private_key = binascii.hexlify(SigningKey.generate(curve=SECP256k1).to_string()).decode('utf-8')
    return private_key

def generate_BTC_address(private_key):
    # Get the public key from the private key
    sk = SigningKey.from_string(binascii.unhexlify(private_key), curve=SECP256k1)
    vk = sk.get_verifying_key()
    public_key = b'\x04' + vk.to_string()

    # Perform SHA-256 and RIPEMD-160 hashing to get the Bitcoin address
    sha256_bpk = hashlib.sha256(public_key).digest()
    ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()

    # Add network byte, perform double SHA-256, and get checksum
    network_byte = b'\x00'
    network_and_pubkey = network_byte + ripemd160_bpk
    sha256_1 = hashlib.sha256(network_and_pubkey).digest()
    sha256_2 = hashlib.sha256(sha256_1).digest()
    checksum = sha256_2[:4]

    # Form the final address and encode in Base58
    address = network_and_pubkey + checksum
    btc_address = base58.b58encode(address).decode('utf-8')
    return btc_address

async def check_balance_BTC(session, address):
    url = f"https://blockchain.info/rawaddr/{address}"
    async with session.get(url, ssl=False) as response:
        if response.status == 200:
            data = await response.json()
            if 'final_balance' in data:
                balance = data['final_balance'] / 100000000  # Convert from satoshis to BTC
                return balance
    return "0"

async def process_address(session, live_counter_list, dead_counter_list, total_btc_list):
    private_key = generate_private_key()
    BTC_address = generate_BTC_address(private_key)
    balance = await check_balance_BTC(session, BTC_address)

    if balance is not None:
        if balance != "0":
            live_counter_list[0] += 1
            total_btc_list[0] += balance  # Add the balance to the total BTC found

            # Save live account details to a file
            with open("live_accounts.txt", "a") as f:
                f.write(f'{BTC_address} | PRIVATE KEY: {private_key} | BALANCE: {balance:.6f} BTC\n')

        else:
            dead_counter_list[0] += 1

async def main():
    num_threads = 5  # Adjust as needed
    live_counter_list = [0]  # Using a list to make it mutable
    dead_counter_list = [0]  # Using a list to make it mutable
    total_btc_list = [0.0]   # Track the total BTC found

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [process_address(session, live_counter_list, dead_counter_list, total_btc_list) for _ in range(num_threads)]
            await asyncio.gather(*tasks)

            # Print summary in the console in one line
            print(f'Total DEAD accounts: {dead_counter_list[0]} | Total LIVE accounts: {live_counter_list[0]} | Total BTC found: {total_btc_list[0]:.6f}', end='\r')
            sys.stdout.flush()  # Ensure the output is flushed to the console

if __name__ == "__main__":
    lolcat("TKKYTRS")
    asyncio.run(main())
