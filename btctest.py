import os
import ecdsa
import hashlib
import base58
import requests
from tqdm import tqdm
import threading
from functools import wraps
import time

STOP_GENERATION = threading.Event()

def multithreaded(num_threads):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            threads = []
            for _ in range(num_threads):
                t = threading.Thread(target=func, args=args, kwargs=kwargs)
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        return wrapper
    return decorator

def retry(num_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Retry {num_retries - _} failed:", e)
                    time.sleep(delay)
            raise Exception("Max retries reached. Unable to execute function.")
        return wrapper
    return decorator

@multithreaded(num_threads=8)
def process_address():
    global STOP_GENERATION
    while not STOP_GENERATION.is_set():
        key_pairs = generate_key_pairs(10)  # 一次生成10个地址
        for private_key, address in key_pairs:
            balance = get_address_info(address)
            if balance is not None and balance > 0:
                print("Private Key:", private_key)
                print("Address:", address)
                print("Balance:", balance, "BTC")
                with open("addresses_with_balance.txt", "a") as file:
                    file.write(f"Private Key: {private_key}\nAddress: {address}\nBalance: {balance} BTC\n\n")
                STOP_GENERATION.set()  # Set the event to stop generation
                return
            else:
                pbar.update(1)

# @retry(num_retries=3, delay=1)
def generate_key_pairs(num_pairs):
    key_pairs = []
    for _ in range(num_pairs):
        # 生成私钥
        private_key = os.urandom(32).hex()

        # 根据私钥生成公钥
        signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        public_key = bytes.fromhex("04") + verifying_key.to_string()

        # 计算公钥的哈希值
        sha256_hash = hashlib.sha256(public_key)
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash.digest()).digest()

        # 添加版本号并计算校验和
        extended_hash = b"\x00" + ripemd160_hash
        checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
        binary_address = extended_hash + checksum

        # 生成比特币地址
        bitcoin_address = base58.b58encode(binary_address).decode('utf-8')
        key_pairs.append((private_key, bitcoin_address))
    return key_pairs

@retry(num_retries=3, delay=1)
def get_address_info(address):
    # 查询地址信息
    url = f"https://blockstream.info/api/address/{address}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    data = response.json()
    balance = data['chain_stats']['funded_txo_sum'] + data['mempool_stats']['funded_txo_sum']
    return balance

if __name__ == "__main__":
    total_addresses = 100000  # 设置要生成的地址总数
    pbar = tqdm(total=total_addresses, desc='Progress')
    process_address()
    pbar.close()
