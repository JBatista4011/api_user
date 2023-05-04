import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

# Conectar ao banco de dados MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="teste"
)

# Pesquisar todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    mycursor1 = mycursor.fetchall()
    users = list()
    for user in mycursor1:
        users.append({
            'id': user[0],
            'nome': user[1],
            'login': user[2],
            'senha': user[3]
        })
    return jsonify({'users': users})

# Pesquisar um usuário pelo login
@app.route('/users/<string:login>', methods=['GET'])
def get_user(login):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE login = %s"
    val = (login,)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    user_dict = {
        'id': user[0],
        'nome': user[1],
        'login': user[2],
        'senha': user[3]
    }
    return jsonify({'user': user_dict})

# Criar um novo usuário
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'nome' in data or not 'login' in data or not 'senha' in data:
        return jsonify({'message': 'Dados inválidos'}), 400
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (nome, login, senha) VALUES (%s, %s, %s)"
    val = (data['nome'], data['login'], data['senha'])
    mycursor.execute(sql, val)
    mydb.commit()
    user_dict = {
        'id': mycursor.lastrowid,
        'nome': data['nome'],
        'login': data['login'],
        'senha': data['senha']
    }
    return jsonify({'user': user_dict}), 201

# Atualizar um usuário existente
@app.route('/users/<string:login>', methods=['PUT'])
def update_user(login):
    data = request.get_json()
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE login = %s"
    val = (login,)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    if not data:
        return jsonify({'message': 'Dados inválidos'}), 400
    nome = data.get('nome', user[1])
    senha = data.get('senha', user[3])
    sql = "UPDATE users SET nome = %s, senha = %s WHERE login = %s"
    val = (nome, senha, login)
    mycursor.execute(sql, val)
    mydb.commit()

# Deletar um usuário existente
@app.route('/users/<string:login>', methods=['DELETE'])
def delete_user(login):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE login = %s"
    val = (login,)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    sql = "DELETE FROM users WHERE login = %s"
    val = (login,)
    mycursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200

app.run(port=5000, host='localhost',debug=True)