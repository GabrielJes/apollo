from app.models.jogador import Jogador
from app.repositories.jogador_repository import JogadorRepository


class JogadorController:
    def __init__(self, repository: JogadorRepository) -> None:
        self.repository = repository

    def create(self, nome: str) -> Jogador:
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome do jogador e obrigatorio.")
        return self.repository.create(nome.strip())

    def list_all(self) -> list[Jogador]:
        return self.repository.list_all()

    def get(self, jogador_id: int) -> Jogador | None:
        return self.repository.get_by_id(jogador_id)

    def delete(self, jogador_id: int) -> bool:
        return self.repository.delete(jogador_id)
