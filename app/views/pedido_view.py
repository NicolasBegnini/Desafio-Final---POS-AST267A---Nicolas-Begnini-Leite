def render_pedido(pedido):
    return {
        "id": pedido.id,
        "nome_cliente": pedido.nome_cliente,
        "produto": pedido.produto,
        "quantidade": pedido.quantidade,
        "valor_total": pedido.valor_total,
        "status": pedido.status,
        "criado_em": pedido.criado_em.isoformat() if pedido.criado_em else None,
    }


def render_pedidos(pedidos):
    return [render_pedido(p) for p in pedidos]
