def extract_lines(input_file, output_file, num_lines=1000000):
    with open(input_file, 'r', encoding='utf-8') as f_in:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for i, line in enumerate(f_in):
                if i >= num_lines:
                    break
                f_out.write(line)

input_file = "eth_address.tsv"  # 输入文件名
output_file = "eth_address.txt"  # 输出文件名
extract_lines(input_file, output_file)
