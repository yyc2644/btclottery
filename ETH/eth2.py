import multiprocessing
from eth_account import Account
import tqdm

def generate_ethereum_addresses(batch_size):
    # Generate a batch of Ethereum private keys and addresses
    accounts = [Account.create() for _ in range(batch_size)]
    private_keys = [account._private_key.hex() for account in accounts]
    # Convert addresses to lowercase
    addresses = [account.address.lower() for account in accounts]
    return private_keys, addresses

def read_local_address_list(filename):
    # Read local address list from a text file
    with open(filename, 'r') as file:
        local_address_list = [line.strip() for line in file.readlines()]
    return local_address_list

def match_local_address(addresses, local_address_list):
    # Match generated addresses with local address list
    matched_addresses = [address for address in addresses if address in local_address_list]
    return matched_addresses

def save_matched_addresses(private_keys, addresses):
    # Save matched private keys and addresses to a file
    with open("private_keys_and_addresses.txt", 'a') as file:
        for private_key, address in zip(private_keys, addresses):
            file.write(f"Private Key: {private_key}, Address: {address}\n")

def main(local_address_filename, batch_size, num_processes):
    local_address_list = read_local_address_list(local_address_filename)
    pool = multiprocessing.Pool(processes=num_processes)
    with tqdm.tqdm() as pbar:
        while True:
            private_keys, addresses = generate_ethereum_addresses(batch_size)
            matched_addresses = pool.apply(match_local_address, args=(addresses, local_address_list))
            save_matched_addresses(private_keys, matched_addresses)
            pbar.update(1)

if __name__ == "__main__":
    local_address_filename = "eth_address.txt"  # Path to the text file containing local addresses
    batch_size = 1000  # Number of addresses to generate in each batch
    num_processes = 4  # Number of processes to use
    main(local_address_filename, batch_size, num_processes)
