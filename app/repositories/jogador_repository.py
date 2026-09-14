import os

import psycopg

from app.models.jogador import Jogador


class JogadorRepository:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = database_url or os.getenv("DATABASE_URL", "")

    def create(self, nome: str) -> Jogador:
        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO jogadores (nome) VALUES (%s) RETURNING id, nome",
                    (nome,),
                )
                jogador_id, jogador_nome = cursor.fetchone()
        return Jogador(id=jogador_id, nome=jogador_nome)

    def list_all(self) -> list[Jogador]:
        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nome FROM jogadores ORDER BY id")
                rows = cursor.fetchall()
        return [Jogador(id=jogador_id, nome=nome) for jogador_id, nome in rows]

    def get_by_id(self, jogador_id: int) -> Jogador | None:
        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nome FROM jogadores WHERE id = %s", (jogador_id,))
                row = cursor.fetchone()
        if row is None:
            return None
        return Jogador(id=row[0], nome=row[1])

    def delete(self, jogador_id: int) -> bool:
        with psycopg.connect(self.database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM jogadores WHERE id = %s", (jogador_id,))
                return cursor.rowcount > 0
