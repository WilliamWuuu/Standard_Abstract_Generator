from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#服务器ip
MODEl_URL = "http://10.249.44.91:5000/generate"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    #向服务器发送请求
    try:
        response = requests.post(MODEl_URL, json={'input': user_input})
        response_data = response.json()
        
        #从服务器获取模型的回答
        model_response = response_data.get('generated_text', 'Error: No response from model')
        
        return jsonify({'response': model_response})
    
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
