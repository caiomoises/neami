<p align="center">
  <img src="static/logo.png" alt="Logo NEAMI" width="100"/>
</p>

# Sistema de Chamadas - NEAMI

Este sistema foi desenvolvido para o controle e exibição de chamadas de pacientes no ambiente do NEAMI. Ele permite a criação, edição e exclusão de chamadas, que são exibidas em tempo real em um painel público.

---

## 🔧 Tecnologias Utilizadas

- Python 3.x
- Flask
- Flask-RESTful (ou FlaskAPI)
- HTML, CSS e JavaScript
- Fetch API (frontend)

---

## 📋 Funcionalidades

- ✅ Adicionar novas chamadas com horário, sala, profissional e paciente.
- 📝 Editar chamadas já registradas.
- ❌ Excluir todas as chamadas com um clique.
- 📺 Visualizar painel público com as chamadas em tempo real.
- 🔁 Atualização automática via Fetch API no frontend.

---

## 🚀 Como Executar

### 1. Clone o repositório:

```bash
git clone https://github.com/caiomoises/neami.git
cd neami
```

### 2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
cd neami
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Execute o servidor:

```bash
python app.py
     ou
flask run
```

A aplicação estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 Estrutura do Projeto

```
neami/
│
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   ├── dados.json          # Armazenamento de dados
│   └── logo.png            # Imagem do logo
│
├── templates/              # Templates HTML
│   ├── controle.html
│   ├── edicao.html
│   └── painel.html
│
├── venv/                   # Ambiente virtual Python (gerado automaticamente)
│
├── data/                   # Pasta para dados adicionais (opcional)
│
├── app.py                  # Arquivo principal da aplicação Flask
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências Python
```

---

## 📲 Endpoints da API

| Método | Endpoint   | Descrição                                      | Corpo da Requisição (JSON)                          |
|--------|------------|-----------------------------------------------|----------------------------------------------------|
| GET    | /dados     | Retorna todas as chamadas ordenadas           |`{"horario": "12:00", "paciente": "paciente 1", "profissional": "profissional 1", "sala": "01", "timestamp": "2025-07-25T11:27:21.526681" },`                                                  |
| POST   | /dados     | Cria uma nova chamada                         | `{"horario": "HH:MM", "paciente": "...", "profissional": "...", "sala": "..."}` |
| POST   | /editar    | Edita uma chamada existente                   | `{"index": N, "dados": {dados_atualizados}}`       |
| POST   | /limpar    | Remove todas as chamadas (limpa o sistema)    | -                                                  |

### Exemplo de Chamada Completa

```json
{
  "horario": "14:30",
  "paciente": "João Silva",
  "profissional": "Dra. Ana",
  "sala": "3",
}
```

---

## 📸 Telas do Sistema

### ✅ Painel Público
Exibe a chamada atual e as próximas chamadas.

### 🛠 Painel de Controle
Permite criar, editar e limpar chamadas.

---

## 👨‍💻 Autor

Desenvolvido por @ocaiomoises – © 2025

---

## 📃 Licença

Este projeto está licenciado sob a Licença MIT.