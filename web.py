import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
import psycopg
from werkzeug.exceptions import HTTPException

from app.controllers.cliente_controller import ClienteController
from app.controllers.peca_controller import PecaController
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.peca_repository import PecaRepository


app = Flask(
    __name__,
    static_folder="app/views/static",
)
cliente_controller = ClienteController(ClienteRepository())
peca_controller = PecaController(PecaRepository())


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    if request.path.startswith("/pecas") or request.path.startswith("/clientes") or request.path.startswith("/health"):
        return jsonify(
            error=f"{type(error).__name__}: {error.description or 'Erro na requisicao.'}"
        ), error.code or 500
    return error


@app.errorhandler(Exception)
def handle_unexpected_exception(error):
    if request.path.startswith("/pecas") or request.path.startswith("/clientes") or request.path.startswith("/health"):
        return jsonify(
            error=f"{type(error).__name__}: {error}"
        ), 500
    return error


@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/clientes")
def create_cliente():
    try:
        data = request.get_json(silent=True) or {}
        cliente = cliente_controller.create(data.get("nome", ""))
        return jsonify({"id": cliente.id, "nome": cliente.nome}), 201
    except (TypeError, ValueError) as error:
        return jsonify(error=str(error)), 400


@app.get("/clientes")
def list_clientes():
    clientes = cliente_controller.list_all()
    return jsonify([{"id": cliente.id, "nome": cliente.nome} for cliente in clientes])


@app.get("/clientes/<int:cliente_id>")
def get_cliente(cliente_id: int):
    cliente = cliente_controller.get(cliente_id)
    if cliente is None:
        return jsonify(error="Cliente nao encontrado"), 404
    return jsonify({"id": cliente.id, "nome": cliente.nome})


@app.delete("/clientes/<int:cliente_id>")
def delete_cliente(cliente_id: int):
    if not cliente_controller.delete(cliente_id):
        return jsonify(error="Cliente nao encontrado"), 404
    return "", 204


@app.get("/pecas")
def list_pecas():
    try:
        filters = {
            "categoria": request.args.get("categoria") or None,
            "fabricante": request.args.get("fabricante") or None,
            "status": request.args.get("status") or None,
            "disponibilidade": request.args.get("disponibilidade") or None,
        }
        search = request.args.get("search") or None
        page = max(int(request.args.get("page", 1)), 1)
        per_page = max(int(request.args.get("per_page", 20)), 1)

        pecas, total = peca_controller.list_all(filters, search, page, per_page)
        return jsonify(
            {
                "items": [serialize_peca(peca) for peca in pecas],
                "total": total,
                "page": page,
                "per_page": per_page,
            }
        )
    except (TypeError, ValueError) as error:
        return jsonify(error=str(error)), 400
    except Exception as error:
        return jsonify(error=f"Erro ao listar peças: {error}"), 500


@app.post("/pecas")
def create_peca():
    try:
        data = request.get_json(silent=True) or {}
        peca = peca_controller.create(data)
        return jsonify(serialize_peca(peca)), 201
    except (TypeError, ValueError) as error:
        return jsonify(error=str(error)), 400
    except psycopg.errors.UniqueViolation:
        return jsonify(error="Codigo ou SKU duplicado."), 409
    except Exception as error:
        return jsonify(error=f"Erro ao criar peça: {error}"), 500


@app.get("/pecas/<int:peca_id>")
def get_peca(peca_id: int):
    try:
        peca = peca_controller.get(peca_id)
        if peca is None:
            return jsonify(error="Peca nao encontrada"), 404
        return jsonify(serialize_peca(peca))
    except Exception as error:
        return jsonify(error=f"Erro ao buscar peça: {error}"), 500


@app.route("/pecas/<int:peca_id>", methods=["PUT", "PATCH"])
def update_peca(peca_id: int):
    try:
        data = request.get_json(silent=True) or {}
        peca = peca_controller.update(peca_id, data)
        if peca is None:
            return jsonify(error="Peca nao encontrada"), 404
        return jsonify(serialize_peca(peca))
    except (TypeError, ValueError) as error:
        return jsonify(error=str(error)), 400
    except psycopg.errors.UniqueViolation:
        return jsonify(error="Codigo ou SKU duplicado."), 409
    except Exception as error:
        return jsonify(error=f"Erro ao atualizar peça: {error}"), 500


@app.delete("/pecas/<int:peca_id>")
def delete_peca(peca_id: int):
    try:
        if not peca_controller.delete(peca_id):
            return jsonify(error="Peca nao encontrada"), 404
        return "", 204
    except Exception as error:
        return jsonify(error=f"Erro ao excluir peça: {error}"), 500


def serialize_peca(peca):
    return {
        "id": peca.id,
        "nome": peca.nome,
        "codigo": peca.codigo,
        "sku": peca.sku,
        "codigo_fabricante": peca.codigo_fabricante,
        "descricao": peca.descricao,
        "categoria": peca.categoria,
        "fabricante": peca.fabricante,
        "fornecedor": peca.fornecedor,
        "quantidade_estoque": peca.quantidade_estoque,
        "estoque_minimo": peca.estoque_minimo,
        "preco_custo": float(peca.preco_custo),
        "preco_venda": float(peca.preco_venda),
        "localizacao": peca.localizacao,
        "status": peca.status,
        "ultima_atualizacao": peca.ultima_atualizacao,
        "created_at": peca.created_at,
    }


def ensure_database_schema() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return

    init_sql_path = Path(__file__).resolve().parent / "database" / "init.sql"
    if not init_sql_path.exists():
        return

    sql_script = init_sql_path.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in sql_script.split(";") if statement.strip()]

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)


if __name__ == "__main__":
    ensure_database_schema()
    app.run(host="0.0.0.0", port=8000)
