import os
import pypdf

def pdf_to_text(pdf_file):
    """将PDF文件转成txt文本"""
    # 读取pdf文件
    pdf_reader = pypdf.PdfReader(pdf_file)
    # 获取pdf文件页数
    page_num = len(pdf_reader.pages)
    # 遍历每一页
    text = ''
    for i in range(page_num):
        # 获取每一页的文本内容
        page_object = pdf_reader.pages[i]
        text += page_object.extract_text()
    return text

# 此处应为源PDF文件的父目录的绝对路径（可视情况该用相对路径）
os.chdir("/Users/wyx/Desktop/files")   
# 此处应为生成txt文件的父目录的绝对路径（可视情况改用相对路径）
os.mkdir("text")   

# 遍历指定文件夹下的所有文件
for filename in os.listdir("documents"):
    print(f"\n{filename}", end="")
    
    text = pdf_to_text(f"documents/{filename}")
    with open(f"text/{filename}.txt", "w") as file:
        file.write(text)
        count = text.count("G")
    # 以"G"的个数来判定转换后的txt文本是否为无效文件   
    if (count > 1000):
        os.remove(f"documents/{filename}")
        os.remove(f"text/{filename}.txt")
        print("\t\tDeleted", end="")

print("\n")
