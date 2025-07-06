from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# 🚀 Cria banco e tabela automaticamente SEM usar outro script
os.makedirs("banco", exist_ok=True)
db_path = "banco/usuarios.db"
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')
con.commit()
con.close()
print("Banco e tabela prontos!")

# 🌐 Flask App
app = Flask(__name__)
CORS(app)

def conectar():
    return sqlite3.connect("banco/usuarios.db")

@app.route('/api/registrar', methods=['POST'])
def registrar():
    data = request.get_json(force=True)
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'erro': 'Por favor, preencha todos os campos'}), 400

    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        con.commit()
        return jsonify({'mensagem': 'Usuário registrado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'erro': 'Email já cadastrado!'}), 400
    finally:
        con.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email = data.get('email')
    senha = data.get('senha')

    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT nome FROM usuarios WHERE email=? AND senha=?", (email, senha))
    usuario = cur.fetchone()
    con.close()

    if usuario:
        return jsonify({'mensagem': f'Bem-vindo, {usuario[0]}!'})
    return jsonify({'erro': 'Login inválido'}), 401

@app.route('/')
def home():
    return '🚀 API Flask rodando com sucesso!'

# Executa na porta 10000 para a Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
