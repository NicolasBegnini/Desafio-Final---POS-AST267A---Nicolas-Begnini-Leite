from app.models.pedido import Pedido
from app.repositories.pedido_repository import PedidoRepository

STATUS_VALIDOS = {"CRIADO", "PAGO", "ENVIADO", "ENTREGUE", "CANCELADO"}


class ValidacaoError(ValueError):
    """Lançada quando os dados recebidos violam uma regra de negócio."""

class PedidoService:
    def __init__(self, repository=None):
        self.repository = repository or PedidoRepository()

    def listar_todos(self):
        return self.repository.find_all()

    def buscar_por_id(self, pedido_id):
        return self.repository.find_by_id(pedido_id)

    def buscar_por_nome(self, nome):
        return self.repository.find_by_name(nome)

    def contar(self):
        return self.repository.count()

    def criar(self, dados):
        self._validar(dados, parcial=False)
        pedido = Pedido(
            nome_cliente=dados["nome_cliente"].strip(),
            produto=dados["produto"].strip(),
            quantidade=dados["quantidade"],
            valor_total=dados["valor_total"],
            status=dados.get("status", "CRIADO"),
        )
        return self.repository.save(pedido)

    def atualizar(self, pedido_id, dados):
        pedido = self.repository.find_by_id(pedido_id)
        if pedido is None:
            return None
        self._validar(dados, parcial=True)
        for campo in ("nome_cliente", "produto", "quantidade", "valor_total", "status"):
            if campo in dados:
                valor = dados[campo]
                setattr(pedido, campo, valor.strip() if isinstance(valor, str) else valor)
        return self.repository.save(pedido)

    def deletar(self, pedido_id):
        pedido = self.repository.find_by_id(pedido_id)
        if pedido is None:
            return False
        self.repository.delete(pedido)
        return True

    @staticmethod
    def _validar(dados, parcial):
        if not isinstance(dados, dict) or (not dados and not parcial):
            raise ValidacaoError("Corpo da requisição inválido ou vazio.")

        obrigatorios = ("nome_cliente", "produto", "quantidade", "valor_total")
        if not parcial:
            faltando = [c for c in obrigatorios if c not in dados]
            if faltando:
                raise ValidacaoError(f"Campos obrigatórios ausentes: {', '.join(faltando)}.")

        for campo in ("nome_cliente", "produto"):
            if campo in dados and (not isinstance(dados[campo], str) or not dados[campo].strip()):
                raise ValidacaoError(f"'{campo}' deve ser um texto não vazio.")

        if "quantidade" in dados:
            q = dados["quantidade"]
            if isinstance(q, bool) or not isinstance(q, int) or q <= 0:
                raise ValidacaoError("'quantidade' deve ser um inteiro maior que zero.")

        if "valor_total" in dados:
            v = dados["valor_total"]
            if isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0:
                raise ValidacaoError("'valor_total' deve ser um número maior ou igual a zero.")

        if "status" in dados and dados["status"] not in STATUS_VALIDOS:
            raise ValidacaoError(f"'status' deve ser um de: {', '.join(sorted(STATUS_VALIDOS))}.")
