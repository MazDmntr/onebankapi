from flask.testing import FlaskClient
import pytest
from app.app import app, db, Cliente

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


modelo_cliente = {
    'nome': 'Maria', 
    'email': 'maria@example.com',
    }

def test_criar_cliente(client: FlaskClient):
    res = client.post('/clientes', json=modelo_cliente)
    assert res.status_code == 201
    data = res.get_json()
    assert data['nome'] == modelo_cliente['nome']
    assert data['email'] == modelo_cliente['email']


def test_listar_clientes(client: FlaskClient):
    client.post('/clientes', json=modelo_cliente)
    res = client.get('/clientes')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 1

def test_obter_cliente_por_id(client: FlaskClient):
    res = client.post('/clientes', json=modelo_cliente)
    cliente_id = res.get_json()['id']
    get_res = client.get(f'/clientes/{cliente_id}')
    assert get_res.status_code == 200
    assert get_res.get_json()['nome'] == modelo_cliente['nome']

def test_atualizar_cliente(client: FlaskClient):
    res = client.post('/clientes', json=modelo_cliente)
    cliente_id = res.get_json()['id']
    update_res = client.put(f'/clientes/{cliente_id}', json=modelo_cliente)
    assert update_res.get_json()['nome'] == modelo_cliente['nome']

def test_deletar_cliente(client: FlaskClient):
    res = client.post('/clientes', json=modelo_cliente)
    cliente_id = res.get_json()['id']
    del_res = client.delete(f'/clientes/{cliente_id}')
    assert del_res.status_code == 200
    get_res = client.get(f'/clientes/{cliente_id}')
    assert get_res.status_code == 404
