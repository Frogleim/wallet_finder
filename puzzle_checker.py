import os
import time
# Wallet address to search for
wallet_address_to_find = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

# Directory to check the files
input_dir = "output_keys"

# Function to check each file and remove the ones without the address
def check_files_and_clean_up(directory, address):
    files_to_keep = []
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                lines = file.readlines()
                found = False
                for line_number, line in enumerate(lines, start=1):
                    if address in line:
                        print(f"Address found in file: {filename}, line: {line_number}")
                        files_to_keep.append(filepath)
                        found = True
                        break
                if not found:
                    print(f"Address not found in file: {filename}")
    
    # Remove files that do not contain the address
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath not in files_to_keep:
            os.remove(filepath)
            print(f"Removed file: {filename}")

# Run the function
if __name__ == '__main__':
    while True:
        check_files_and_clean_up(input_dir, wallet_address_to_find)
        time.sleep(5)