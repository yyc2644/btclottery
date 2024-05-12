import tqdm
import multiprocessing
from eth_account import Account

def generate_ethereum_addresses(batch_size, num_batches):
    # 批处理生成一定数量的以太坊私钥和地址
    all_private_keys = []
    all_addresses = []
    for _ in range(num_batches):
        batch_accounts = [Account.create() for _ in range(batch_size)]
        private_keys = [account._private_key.hex() for account in batch_accounts]
        addresses = [account.address for account in batch_accounts]
        all_private_keys.extend(private_keys)
        all_addresses.extend(addresses)
    return all_private_keys, all_addresses

def read_local_address_set(filename):
    # 从文本文件中读取本地地址列表并转换为集合
    with open(filename, 'r') as file:
        local_address_list = {line.strip() for line in file.readlines()}
    return local_address_list

def match_local_addresses(addresses, local_address_set):
    # 将生成的地址与本地地址集合进行匹配
    matched_addresses = set(addresses) & local_address_set
    return matched_addresses

def save_matched_addresses(matched_addresses_with_keys):
    # 将匹配的地址、私钥和地址保存到文件中
    with open("matched_addresses_with_private_keys.txt", 'a') as file:
        for address, private_key in matched_addresses_with_keys:
            file.write(f"Address: {address}, Private Key: {private_key}\n")
        file.write("\n")

def main(local_address_filename, batch_size, num_batches, num_processes):
    local_address_set = read_local_address_set(local_address_filename)
    pool = multiprocessing.Pool(processes=num_processes)
    with tqdm.tqdm(total=num_batches) as pbar:
        for _ in range(num_batches):
            private_keys, addresses = generate_ethereum_addresses(batch_size, 1)
            matched_addresses = pool.apply(match_local_addresses, args=(addresses, local_address_set))
            if matched_addresses:
                matched_addresses_with_keys = [(address, private_keys[addresses.index(address)]) for address in matched_addresses]
                save_matched_addresses(matched_addresses_with_keys)
            pbar.update(1)

if __name__ == "__main__":
    local_address_filename = "eth_address.tsv"  # 包含本地地址的文本文件路径
    batch_size = 1000  # 每个批次生成的地址数量
    num_batches = 100  # 生成的批次数量
    num_processes = 4  # 使用的进程数
    main(local_address_filename, batch_size, num_batches, num_processes)