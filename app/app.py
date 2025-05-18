from flask import Flask, request, jsonify
from models.cliente import db, Cliente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Criar tabelas no primeiro acesso
with app.app_context():
    db.create_all()

# CREATE - Criar cliente
@app.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.get_json()
    novo_cliente = Cliente(nome=data['nome'], email=data['email'])
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify(novo_cliente.to_dict()), 201

# READ - Listar todos os clientes
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

# READ - Buscar cliente por ID
@app.route('/clientes/<int:id>', methods=['GET'])
def obter_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict())

# UPDATE - Atualizar cliente
@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()
    cliente.nome = data.get('nome', cliente.nome)
    cliente.email = data.get('email', cliente.email)
    db.session.commit()
    return jsonify(cliente.to_dict())

# DELETE - Deletar cliente
@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({
        "mensagem": "Cliente deletado com sucesso.",
        "cliente_id": id       
        })

if __name__ == '__main__':
    app.run(debug=True)
