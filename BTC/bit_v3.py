from tqdm import tqdm
import threading
from functools import wraps
import time
from generate_key_pairs import generate_key_pairs
generate_key_pairs = generate_key_pairs(5,increment_count=100)

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

@multithreaded(num_threads=6)
def process_address():
    global STOP_GENERATION
    # 读取本地txt文件中的地址
    with open("new_file2.txt", "r") as file:
        local_addresses = file.readlines()
        local_addresses = [line.strip() for line in local_addresses]
    while not STOP_GENERATION.is_set():
        key_pairs = generate_key_pairs  # 一次生成10个地址
        for private_key, address in key_pairs:
            # 如果地址在本地文件中，则输出
            if address in local_addresses:
                print("Private Key:", private_key)
                print("Address:", address)
                print("Found in local addresses!")
                # STOP_GENERATION.set()  # 设置事件以停止生成
                with open("addresses_with_balance.txt", "a") as file:
                    file.write(f"Private Key: {private_key}\nAddress: {address} BTC\n\n")
            else:
                print("Address:", address)
                pbar.update(1)

# @retry(num_retries=3, delay=1)
# def generate_key_pairs(num_pairs):
#     key_pairs = []
#     for _ in range(num_pairs):
#         # 生成私钥
#         private_key = os.urandom(32).hex()
#
#         # 根据私钥生成公钥
#         signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
#         verifying_key = signing_key.get_verifying_key()
#         public_key = bytes.fromhex("04") + verifying_key.to_string()
#
#         # 计算公钥的哈希值
#         sha256_hash = hashlib.sha256(public_key)
#         ripemd160_hash = hashlib.new('ripemd160', sha256_hash.digest()).digest()
#
#         # 添加版本号并计算校验和
#         extended_hash = b"\x00" + ripemd160_hash
#         checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
#         binary_address = extended_hash + checksum
#
#         # 生成比特币地址
#         bitcoin_address = base58.b58encode(binary_address).decode('utf-8')
#         key_pairs.append((private_key, bitcoin_address))
#     return key_pairs

if __name__ == "__main__":
    total_addresses = 10000  # 设置要生成的地址总数
    pbar = tqdm(total=total_addresses, desc='Progress')
    process_address()
    pbar.close()
