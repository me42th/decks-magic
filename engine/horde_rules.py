import random
from typing import List

from .cards import Card
from .game import GameState


def reveal_until_non_token(library: List[Card]) -> List[Card]:
    """Reveal cards until a non-token card is found."""
    revealed: List[Card] = []
    while library:
        card = library.pop(0)
        revealed.append(card)
        if "Token" not in card.types:
            break
    return revealed


def play_horde_turn(state: GameState, horde_library: List[Card], rng: random.Random) -> None:
    """Very small subset of the Horda turn rules."""
    revealed = reveal_until_non_token(horde_library)
    tokens = [c for c in revealed if "Token" in c.types]
    non_tokens = [c for c in revealed if "Token" not in c.types]

    state.battlefield.extend(tokens)
    if non_tokens:
        state.battlefield.extend(non_tokens)

    # All horde creatures attack, player loses life equal to their power
    total_power = sum(card.pt[0] for card in state.battlefield if card.pt)
    state.life -= total_power
