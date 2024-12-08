from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#服务器ip
MODEl_URL = "http://10.249.44.55:1234/generate"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/full_text')
def full_text_page():
    return render_template('full_text.html')


@app.route('/summary')
def summary_page():
    return render_template('summary.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    selected_function = data.get('function')
    
    print(data)
    
    if selected_function == 'full_text':
        keyword = data.get('keyword')
        summary = data.get('summary')
        request_data = {'keyword': keyword, 'summary': summary, 'function':'full_text'}

    elif selected_function == 'summary':
        keyword = data.get('keyword')
        request_data = {'keyword': keyword, 'function':'summary'}
    else:
        return jsonify({'response': 'Error: Invalid function selected'})

    try:
        response = requests.post(MODEl_URL, json=request_data)
        response_data = response.json()
        
        model_response = response_data.get('generated_text', 'Error: No response from model')
        return jsonify({'response': model_response})
    
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)

