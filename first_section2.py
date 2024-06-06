import re
import os

def extract_first_section(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    match = re.finditer(r'\b\d[\u4e00-\u9fa5]+', text)

    match_count = 0

    # 遍历匹配项
    for sec in match:
        match_count += 1
        if match_count == 2:
            # Split the text based on the first occurrence of the section number
            first_section_text = text[:sec.start()]
            return first_section_text

    # Return 'deleted' 如果只有一个部分
    return 'deleted'


# 获取目录中的所有文件列表
files = os.listdir('C:/MyCoding/dataset/术语和定义')

# 遍历文件列表
for filename in files:
    # 构建文件的绝对路径
    file_path = os.path.join('C:/MyCoding/dataset/术语和定义', filename)
    new_file_path = os.path.join('C:/MyCoding/shuyu', f"{filename}")

    # Extract the first section
    first_section_text = extract_first_section(file_path)

    # Print and save the first section
    if first_section_text != 'deleted':
        # 将文件内容写入新文件
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(first_section_text)
        print(f"已将文件 '{filename}' 的第一部分写入到新文件 '{new_file_path}'。")
    else:
        print(f"文件 '{filename}' 没有第二个部分")