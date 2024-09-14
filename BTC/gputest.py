'''
不要使用GPU！！！！！
GPU只能加速生成私钥的部份，计算公钥和地址的部份，不能加速，所以实测下来，还不如CPU！ss
'''
import time
import torch
from bitcoin import privkey_to_pubkey, pubkey_to_address,compress

# 设置设备为 MPS（适用于 M1/M2 芯片），如果没有 MPS 后端可用，则使用 CPU
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
print(device)

# 生成压缩地址的方法
def generate_compressed_address(private_key):
    # 生成压缩格式的公钥
    compressed_public_key = compress(privkey_to_pubkey(private_key))
    # 生成比特币地址
    compressed_address = pubkey_to_address(compressed_public_key)
    return compressed_public_key, compressed_address

# 范围内的私钥生成器
def generate_private_keys(start, end):
    # return torch.arange(start, end, device=device, dtype=torch.float32)
    return [int(k) for k in range(start, end)]

# 计算并匹配比特币地址
def find_matching_address(start, end, target_address):
    private_keys = generate_private_keys(start, end)
    # print(private_keys)
    for private_key in private_keys:
        private_key = format(private_key, 'x').zfill(64)
        # print(private_key)
        # 将私钥转换为十六进制字符串格式
        # private_key_hex = hex(private_key.item())[2:]
        # print(private_key_hex)
        # 生成公钥
        pubkey = generate_compressed_address(private_key)
        # print(pubkey)
        # 生成比特币地址
    #     address = pubkey_to_address(pubkey)
        if pubkey[1] == target_address:
            print(private_key, pubkey)
            return private_key, pubkey
    return None, None

if __name__ == "__main__":
    # 文件地址
    default_output_file = "balances.txt"

    # 示例输入：私钥范围和目标地址
    start_time = time.time()

    start_key = 71181701183000000000
    end_key =   71181701183000100000  # 范围可以调整
    test_start_key = 1
    test_end_key = 100000
    test_target_address = '1ErZWg5cFCe4Vw5BzgfzB74VNLaXEiEkhk'  # 替换为你的目标地址
    address66 = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

    # generate_private_keys(start_key,end_key)
    # 在范围内查找匹配的比特币地址
    matching_key, matching_address = find_matching_address(start_key, end_key, test_target_address)
    #
    if matching_key is not None:
        print(f"匹配的私钥: {matching_key}")
        print(f"生成的比特币地址: {matching_address}")
        with open(default_output_file, 'a') as file:
            file.write(f"{start_key},{end_key}private_key: {matching_key}, Address: {matching_address}\n")
    else:
        print("未找到匹配的地址。")
        with open(default_output_file, 'a') as file:
            file.write(f"{start_key}-{end_key}没有找到匹配的地址。\n")

    end_time = time.time()
    total_addresses_generated = (end_key - start_key + 1)
    elapsed_time_minutes = (end_time - start_time) / 60
    addresses_per_minute = total_addresses_generated / elapsed_time_minutes
    print(f"运行时间: {elapsed_time_minutes} 分钟,运行条数: {total_addresses_generated},每分钟生成的地址数量: {addresses_per_minute:.2f}")
