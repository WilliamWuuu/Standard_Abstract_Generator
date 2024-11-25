import os
import re

def remove_newlines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        content = re.sub(r'\n', '', content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def batch_remove_newlines(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, filename)
            remove_newlines(input_file, output_file)
            print(f'{filename} processed.')

if __name__ == "__main__":
    directory = '~/Path'
    batch_remove_newlines(directory)