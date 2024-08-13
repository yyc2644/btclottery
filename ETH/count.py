def count_eth_addresses(filename):
    addresses = {}
    with open(filename, 'r') as file:
        for line in file:
            address = line.strip()
            prefix = address[36:]
            if prefix not in addresses:
                addresses[prefix] = 1
            else:
                addresses[prefix] += 1

    sorted_addresses = sorted(addresses.items(), key=lambda x: x[1], reverse=False)

    for prefix, count in sorted_addresses:
        print(f"前6位为 {prefix} 的地址数量为 {count}")


if __name__ == "__main__":
    # filename = input("请输入包含以太坊地址的文本文件名：")
    filename = r"eth_address.txt"
    count_eth_addresses(filename)
