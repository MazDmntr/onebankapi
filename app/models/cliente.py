from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(15), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    data_cadastro = db.Column(db.DateTime, server_default=db.func.now())
    data_atualizacao = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    def __init__(self, nome, email, cpf, telefone=None, endereco=None, data_nascimento=None):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.data_nascimento = data_nascimento
        self.data_cadastro = db.func.now()
        self.data_atualizacao = db.func.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'data_cadastro': self.data_cadastro.isoformat(),
            'data_atualizacao': self.data_atualizacao.isoformat()
        }