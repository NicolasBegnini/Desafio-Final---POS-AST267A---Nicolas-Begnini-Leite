import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()


PEDIDO = {"nome_cliente": "Maria Silva", "produto": "Notebook", "quantidade": 1, "valor_total": 4500.0}


def test_criar_e_buscar_por_id(client):
    r = client.post("/pedidos", json=PEDIDO)
    assert r.status_code == 201
    pedido_id = r.get_json()["id"]
    r = client.get(f"/pedidos/{pedido_id}")
    assert r.status_code == 200
    assert r.get_json()["nome_cliente"] == "Maria Silva"
    assert r.get_json()["status"] == "CRIADO"


def test_listar_e_contar(client):
    client.post("/pedidos", json=PEDIDO)
    client.post("/pedidos", json={**PEDIDO, "nome_cliente": "João Souza"})
    assert len(client.get("/pedidos").get_json()) == 2
    assert client.get("/pedidos/contar").get_json() == {"total": 2}


def test_buscar_por_nome_parcial(client):
    client.post("/pedidos", json=PEDIDO)
    client.post("/pedidos", json={**PEDIDO, "nome_cliente": "João Souza"})
    r = client.get("/pedidos/nome/maria")
    assert r.status_code == 200
    assert [p["nome_cliente"] for p in r.get_json()] == ["Maria Silva"]


def test_atualizar(client):
    pid = client.post("/pedidos", json=PEDIDO).get_json()["id"]
    r = client.put(f"/pedidos/{pid}", json={"status": "PAGO", "quantidade": 2})
    assert r.status_code == 200
    assert r.get_json()["status"] == "PAGO"
    assert r.get_json()["quantidade"] == 2


def test_deletar(client):
    pid = client.post("/pedidos", json=PEDIDO).get_json()["id"]
    assert client.delete(f"/pedidos/{pid}").status_code == 204
    assert client.get(f"/pedidos/{pid}").status_code == 404


def test_nao_encontrado(client):
    assert client.get("/pedidos/999").status_code == 404
    assert client.put("/pedidos/999", json={"status": "PAGO"}).status_code == 404
    assert client.delete("/pedidos/999").status_code == 404


@pytest.mark.parametrize(
    "corpo",
    [
        {},
        {"produto": "X", "quantidade": 1, "valor_total": 1},
        {**PEDIDO, "quantidade": 0},
        {**PEDIDO, "valor_total": -1},
        {**PEDIDO, "status": "INVENTADO"},
    ],
)
def test_validacoes(client, corpo):
    assert client.post("/pedidos", json=corpo).status_code == 400


def test_corpo_nao_json(client):
    r = client.post("/pedidos", data="texto", content_type="text/plain")
    assert r.status_code == 400
