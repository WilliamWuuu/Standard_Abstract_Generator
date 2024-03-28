import os
import PyPDF2
from PyPDF2.errors import PdfReadError

def pdf_to_text(pdf_file):
    """将PDF文件转成txt文本"""
    try:
        text = ''
        with open(pdf_file, "rb") as pdf_file:
            # 读取pdf文件
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # 获取pdf文件页数
            page_num = len(pdf_reader.pages)
            # 遍历每一页
            for i in range(page_num):
                # 获取每一页的文本内容
                page_object = pdf_reader.pages[i]
                try:
                    # 提取文本并追加到结果中
                    text += page_object.extract_text()
                except UnicodeEncodeError:
                    # 在遇到编码错误时跳过当前文件
                    print(f"UnicodeEncodeError: Skipping file {pdf_file.name}")
                    break
        return text
    except PdfReadError as e:
        print(f"Error reading PDF: {e}")
        return None

# 存放pdf文件的绝对路径
pdf_path = '/Users/wyx/Desktop/Python_Files/web/pdf_files'
# 存放txt文件的绝对路径
txt_path = '/Users/wyx/Desktop/Python_Files/web/text_files'

# 遍历文件夹中的文件
for filename in os.listdir(pdf_path):
    file_path = os.path.join(pdf_path, filename)
    text = pdf_to_text(file_path)
    
    if text:
        count = text.count("G")
        if count < 1000:
            # 定义新文件名
            new_filename = f"{filename}.txt"
            new_file_path = os.path.join(txt_path, new_filename)
            
            text = text.replace(' ', '')
            # 写入操作后的结果到新文件中
            with open(new_file_path, 'w', encoding='utf-8', errors='replace') as new_file:
                new_file.write(text)
                print(f"已将转换后的结果写入文件：{new_file_path}")
                
    else:
        print("提取文本过程遇到错误")
