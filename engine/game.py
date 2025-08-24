from dataclasses import dataclass, field
from typing import List

from .cards import Card


@dataclass
class GameState:
    """Represents a very small portion of a Magic game state."""

    library: List[Card]
    hand: List[Card] = field(default_factory=list)
    battlefield: List[Card] = field(default_factory=list)
    graveyard: List[Card] = field(default_factory=list)
    life: int = 20
