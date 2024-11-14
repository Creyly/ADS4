
from flask import Flask, request, jsonify
import sqlite3

# Inicialize o app Flask
app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def connect_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row  # Permite que os resultados sejam acessados como dicionários
    return db

# Crie uma rota para inserir dados
@app.route('/add', methods=['POST'])
def add_item():
    data = request.get_json()
    product_code = data.get('product_code')
    description = data.get('description')

    # Insere os dados na tabela do banco de dados
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO products (product_code, description) VALUES (?, ?)', (product_code, description))
    db.commit()
    db.close()

    return jsonify({'message': 'Produto adicionado com sucesso!'}), 201

# Crie uma rota para buscar dados
@app.route('/product/<product_code>', methods=['GET'])
def get_product(product_code):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE product_code = ?', (product_code,))
    product = cursor.fetchone()
    db.close()

    if product:
        return jsonify(dict(product)), 200
    else:
        return jsonify({'message': 'Produto não encontrado!'}), 404

# Execute o app
if __name__ == '__main__':
    # Criação da tabela caso não exista
    db = connect_db()
    db.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, product_code TEXT, description TEXT)')
    db.close()
    app.run(debug=True)