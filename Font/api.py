#api.py需放在远程服务器
from VectorDatabase import VectorDatabase
import torch 
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

#加载模型和tokenizer 路径可修改
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "/mnt/home/user14/weixuchen/models/Auto_Standard_Generator_v2.0"
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path)
database = VectorDatabase('VectorDatabase/vectorDB.db', 64)


#初始化Flask应用
app = Flask(__name__)

#定义API路由
@app.route('/generate', methods=['POST'])
def generate():
    try:
        #获取前端传递的输入与选择的功能
        data = request.json
        function_type = data.get('function')
        

        if not function_type:
            return jsonify({'error': 'No function specified'}), 400
        
        #根据function_type选择处理方式

        #生成摘要
        if function_type == 'summary':
            keyword = data.get('keyword')
            if not keyword:
                return jsonify({'error': 'Keyword is missing'}), 400
            input_text = f"instruction: 基于以下标准化文档的关键词，生成对应标准化文档的摘要。\ninput:{keyword} \noutput:"
            
            #调用模型生成结果
            inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
            outputs = model.generate(inputs['input_ids'], max_length=2048)  #设置max_length为生成长度
            
            #解码生成的结果
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            #删去输入"input:" 和 "output:" 部分
            if "output:" in generated_text:
                generated_text = generated_text.split("output:")[-1].strip()
            
            #返回响应
            return jsonify({'generated_text': generated_text})


        #生成全文
        elif function_type == 'full_text':
            full_text_part = ['前言', '范围', '规范性引用文件', '术语和定义', '附录', '参考文献']
            keyword = data.get('keyword')
            summary = data.get('summary')
            if not keyword or not summary:
                return jsonify({'error': 'Keyword or Summary is missing'}), 400
            
            # vdb
            search_result = database.search_vector(summary, k=5)

            # Judge the closest result by its distance to the query.
            # If it is closest enough, use the standard text corresponding file_path
            for result in search_result:
                valid = False
                if result["distance"] < 1e-5:
                    file_path = result["file_path"]
                
                    if file_path.endswith(".txt"):
                        valid = True

                        with open(file_path, 'r', encoding='utf-8') as file:
                            text = file.read()

                        break

            if valid == True:
                # Just return text
                return jsonify({'generated_text': text})
            else:
                # Deliver the user message to large language model and you know what to do.
            
            #循环调用模型生成各部分结果
                for part in full_text_part:                
                    input_text = f"instruction: 基于以下标准化文档的关键词和摘要，生成对应标准化文档的{part}。\ninput:\n关键词：{keyword} \n摘要：{summary} \noutput:"
                    
                    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
                    outputs = model.generate(inputs['input_ids'], max_length=8192)  #设置max_length为生成长度
                    
                    #解码生成的结果
                    original_generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

                    #删去输入"input:" 和 "output:" 部分
                    if "output:" in original_generated_text:
                        original_generated_text = original_generated_text.split("output:")[-1].strip()
                    
                    generated_text = generated_text + original_generated_text
                
                
                #返回响应
                return jsonify({'generated_text': generated_text})

        
        
        else:
            return jsonify({'error': 'Invalid function type'}), 400
        

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print(f"当前模型运行在设备 {model.device} 上")
    app.run(host='0.0.0.0', port=1234)  #设置服务器运行在6000端口

