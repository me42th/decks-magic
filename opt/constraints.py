"""Constraint handling for deck optimisation.

The real project would expose a rich set of deck-building rules.  For the
purposes of the exercise we enforce only a couple of soft constraints via a
numeric penalty so that the genetic algorithm can still explore the search
space while favouring saner decks.
"""

from engine.deck import Deck


EXPECTED_DECK_SIZE = 60
MIN_LANDS = 20


def constraint_penalty(deck: Deck) -> float:
    """Return a score representing how far ``deck`` is from simple rules."""

    penalty = 0.0

    size_diff = abs(len(deck.cards) - EXPECTED_DECK_SIZE)
    penalty += size_diff * 0.1

    land_count = sum(1 for c in deck.cards if "Land" in c.types)
    if land_count < MIN_LANDS:
        penalty += (MIN_LANDS - land_count) * 0.1

    return penalty
