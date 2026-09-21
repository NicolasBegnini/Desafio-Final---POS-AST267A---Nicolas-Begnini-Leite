from flask import Blueprint, jsonify, request

from app.services.pedido_service import PedidoService, ValidacaoError
from app.views.pedido_view import render_pedido, render_pedidos

pedido_bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")
service = PedidoService()


@pedido_bp.get("")
def listar_todos():
    return jsonify(render_pedidos(service.listar_todos())), 200


@pedido_bp.get("/contar")
def contar():
    return jsonify({"total": service.contar()}), 200


@pedido_bp.get("/nome/<string:nome>")
def buscar_por_nome(nome):
    return jsonify(render_pedidos(service.buscar_por_nome(nome))), 200


@pedido_bp.get("/<int:pedido_id>")
def buscar_por_id(pedido_id):
    pedido = service.buscar_por_id(pedido_id)
    if pedido is None:
        return jsonify({"erro": f"Pedido {pedido_id} não encontrado"}), 404
    return jsonify(render_pedido(pedido)), 200


@pedido_bp.post("")
def criar():
    try:
        pedido = service.criar(request.get_json(silent=True))
    except ValidacaoError as e:
        return jsonify({"erro": str(e)}), 400
    return jsonify(render_pedido(pedido)), 201


@pedido_bp.put("/<int:pedido_id>")
def atualizar(pedido_id):
    try:
        pedido = service.atualizar(pedido_id, request.get_json(silent=True))
    except ValidacaoError as e:
        return jsonify({"erro": str(e)}), 400
    if pedido is None:
        return jsonify({"erro": f"Pedido {pedido_id} não encontrado"}), 404
    return jsonify(render_pedido(pedido)), 200


@pedido_bp.delete("/<int:pedido_id>")
def deletar(pedido_id):
    if not service.deletar(pedido_id):
        return jsonify({"erro": f"Pedido {pedido_id} não encontrado"}), 404
    return "", 204
