import os

def count_chinese_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            chinese_words = [char for char in content if '\u4e00' <= char <= '\u9fff']
            return len(chinese_words)
    except Exception as e:
        print(f"Error counting Chinese words in {file_path}: {e}")
        return -1

def delete_files_less_than_10_chinese_words(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            chinese_word_count = count_chinese_words(file_path)
            if chinese_word_count < 10 and chinese_word_count != -1:
                os.remove(file_path)
                print(f"Deleted {file_path}")

# 替换为你的文件夹路径
folder_path = 'C:/MyCoding/dataset/参考文献'
delete_files_less_than_10_chinese_words(folder_path)