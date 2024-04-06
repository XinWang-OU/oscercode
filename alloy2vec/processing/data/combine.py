import pandas as pd
import os

x_path ='/home/eticaoffice/Updateddata/No1999-2018'

# 创建一个空列表用于存储数据
data = []

# 遍历每个文件
for file in os.listdir(x_path):
    # 拼接完整的文件路径
    p = os.path.join(x_path, file)
    # 读取文件内容
    with open(p, 'r', encoding='utf-8') as f:
        # 将文件内容和类别（文件名）作为字典添加到列表
        data.append({'text': f.read(), 'class': file})

# 一次性将列表转换为DataFrame
df = pd.DataFrame(data)

# 保存DataFrame到文本文件
output_file = '/home/eticaoffice/Updateddata/No1999-2018/combined_text.txt'  # 替换为您希望保存文件的路径
df.to_csv(output_file, sep='\t', index=False, header=False)