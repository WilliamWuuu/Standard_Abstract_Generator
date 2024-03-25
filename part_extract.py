keywords = ["目次", "前言", "引言", "参考文献", "附录", "标准名称", 
            "范围", "规范性引用文件", "术语和定义", "代号和缩略语", "核心技术要素"]

def log_extract(filepath):
    """提取目次部分"""
    # 读取文件
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # 确定分割位置
    split_points = []
    # 判断是否已经找到目次起点
    logflag = False
    
    for i, line in enumerate(lines):
        if '目次' in line:
            split_points.append(i)
            logflag = True
        elif logflag == True:
            # 以“…”为依据判断当前行是否为目录
            if "…" not in line:
                split_points.append(i)
    
    # 提取指定部分
    log = []
    log = lines[split_points[0]:split_points[1]]
    # 将列表转换成字符串
    log = '\n'.join(log)
    
    return log


def part_extract(filepath, keyword):
    """提取由keyword指定的部分，不包括目次"""
    # 读取文件
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # 确定分割位置
    split_points = []
    keyflag = 0
    for i, line in enumerate(lines):
        if '目次' in line:
            split_points.append(i)
        elif keyword in line and (line[0:len(keyword)] == keyword or line[-len(keyword)-1:] == keyword):
            if i - split_points[-1] == 1 and len(split_points) > 1:
                split_points[-1] = i
            else:
                split_points.append(i)
                keyflag += 1
        elif keyflag == 2:
            for key in keywords:
                if (key in line) and (key != keyword) and (line[0:len(key)] == key or line[-len(key)-1:-1] == key):
                    split_points.append(i)
                    keyflag = 0
                    break
    
    # 提取指定部分
    keypart = []
    # 找到了结尾，即该部分位于文本中间
    if len(split_points) == 4:         
        start = split_points[2]
        end = split_points[3]
        keypart = lines[start:end]
    # 没找到结尾，即该部分位于文本最后
    elif len(split_points) == 3:
        start = split_points[2]
        keypart = lines[start:]    
    
    keypart = '\n'.join(keypart)
    return keypart


