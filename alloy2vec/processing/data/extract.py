# 定义文件路径
input_file_path = '/home/eticaoffice/Updateddata/No1999-2018/combined_text.txt'

# 创建一个空列表用于存储处理后的数据
processed_data = []

# 读取并处理文件
with open(input_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        columns = line.split('\t')
        if len(columns) >= 34:
            # 如果列数大于等于34，则保留第10和第34列
            title = columns[9]  # 第10列
            abstract = columns[33]  # 第34列
            combined_text = title + ". " + abstract
        elif len(columns) >= 10:
            # 否则，只保留第10列
            combined_text = columns[9]  # 第10列
        else:
            continue  # 如果不满足以上条件，则跳过这一行
        processed_data.append(combined_text)

# 定义输出文件的路径
output_file_path = '/home/eticaoffice/Updateddata/No1999-2018/extracted_text.txt'

# 将处理后的数据保存到新文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for item in processed_data:
        output_file.write(item + '\n')
