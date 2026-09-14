import unittest

from app.controllers.jogador_controller import JogadorController
from app.models.jogador import Jogador


class FakeJogadorRepository:
    def __init__(self) -> None:
        self.jogadores = {}
        self.next_id = 1

    def create(self, nome: str) -> Jogador:
        jogador = Jogador(self.next_id, nome)
        self.jogadores[jogador.id] = jogador
        self.next_id += 1
        return jogador

    def list_all(self) -> list[Jogador]:
        return list(self.jogadores.values())

    def get_by_id(self, jogador_id: int) -> Jogador | None:
        return self.jogadores.get(jogador_id)

    def delete(self, jogador_id: int) -> bool:
        return self.jogadores.pop(jogador_id, None) is not None


class JogadorControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = JogadorController(FakeJogadorRepository())

    def test_cria_lista_busca_e_exclui_jogador(self) -> None:
        jogador = self.controller.create(" Ronaldinho Gaucho ")
        self.assertEqual(jogador.nome, "Ronaldinho Gaucho")
        self.assertEqual(self.controller.list_all(), [jogador])
        self.assertEqual(self.controller.get(jogador.id), jogador)
        self.assertTrue(self.controller.delete(jogador.id))
        self.assertIsNone(self.controller.get(jogador.id))

    def test_nome_e_obrigatorio(self) -> None:
        with self.assertRaises(ValueError):
            self.controller.create("   ")


if __name__ == "__main__":
    unittest.main()
