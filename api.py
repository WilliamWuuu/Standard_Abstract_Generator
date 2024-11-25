#api.py需放在远程服务器

from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

#加载模型和tokenizer 路径可修改
model = AutoModelForCausalLM.from_pretrained("/mnt/home/user14/weixuchen/models/Qwen2.5-7B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("/mnt/home/user14/weixuchen/models/Qwen2.5-7B-Instruct")

#初始化Flask应用
app = Flask(__name__)

#定义API路由
@app.route('/generate', methods=['POST'])
def generate():
    try:
        #获取前端传递的输入文本
        data = request.json
        input_text = data['input']
        
        #使用LLaMA模型生成结果
        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(inputs['input_ids'], max_length=200)  #设置max_length为生成长度
        
        #解码生成的结果
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        #返回响应
        return jsonify({'generated_text': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  #设置服务器运行在5000端口
