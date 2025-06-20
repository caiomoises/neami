from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

DADOS_PATH = os.path.join('static', 'dados.json')

@app.route('/')
def painel():
    return render_template('painel.html')

@app.route('/controle')
def controle():
    return render_template('controle.html')

@app.route('/dados')
def get_dados():
    with open(DADOS_PATH, 'r') as f:
        return jsonify(json.load(f))

@app.route('/dados', methods=['POST'])
def atualizar_dados():
    data = request.get_json()
    with open(DADOS_PATH, 'w') as f:
        json.dump(data, f)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)