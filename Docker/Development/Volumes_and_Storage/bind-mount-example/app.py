from flask import Flask, request
import os

app = Flask(__name__)

DATA_DIR = '/app/data'
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/write', methods=['POST'])
def write_data():
    content = request.get_json().get('content', '')
    with open(f'{DATA_DIR}/data.txt', 'a') as f:
        f.write(content + '\n')
    return {'status': 'success'}

@app.route('/read')
def read_data():
    try:
        with open(f'{DATA_DIR}/data.txt', 'r') as f:
            return {'content': f.read()}
    except FileNotFoundError:
        return {'content': ''}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
