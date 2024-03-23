# @ILovAC 观察到经过转换后作为标题到关键词往往之间有空格（对空格数量仍然存在疑问）
# 若空格数量不一，则下述程序需进一步修改
keywords = {"目  次", "前  言", "引  言", "参 考 文 献", "附 录", " 标准名称", " 范围", " 规范性引用文件", " 术语和定义", " 代号和缩略语", " 核心技术要素"}
    
def text_split(input_file, output_file, keyword):
    """依据keyword进行文本提取"""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    # 初始化写入文本
    current_file = None
    
    # 由于”目次“中有大量关键词，需单独考虑
    if keyword == "目  次":
        for line in lines:
            if keyword in line:
                current_file = open(output_file, 'w')
            elif "前  言" in line:
                current_file.close()
            else:
                if current_file.closed == False:
                    current_file.write(line)
    
    else:
        for line in lines:
            if keyword in line and "." not in line:    # 判断该keyword不存在于目录中
                current_file = open(output_file, 'w')
            
            else:
                if current_file is not None:
                    # 寻找提取文本的末尾（以下一个标题为末尾）
                    for key in keywords and key != keyword:
                        if key in line:
                            current_file.close()
                    # 若未找到，则写入当前行
                    if current_file.closed == False:
                        current_file.write(line)

# 以下仅为示例
input_file = 'documents/test2.txt'
output_file = 'documents/text.txt'
keyword = '前  言'
text_split(input_file, output_file, keyword)
