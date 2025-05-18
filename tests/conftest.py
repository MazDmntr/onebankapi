import pytest
from app import create_app, db

@pytest.fixture
def app():
    test_config = 'sqlite:///:memory:'
    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()