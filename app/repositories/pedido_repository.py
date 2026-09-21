from app.extensions import db
from app.models.pedido import Pedido


class PedidoRepository:
    def find_all(self):
        return Pedido.query.order_by(Pedido.id).all()

    def find_by_id(self, pedido_id):
        return db.session.get(Pedido, pedido_id)

    def find_by_name(self, nome):
        return (
            Pedido.query.filter(Pedido.nome_cliente.ilike(f"%{nome}%"))
            .order_by(Pedido.id)
            .all()
        )

    def count(self):
        return Pedido.query.count()

    def save(self, pedido):
        db.session.add(pedido)
        db.session.commit()
        return pedido

    def delete(self, pedido):
        db.session.delete(pedido)
        db.session.commit()
