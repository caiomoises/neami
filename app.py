from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DADOS_PATH = os.path.join('static', 'dados.json')

DADOS_VAZIOS = {
    "chamadas": [],
    "ultima_atualizacao": None
}

MAX_CHAMADAS = 6  # Número máximo de chamadas a armazenar

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
            dados = json.load(f)
            # Ordena as chamadas por timestamp (mais recente primeiro)
            dados["chamadas"] = sorted(
                dados.get("chamadas", []),
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )
            return jsonify(dados)
    return jsonify(DADOS_VAZIOS)

@app.route('/dados', methods=['POST'])
def atualizar_dados():
    novos_dados = request.get_json()
    novos_dados['timestamp'] = datetime.now().isoformat()

    dados_atuais = DADOS_VAZIOS
    if os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, 'r') as f:
            dados_atuais = json.load(f)

    # Adiciona a nova chamada
    chamadas = dados_atuais.get("chamadas", [])
    chamadas.insert(0, novos_dados)
    
    # Mantém apenas as últimas MAX_CHAMADAS chamadas
    dados_salvar = {
        "chamadas": chamadas[:MAX_CHAMADAS],
        "ultima_atualizacao": datetime.now().isoformat()
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