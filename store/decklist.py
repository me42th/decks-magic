from pathlib import Path
from typing import List

from engine.deck import Deck
from engine.cards import Card
from api.mgt_api import fetch_card_data


def load_decklist_txt(path: Path) -> Deck:
    """Load a deck list from a plaintext file using MTG API for card details."""
    cards: List[Card] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            qty_str, name = line.split(" ", 1)
            qty = int(qty_str)
        except ValueError:
            # skip malformed lines
            continue
        card = fetch_card_data(name)
        cards.extend([card] * qty)
    return Deck(cards)
