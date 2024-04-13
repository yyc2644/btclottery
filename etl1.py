# # 打开原始文件
# with open('/Users/yicheng/PycharmProjects/btclottery/new_file.txt', 'r') as f:
#     lines = f.readlines()
#
# # 创建新文件来存储符合条件的地址和 satoshis
# with open('new_file2.txt', 'w') as f:
#     for line in lines:
#         # 分割每行数据，以 ":" 为分隔符
#         parts = line.strip().split(':')
#         if len(parts) == 2:
#             address = parts[0].strip()
#             satoshis = parts[1].strip().split()[0]  # 提取 satoshis 部分
#             # 检查地址长度是否为 34 位
#             if len(address) == 34:
#                 f.write(f"{address}\n")
#
# print("Done! New file created with the desired addresses.")


import csv

input_file = "blockchair_bitcoin_addresses_and_balance_May_01_2023.tsv"
output_file = "new_file1.txt"

with open(input_file, "r", newline="") as file_in, open(output_file, "w") as file_out:
    tsv_reader = csv.reader(file_in, delimiter="\t")
    for row in tsv_reader:
        if row[0].startswith("1"):
            cleaned_row = row[0].split("\t")[0]
            file_out.write(cleaned_row + "\n")
