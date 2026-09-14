from flask import Flask, jsonify, request, send_from_directory

from app.controllers.jogador_controller import JogadorController
from app.repositories.jogador_repository import JogadorRepository


app = Flask(
    __name__,
    static_folder="app/views/static",
)
jogador_controller = JogadorController(JogadorRepository())


@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/jogadores")
def create_jogador():
    try:
        data = request.get_json(silent=True) or {}
        jogador = jogador_controller.create(data.get("nome", ""))
        return jsonify({"id": jogador.id, "nome": jogador.nome}), 201
    except (TypeError, ValueError) as error:
        return jsonify(error=str(error)), 400


@app.get("/jogadores")
def list_jogadores():
    jogadores = jogador_controller.list_all()
    return jsonify([{"id": jogador.id, "nome": jogador.nome} for jogador in jogadores])


@app.get("/jogadores/<int:jogador_id>")
def get_jogador(jogador_id: int):
    jogador = jogador_controller.get(jogador_id)
    if jogador is None:
        return jsonify(error="Jogador nao encontrado"), 404
    return jsonify({"id": jogador.id, "nome": jogador.nome})


@app.delete("/jogadores/<int:jogador_id>")
def delete_jogador(jogador_id: int):
    if not jogador_controller.delete(jogador_id):
        return jsonify(error="Jogador nao encontrado"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
