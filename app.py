from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DADOS_PATH = os.path.join('static', 'dados.json')

DADOS_VAZIOS = {
    "chamada_atual": {},
    "ultima_chamada": {}
}

@app.route('/')
def painel():
    return render_template('painel.html')

@app.route('/controle')
def controle():
    return render_template('controle.html')

@app.route('/dados', methods=['GET'])
def get_dados():
    if os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, 'r') as f:
            return jsonify(json.load(f))
    return jsonify(DADOS_VAZIOS)

@app.route('/dados', methods=['POST'])
def atualizar_dados():
    novos_dados = request.get_json()

    dados_atuais = DADOS_VAZIOS
    if os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, 'r') as f:
            dados_atuais = json.load(f)

    dados_salvar = {
        "chamada_atual": novos_dados,
        "ultima_chamada": dados_atuais.get("chamada_atual", {})
    }

    with open(DADOS_PATH, 'w') as f:
        json.dump(dados_salvar, f, indent=2, ensure_ascii=False)

    return jsonify({'status': 'ok'})

@app.route('/limpar', methods=['POST'])
def limpar_dados():
    try:
        with open(DADOS_PATH, 'w') as f:
            json.dump(DADOS_VAZIOS, f, indent=2, ensure_ascii=False)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
