import json
from pathlib import Path
from typing import List, Optional, Tuple
from types import SimpleNamespace

try:  # pragma: no cover - exercised via tests with monkeypatch
    import requests as _requests
except Exception:  # requests may not be installed in minimal environments
    _requests = None

# ``requests`` is exposed as a module-level object so that tests (and callers)
# can monkeypatch ``requests.get`` even if the real library isn't available.
def _missing_requests_get(*args, **kwargs):  # pragma: no cover - simple fallback
    raise RuntimeError("requests library is required to fetch card data")

requests = _requests or SimpleNamespace(get=_missing_requests_get)

from engine.cards import Card
from engine.deck import Deck

API_URL = "https://api.magicthegathering.io/v1/cards"


def _parse_line(line: str) -> Optional[tuple[int, str]]:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = line.split(" ", 1)
    if len(parts) != 2:
        return None
    qty_str, name = parts
    try:
        qty = int(qty_str)
    except ValueError:
        return None
    return qty, name.strip()


def _fetch_card(name: str) -> Optional[Card]:
    try:
        resp = requests.get(API_URL, params={"name": name}, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("cards", [])
        if not data:
            print(f"Warning: card '{name}' not found")
            return None
        card_data = data[0]
        power = card_data.get("power")
        toughness = card_data.get("toughness")
        pt: Optional[Tuple[int, int]] = None
        try:
            if power is not None and toughness is not None:
                pt = (int(power), int(toughness))
        except ValueError:
            pt = None
        return Card(
            id=card_data.get("id", name),
            name=card_data.get("name", name),
            cmc=int(card_data.get("cmc", 0)),
            types=card_data.get("types", []),
            colors=card_data.get("colors", []),
            pt=pt,
            text_dsl=card_data.get("text", ""),
        )
    except Exception as exc:
        print(f"Warning: failed to fetch card '{name}': {exc}")
        return None


def load_deck(path: Path) -> Deck:
    cards: List[Card] = []
    for line in path.read_text().splitlines():
        parsed = _parse_line(line)
        if not parsed:
            continue
        qty, name = parsed
        card = _fetch_card(name)
        if card is None:
            continue
        cards.extend([card] * qty)
    return Deck(cards)
