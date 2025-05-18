from flask import Blueprint

from .clientes import clientes_bp

def register_routes(app):
    app.register_blueprint(clientes_bp)