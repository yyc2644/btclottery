import torch
from bitcoin import privtopub, pubtoaddr

# 检查是否支持 MPS（Apple GPU 后端）
device = torch.device('mps' if torch.backends.mps.is_built() else 'cpu')
print(f"Using device: {device}")


# 生成随机256位私钥的函数
def generate_private_key():
    return ''.join(['%02x' % x for x in torch.randint(0, 256, (32,), dtype=torch.uint8).tolist()])


# 随机生成私钥并利用 GPU 生成比特币地址
def generate_bitcoin_address_on_gpu():
    # 生成随机的私钥
    private_key_hex = generate_private_key()

    # 生成公钥
    public_key = privtopub(private_key_hex)

    # 生成比特币地址
    address = pubtoaddr(public_key)

    return private_key_hex, address


# 生成一个比特币地址
private_key, address = generate_bitcoin_address_on_gpu()
print(f"Private Key: {private_key}")
print(f"Bitcoin Address: {address}")