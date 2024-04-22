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

def detect_files_with_garbage(directory):
    garbage_files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file_size = os.path.getsize(filepath)
        if file_size < 1024:
            garbage_files.append(filename)
            continue
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            if contains_garbage(text, filename):
                garbage_files.append(filename)
    return garbage_files

def delete_original_files_with_garbage(directory,garbage_files):
    for filename in garbage_files:
        filepath = os.path.join(directory, filename)
        os.remove(filepath)
        print(f"Deleted {filepath}")


if __name__ == "__main__":
    directory_path_original = "~/Path/to/original/files"
    directory_path_no_newlines = "~/Path/to/no/newlines/files"
    garbage_files = detect_files_with_garbage(directory_path_no_newlines)
    delete_original_files_with_garbage(directory_path_original,garbage_files)
