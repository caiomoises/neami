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

MAX_CHAMADAS = 6

def carregar_dados():
    if os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return DADOS_VAZIOS
    return DADOS_VAZIOS

def salvar_dados(dados):
    with open(DADOS_PATH, 'w') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

@app.route('/')
def painel():
    return render_template('painel.html')

@app.route('/controle')
def controle():
    return render_template('controle.html')

@app.route('/edicao')
def edicao():
    return render_template('edicao.html')

@app.route('/dados', methods=['GET'])
def get_dados():
    dados = carregar_dados()
    dados["chamadas"] = sorted(
        dados.get("chamadas", []),
        key=lambda x: (x.get("horario", "99:99"), x.get("timestamp", ""))
    )
    return jsonify(dados)

@app.route('/dados', methods=['POST'])
def atualizar_dados():
    novos_dados = request.get_json()
    novos_dados['timestamp'] = datetime.now().isoformat()

    dados = carregar_dados()
    chamadas = dados.get("chamadas", [])
    chamadas.insert(0, novos_dados)
    
    dados_salvar = {
        "chamadas": chamadas[:MAX_CHAMADAS],
        "ultima_atualizacao": datetime.now().isoformat()
    }

    salvar_dados(dados_salvar)
    return jsonify({'status': 'ok'})

@app.route('/editar', methods=['POST'])
def editar_dados():
    try:
        dados_edicao = request.get_json()
        index_ordenado = dados_edicao.get('index')  # Índice na ordenação por horário
        novos_dados = dados_edicao.get('dados')

        dados = carregar_dados()
        
        # Ordena as chamadas por horário para encontrar o índice correto
        chamadas_ordenadas = sorted(
            dados.get("chamadas", []),
            key=lambda x: (x.get("horario", "99:99"), x.get("timestamp", ""))
        )
        if not 0 <= index_ordenado < len(chamadas_ordenadas):
            return jsonify({'status': 'error', 'message': 'Índice inválido'}), 400
        
        # Obtém o ID/timestamp da chamada que está sendo editada
        chamada_id = chamadas_ordenadas[index_ordenado]['timestamp']
        
        # Encontra a chamada original na lista não ordenada
        for i, chamada in enumerate(dados["chamadas"]):
            if chamada['timestamp'] == chamada_id:
                # Atualiza a chamada encontrada
                novos_dados['timestamp'] = datetime.now().isoformat()
                dados["chamadas"][i] = novos_dados
                break
        
        dados["ultima_atualizacao"] = datetime.now().isoformat()
        salvar_dados(dados)
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/limpar', methods=['POST'])
def limpar_dados():
    try:
        salvar_dados(DADOS_VAZIOS)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists(DADOS_PATH):
        salvar_dados(DADOS_VAZIOS)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)