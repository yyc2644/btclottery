from eth_account import Account
from web3 import Web3

def generate_private_key():
    account = Account.create()
    private_key = account._private_key.hex()
    return private_key

def private_key_to_address(private_key):
    account = Account.from_key(private_key)
    address = account.address.lower()  # Convert address to lowercase
    return address

def increment_hex(hex_string):
    hex_int = int(hex_string, 16)
    incremented_int = (hex_int + 1) % (2 ** 256)  # Ensure the integer stays within 256 bits
    return format(incremented_int, '064x')

def generate_adjacent_private_keys(private_key, count):
    private_keys = []
    current_private_key = private_key
    for _ in range(count):
        current_private_key = increment_hex(current_private_key)
        private_keys.append(current_private_key)
    return private_keys

def generate_adjacent_addresses(private_key, count):
    adjacent_private_keys = generate_adjacent_private_keys(private_key, count)
    addresses = [private_key_to_address(key) for key in adjacent_private_keys]
    return addresses

# 连接到以太坊网络（使用公共 RPC 节点）
w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))

def get_eth_balance(address):
    # 将地址转换为 checksum 格式
    address = w3.to_checksum_address(address)
    # 查询地址的余额（单位：wei）
    balance_wei = w3.eth.get_balance(address)
    # 将余额转换为以太币
    balance_eth = w3.from_wei(balance_wei, 'ether')
    return balance_wei

def read_addresses_from_file(input_file):
    addresses = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(",")
            private_key = parts[0].split(": ")[1].strip()
            address = parts[1].split(": ")[1].strip()
            addresses.append((private_key, address))
    return addresses

def save_balances_to_file(address, private_key, balance):
    with open("balances.txt", 'a') as file:
        file.write(f"private_key: {private_key},Address: {address}, Balance: {balance} Wei\n")

if __name__ == "__main__":

    private_key = generate_private_key()
    # private_key = input("请输入私钥：")
    print(private_key)

    adjacent_private_keys = generate_adjacent_private_keys(private_key, 1000)

    balances = {}

    for index, key in enumerate(adjacent_private_keys):
        address = private_key_to_address(key)
        balance = get_eth_balance(address)
        print(index)
        if balance > 0:
            balances[address] = balance
            print(f"发现有金额的地址：{address}，私钥：{key}，余额：{balance} Wei")
            # 保存有金额的地址和余额到文件
            save_balances_to_file(address, key, balance)
    print("查询完成,没有发现余额。")