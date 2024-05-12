#清洗数据，从地址列表中，只获取对应的地址，保存
import pandas as pd

# # 读取原始文件
file_path = "All_Ethereum_Addresses_Latest.tsv"  # 替换成你的文件路径
df = pd.read_csv(file_path, sep='\t')
#
# # 只保留地址列，去掉balance列
cleaned_df = df[['address']]
#
# # 另存为一个新文件
cleaned_file_path = "cleaned_file.tsv"
cleaned_df.to_csv(cleaned_file_path, sep='\t', index=False)
#
# print("文件清洗完成，并另存为:", cleaned_file_path)


# 删除地址大于等于指定值的行
specified_address = '0xaafa3758a063a550cfb6ec14a897c2dda9f885c3'
cleaned_df = cleaned_df[cleaned_df['address'] < specified_address]


# 另存为一个新文件
cleaned_file_path = "eth_address.tsv"
cleaned_df.to_csv(cleaned_file_path, sep='\t', index=False)