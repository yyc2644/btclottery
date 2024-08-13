# 1
test = "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"
# 66
address66 = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
# 67
address67 = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
# 生成地址的方法
import bitcoin
from random import randint
import time



def generate_compressed_address(private_key):
    # 从私钥生成压缩公钥
    compressed_public_key = bitcoin.privkey_to_pubkey(private_key)
    # 生成压缩地址
    compressed_address = bitcoin.pubkey_to_address(compressed_public_key, 0)
    return compressed_public_key, compressed_address


def generate_random_private_key():
    # 生成随机数作为私钥
    private_key_hex = format(randint(2 ** 65, 2 ** 66), 'x')
    # print(private_key_hex)
    # 补零至64位长度
    private_key_hex = private_key_hex.zfill(64)
    # print(private_key_hex)
    return private_key_hex

# 指定范围按顺序生成
# 生成器函数
def generate_numbers(start = 61181701178000000000, end = 73786976294838206463):
    current = start
    while current <= end:
        yield current
        current += 1

def main(start,end = 73786976294838206463):
    start_time = time.time()
    addresses_generated = 0
    address = address66
    print(start,end,address)
    for number in generate_numbers(start = start,end = end):
        private_key = format(number, 'x').zfill(64)
        addr = generate_compressed_address(private_key)[1]
        # print(addr)
        if  addr == address:
            print("ok!", private_key, addr)
            with open("balances.txt", 'a') as file:
                file.write(f"private_key: {private_key},Address: {addr}")
            break
        addresses_generated += 1
        current_time = time.time()
        if current_time - start_time >= 60:
            print("Addresses generated in 1 min:", addresses_generated,"now",private_key)
            addresses_generated = 0
            start_time = current_time

if __name__ == "__main__":

    main(start = 62334622687178450000)
    # generate_numbers()
    # print((73786976294838206463-71181701177803410000) /1000000/30/24)