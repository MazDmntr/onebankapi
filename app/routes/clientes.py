from flask import Blueprint, jsonify, request
from app.models import Cliente 
from app import db
from datetime import datetime

clientes_bp = Blueprint("clientes", __name__)

# CREATE - Criar cliente
@clientes_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.get_json()
    novo_cliente = Cliente(
        nome=data['nome'], 
        email=data['email'],
        cpf=data['cpf'],
        telefone=data.get('telefone'),
        endereco=data.get('endereco'),
        data_nascimento=datetime.strptime(data.get('data_nascimento'),'%Y-%m-%d')
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify(novo_cliente.to_dict()), 201

# READ - Listar todos os clientes
@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

# READ - Buscar cliente por ID
@clientes_bp.route('/clientes/<int:id>', methods=['GET'])
def obter_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict())

# UPDATE - Atualizar cliente
@clientes_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()
    cliente.nome = data.get('nome', cliente.nome)
    cliente.email = data.get('email', cliente.email)
    cliente.cpf = data.get('cpf', cliente.cpf)
    cliente.telefone = data.get('telefone', cliente.telefone)
    cliente.endereco = data.get('endereco', cliente.endereco)
    cliente.data_nascimento = datetime.strptime(data.get('data_nascimento'),'%Y-%m-%d') if data.get('data_nascimento') else cliente.data_nascimento
    cliente.data_atualizacao = db.func.now()
    db.session.commit()
    return jsonify(cliente.to_dict())

# DELETE - Deletar cliente
@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({
        "mensagem": "Cliente deletado com sucesso.",
        "cliente_id": id       
        })
    