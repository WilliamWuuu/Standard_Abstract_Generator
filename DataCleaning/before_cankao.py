import re
import os

def extract_first_section(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    match = re.finditer(r'参考文献', text)
    first = next(match, None)

    if first:
        first_section_text = text[:first.start()]
        return first_section_text.strip()
    else:
        return text


# 获取目录中的所有文件列表
files = os.listdir('C:/MyCoding/DBtext_another')

# 遍历文件列表
for filename in files:
    # 构建文件的绝对路径
    file_path = os.path.join('C:/MyCoding/DBtext_another', filename)
    new_file_path = os.path.join('C:/MyCoding/DBtext_edit', f"{filename}")

    # Extract the first section
    first_section_text = extract_first_section(file_path)

    if first_section_text != None:
        # 将文件内容写入新文件
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(first_section_text)

        print(f"已将文件 '{filename}' 的内容写入到新文件 '{new_file_path}'。")