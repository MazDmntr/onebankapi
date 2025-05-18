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

def test_criar_cliente(client):
    res = client.post('/clientes', json={'nome': 'Maria', 'email': 'maria@example.com'})
    assert res.status_code == 201
    data = res.get_json()
    assert data['nome'] == 'Maria'
    assert data['email'] == 'maria@example.com'


def test_listar_clientes(client):
    client.post('/clientes', json={'nome': 'João', 'email': 'joao@example.com'})
    res = client.get('/clientes')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 1

def test_obter_cliente_por_id(client):
    res = client.post('/clientes', json={'nome': 'Carlos', 'email': 'carlos@example.com'})
    cliente_id = res.get_json()['id']
    get_res = client.get(f'/clientes/{cliente_id}')
    assert get_res.status_code == 200
    assert get_res.get_json()['nome'] == 'Carlos'

def test_atualizar_cliente(client):
    res = client.post('/clientes', json={'nome': 'Ana', 'email': 'ana@example.com'})
    cliente_id = res.get_json()['id']
    update_res = client.put(f'/clientes/{cliente_id}', json={'nome': 'Ana Maria'})
    assert update_res.status_code == 200
    assert update_res.get_json()['nome'] == 'Ana Maria'

def test_deletar_cliente(client):
    res = client.post('/clientes', json={'nome': 'Pedro', 'email': 'pedro@example.com'})
    cliente_id = res.get_json()['id']
    del_res = client.delete(f'/clientes/{cliente_id}')
    assert del_res.status_code == 200
    get_res = client.get(f'/clientes/{cliente_id}')
    assert get_res.status_code == 404
