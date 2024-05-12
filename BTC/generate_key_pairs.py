import os
import hashlib
import ecdsa
import base58

def generate_key_pairs(num_pairs, increment_count=1):
    key_pairs = []
    for _ in range(num_pairs):
        # 生成私钥
        private_key = os.urandom(32).hex()

        for _ in range(increment_count + 1):
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

            # 生成下一个私钥
            private_key = hex(int(private_key, 16) + 1)[2:].zfill(64)

    return key_pairs


if __name__ == "__main__":
    # 生成5对私钥和比特币地址，每次增加2个私钥
    key_pairs = generate_key_pairs(10, increment_count=1000)
    for private_key, bitcoin_address in key_pairs:
        print("Private Key:", private_key)
        print("Bitcoin Address:", bitcoin_address)
        print()
