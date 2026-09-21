# API REST de Pedidos — Flask + MVC

Desafio Final do Bootcamp Arquiteto(a) de Software.

## Como executar
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
python run.py                   # http://127.0.0.1:5000
python -m pytest -q             # testes automatizados
```

## Endpoints
| Método | Rota                   | Descrição                          |
|--------|------------------------|------------------------------------|
| POST   | /pedidos               | Cria um pedido                     |
| GET    | /pedidos               | Lista todos (Find All)             |
| GET    | /pedidos/{id}          | Busca por ID (Find By ID)          |
| GET    | /pedidos/nome/{nome}   | Busca por nome do cliente          |
| GET    | /pedidos/contar        | Total de registros (Contagem)      |
| PUT    | /pedidos/{id}          | Atualiza um pedido                 |
| DELETE | /pedidos/{id}          | Remove um pedido                   |

## Estrutura
Ver a pasta `docs/` para os diagramas e a explicação da arquitetura.
