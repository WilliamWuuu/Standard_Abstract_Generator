import os

keywords = ["目次", "前言", "引言", "范围", "标准名称", "规范性引用文件", "术语和定义", "代号和缩略语", "核心技术要素", "附录", "参考文献"]

def part_extract(filepath, keyword):
    # 读取文件
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # 创建一个列表，用来记录提取片段的首尾
    split_points = []
    # 用以记录是否找到keyword
    keyflag = False
    
    # keyword为“目次”的情况需单独讨论
    if keyword == "目次":
        for i, line in enumerate(lines):
            # 找到关键词
            if keyword in line:
                split_points.append(i)
                keyflag = True
            # 已经找到首尾断点
            elif len(split_points) == 2:
                break
            # 遍历到文档的最后一行也没有找到keyword
            elif keyflag == False and i == len(lines) - 1:
                break
            # 
            elif keyflag == True:
                # 笔者将"."作为判断是否为目录行的依据
                if "." not in line:
                    split_points.append(i)
        # 如果文章有目次部分
        if keyflag == True:
            keypart = lines[split_points[0]:split_points[1]]
            keypart = '\n'.join(keypart)
        # 否则输出空字符串
        else:
            keypart = ""           
    
    # keyword为除“目次”的其他关键词时
    else:
        # 用以记录是否找到需求部分的末尾
        endflag = True
        
        for i, line in enumerate(lines):
            # 若在非目录行中找到keyword
            if keyword in line and "." not in line and len(line) > len(keyword) and (line[0:len(keyword)] == keyword or line[-len(keyword)-1:-1] == keyword):
                split_points.append(i)
                keyflag = True
            # 已找到首尾断点
            elif len(split_points) == 2:
                break
            # 由于处于文档末尾，只能找到首断点
            elif len(split_points) ==1 and i == len(lines) - 1:
                endflag = False
                break
            #
            elif keyflag == True:
                # 遍历关键词集合，判断是否有关键词落在该行中
                for key in keywords:
                    if key in line and key != keyword and len(line) > len(key) and (line[0:len(key)] == key or line[-len(key)-1:-1] == key):
                        split_points.append(i)
                        break
        
        if keyflag == False:
            keypart = ""
        elif endflag == False:
            keypart = lines[split_points[0]:]
            keypart = '\n'.join(keypart)
        else:
            keypart = lines[split_points[0]:split_points[1]]
            keypart = '\n'.join(keypart)            
                
    return keypart    
      
# 存放pdf文件的绝对路径
txt_path = '/Users/wyx/Desktop/Python Files/web/results'
# 存放txt文件的绝对路径
preface_path = '/Users/wyx/Desktop/Python Files/web/prefaces'

# 遍历文件夹中的文件
for filename in os.listdir(txt_path):
    file_path = os.path.join(txt_path, filename)
    preface = part_extract(file_path, "目次")   # 示例

    new_file_path = os.path.join(preface_path, filename)
    
    # 写入操作后的结果到新文件中
    with open(new_file_path, 'w') as new_file:
        new_file.write(preface)
        print(f"已将提取后的结果写入文件：{new_file_path}")  


