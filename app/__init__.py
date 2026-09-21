from flask import Flask, jsonify

from app.config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.controllers.pedido_controller import pedido_bp
    from app.models.pedido import Pedido

    app.register_blueprint(pedido_bp)

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def rota_nao_encontrada(_erro):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(405)
    def metodo_nao_permitido(_erro):
        return jsonify({"erro": "Método HTTP não permitido"}), 405

    return app
