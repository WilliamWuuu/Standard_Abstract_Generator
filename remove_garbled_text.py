import os
import re

def contains_garbage(text,filename):
    if re.search(r'书{3,}', text):
        return True
    if text.count('!') > 50:
        return True
    invalid_chars = set('ºÓÊ¡µØêÐÏÄÉÀÑÔìÎùÕñåÌá¶Å3ÁîÍãÖÆçÃË')
    if any(char in invalid_chars for char in filename):
        return True
    return False

def delete_files_with_garbage(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file_size = os.path.getsize(filepath)
        if file_size < 1024:
            os.remove(filepath)
            print(f"Deleted {filename} (size: {file_size} bytes)")
            continue
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            if contains_garbage(text,filename):
                os.remove(filepath)
                print(f"Deleted {filename} (contains garbage)")

    
if __name__ == "__main__":
    directory_path = "~/Path"
    delete_files_with_garbage(directory_path)
