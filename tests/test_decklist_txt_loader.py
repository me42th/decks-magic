from types import SimpleNamespace
from pathlib import Path

from decklist_txt_loader import load_deck


class DummyResponse:
    def __init__(self, name: str):
        self.name = name

    def raise_for_status(self) -> None:  # pragma: no cover - simple stub
        pass

    def json(self) -> dict:
        return {
            "cards": [
                {
                    "id": f"id_{self.name}",
                    "name": self.name,
                    "cmc": 0,
                    "types": ["Basic", "Land"],
                    "colors": [],
                    "text": "",
                }
            ]
        }


def fake_get(url: str, params: dict, timeout: int = 10) -> DummyResponse:
    return DummyResponse(params["name"])


def test_load_deck_from_txt(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("decklist_txt_loader.requests.get", fake_get)
    deck_file = tmp_path / "deck.txt"
    deck_file.write_text("2 Forest\n")
    deck = load_deck(deck_file)
    assert len(deck.cards) == 2
    assert all(card.name == "Forest" for card in deck.cards)
