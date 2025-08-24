from __future__ import annotations
from collections import Counter
from typing import List

from .cards import Card


class Deck:
    """List of cards with basic validation rules."""

    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.validate()

    def validate(self) -> None:
        counts = Counter(card.id for card in self.cards)
        if len(self.cards) < 1:
            raise ValueError("Deck must contain at least one card")
        for card in self.cards:
            # Basic lands are exempt from the four-copy rule
            is_basic_land = "Basic" in card.types and "Land" in card.types
            if not is_basic_land and counts[card.id] > 4:
                raise ValueError(f"Card {card.name} exceeds four-copy limit")
