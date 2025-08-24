import pytest
from engine.cards import Card
from engine.deck import Deck


def test_four_copy_limit():
    card = Card("a", "A", 1, ["Creature"], ["C"], (1, 1))
    Deck([card] * 4)  # should not raise
    with pytest.raises(ValueError):
        Deck([card] * 5)
