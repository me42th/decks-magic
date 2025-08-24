import random
from typing import List

from .cards import Card
from .game import GameState


def reveal_until_non_token(library: List[Card]) -> List[Card]:
    """Reveal cards from ``library`` until a non-token card is found.

    The revealed cards are removed from ``library`` and returned.  This mirrors
    the Horde format rule where the top of the library is revealed until a
    proper spell is hit.
    """
    revealed: List[Card] = []
    while library:
        card = library.pop(0)
        revealed.append(card)
        if "Token" not in card.types:
            break
    return revealed


def mill(library: List[Card], amount: int) -> None:
    """Remove ``amount`` cards from the top of ``library``.

    In the Horde format the Horde has no life total; instead damage is applied
    by milling cards.  ``mill`` performs this operation in-place.
    """

    del library[:amount]


def play_horde_turn(state: GameState, horde_library: List[Card], rng: random.Random) -> None:
    """Execute the Horde's turn following the simplified rules.

    Tokens are created with haste, the first non-token is "cast" and all Horde
    creatures attack immediately dealing damage equal to their combined power.
    """
    revealed = reveal_until_non_token(horde_library)
    tokens = [c for c in revealed if "Token" in c.types]
    non_tokens = [c for c in revealed if "Token" not in c.types]

    state.battlefield.extend(tokens)
    if non_tokens:
        state.battlefield.extend(non_tokens)

    # All horde creatures attack, player loses life equal to their power
    total_power = sum(card.pt[0] for card in state.battlefield if card.pt)
    state.life -= total_power
