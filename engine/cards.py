from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass(frozen=True)
class Card:
    """Represents a minimal Magic card for the MVP."""
    id: str
    name: str
    cmc: int
    types: List[str]
    colors: List[str]
    pt: Optional[Tuple[int, int]] = None  # power, toughness
    text_dsl: str = ""
