import re
import os


'''def extract_after_section(file_path):
    # Read the text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Use regular expression to find the first and second occurrence of a section number
    match = re.finditer(r'\d术语和定义', text)
    first = next(match, None)
    second = next(match, None)

    # If the second section is found, extract text after it
    if second:
        after_section_text = text[second.start():]
        return after_section_text
    else:
        return None'''


def extract_between_section(file_path):
    # Read the text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Use regular expression to find the first occurrence of '附录' and '参考文献'
    fulu = re.search(r'\n附录A\b', text)
    cankao = re.search(r'参考文献', text)

    # If both '附录' and '参考文献' are found, extract text between them
    if fulu and cankao:
        between_section_text = text[fulu.start():cankao.start()]
        return between_section_text
    else:
        return None


# 获取目录中的所有文件列表
files = os.listdir('C:/MyCoding/DBtext_inter')

# 遍历文件列表
for filename in files:
    # 构建文件的绝对路径
    #file_path = os.path.join('C:/MyCoding/GB_text', filename)
    after_file_path = os.path.join('C:/MyCoding/DBtext_inter', f"{filename}")
    between_file_path = os.path.join('C:/MyCoding/DBtext_edit', f"{filename}")

    # Extract the second section
    '''after_text = extract_after_section(file_path)'''

    # Extract the text between '附录' and '参考文献'
    between_text = extract_between_section(after_file_path)

    # Print and save the second section and text between '附录' and '参考文献'
    '''if after_text:
        with open(after_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(after_text)
        print(f"已将文件 '{filename}' 第二个部分内容写入到新文件 '{after_file_path}'。")'''

    if between_text:
        with open(between_file_path, 'a', encoding='utf-8') as new_file2:
            #new_file.write("\n\n\n")
            new_file2.write(between_text)
        print(f"已将文件 '{filename}' 附录和参考文献之间内容写入到新文件 '{between_file_path}'。")
    else:
        print(f"文件 '{filename}' 没有第二个部分或者附录与参考文献之间没有内容，未创建新文件。")
