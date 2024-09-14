import bitcoin
import time
import argparse
import asyncio
import aiofiles
from concurrent.futures import ProcessPoolExecutor

# 配置类，用于封装参数
class Config:
    def __init__(self, start, end, target_address, output_file):
        self.start = start
        self.end = end
        self.target_address = target_address
        self.output_file = output_file

# 生成压缩地址的方法
def generate_compressed_address(private_key):
    compressed_public_key = bitcoin.compress(bitcoin.privkey_to_pubkey(private_key))
    compressed_address = bitcoin.pubkey_to_address(compressed_public_key)
    return compressed_public_key, compressed_address

# 生成指定范围内的数字
def generate_numbers(start=2**65, end=2**66):
    current = start
    while current <= end:
        yield current
        current += 1

# 进程池中的 worker 函数，不是协程函数
def worker(start, end, target_address):
    found = None
    for number in generate_numbers(start, end):
        private_key = format(number, 'x').zfill(64)
        addr = generate_compressed_address(private_key)[1]
        if addr == target_address or "1YangA" in addr:
            print(addr)
            found = (private_key, addr)
            break
        elif "1YangA" in addr:
            print(private_key, addr)
    return found

async def process_results(futures, config):
    match_found = False
    for future in asyncio.as_completed(futures):
        result = await future
        if result is not None:
            private_key, addr = result
            print("找到匹配的地址!", private_key, addr)
            match_found = True
            async with aiofiles.open(config.output_file, 'a') as file:
                await file.write(f"{config.start},{config.end} private_key: {private_key}, Address: {addr}\n")
            break

    if not match_found:
        async with aiofiles.open(config.output_file, 'a') as file:
            await file.write(f"{config.start}-{config.end} 没有找到匹配的地址。\n")

async def main(config):
    start_time = time.time()

    num_processes = 4  # 根据需要调整进程数
    chunk_size = (config.end - config.start) // num_processes
    loop = asyncio.get_event_loop()

    # 使用进程池执行多进程
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [
            loop.run_in_executor(executor, worker, config.start + i * chunk_size,
                                 config.start + (i + 1) * chunk_size - 1 if i != num_processes - 1 else config.end,
                                 config.target_address)
            for i in range(num_processes)
        ]

        # 处理结果
        await process_results(futures, config)

    end_time = time.time()
    print(f"总执行时间: {end_time - start_time:.2f} 秒")

    # 打印每分钟执行的量
    total_addresses_generated = (config.end - config.start + 1)
    elapsed_time_minutes = (end_time - start_time) / 60
    addresses_per_minute = total_addresses_generated / elapsed_time_minutes
    print(f"每分钟生成的地址数量: {addresses_per_minute:.2f}")

if __name__ == "__main__":
    # 设置默认参数
    default_start = 71181701188000100000
    default_end = 71181701188000200000
    default_target_address = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
    default_output_file = "balances.txt"

    parser = argparse.ArgumentParser(description='Bitcoin 地址生成器')
    parser.add_argument('--start', type=int, help='私钥范围的起始值')
    parser.add_argument('--end', type=int, help='私钥范围的结束值')
    parser.add_argument('--target_address', type=str, help='目标比特币地址')
    parser.add_argument('--output_file', type=str, help='输出匹配结果的文件')

    args = parser.parse_args()

    # 使用命令行参数，如果未提供则使用默认值
    config = Config(
        start=args.start if args.start is not None else default_start,
        end=args.end if args.end is not None else default_end,
        target_address=args.target_address if args.target_address is not None else default_target_address,
        output_file=args.output_file if args.output_file is not None else default_output_file
    )

    # 运行主协程
    asyncio.run(main(config))