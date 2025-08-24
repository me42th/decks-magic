from types import SimpleNamespace
from pathlib import Path

from decklist_txt_loader import carregar_baralho


class RespostaDummy:
    def __init__(self, nome: str):
        self.nome = nome

    def raise_for_status(self) -> None:  # pragma: no cover - mantemos o nome para imitar ``requests``
        pass

    def json(self) -> dict:
        return {
            "cards": [
                {
                    "id": f"id_{self.nome}",
                    "name": self.nome,
                    "cmc": 0,
                    "types": ["Basic", "Land"],
                    "colors": [],
                    "text": "",
                }
            ]
        }


def obter_falso(url: str, params: dict, timeout: int = 10) -> RespostaDummy:
    # ``params`` é um dicionário; em PHP seria um array associativo.
    return RespostaDummy(params["name"])


def teste_carregar_baralho_do_txt(monkeypatch, tmp_path: Path) -> None:
    # ``monkeypatch`` é um recurso de testes do pytest para substituir atributos dinamicamente.
    monkeypatch.setattr("decklist_txt_loader.requests.get", obter_falso)
    # O operador ``/`` é sobrecarregado em ``Path`` para criar caminhos; PHP não possui essa sintaxe.
    arquivo_baralho = tmp_path / "deck.txt"
    arquivo_baralho.write_text("2 Forest\n")
    baralho = carregar_baralho(arquivo_baralho)
    assert len(baralho.cards) == 2
    # Expressão geradora; em PHP seria necessário um laço ``foreach``.
    assert all(carta.name == "Forest" for carta in baralho.cards)
