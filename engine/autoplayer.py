"""Utility functions for driving the player's actions.

The goal of this module is *not* to be a perfect Magic autoplayer, but to
provide a slightly more useful heuristic than "play the first card".  The
logic implemented here is intentionally small: draw a card, play one land if
available, then play the first non-land card from the hand.  No mana system or
advanced decision making is modelled; the intent is simply to give the search
and simulation modules something deterministic to work with.
"""

from __future__ import annotations

from typing import List, Dict

from .game import GameState


def _play_first_of_type(state: GameState, card_type: str) -> Dict[str, str] | None:
    """Remove and play the first card of a given type from the hand.

    Parameters
    ----------
    state:
        The current :class:`GameState`.
    card_type:
        Type to search for, e.g. ``"Land"``.

    Returns
    -------
    dict | None
        Event describing the play, or ``None`` if no card of that type was
        found.
    """

    for idx, card in enumerate(state.hand):
        if card_type in card.types:
            state.battlefield.append(state.hand.pop(idx))
            return {"event": "play", "card": card.name}
    return None


def _play_first_non_land(state: GameState) -> Dict[str, str] | None:
    for idx, card in enumerate(state.hand):
        if "Land" not in card.types:
            state.battlefield.append(state.hand.pop(idx))
            return {"event": "play", "card": card.name}
    return None


def play_player_turn(state: GameState) -> List[Dict[str, str]]:
    """Execute a very small subset of a player's turn.

    The function returns a list of event dictionaries that the simulator can
    log.  Each run consists of a draw step followed by at most one land play
    and one non-land play.
    """

    events: List[Dict[str, str]] = []

    if state.library:
        drawn = state.library.pop(0)
        state.hand.append(drawn)
        events.append({"event": "draw", "card": drawn.name})

    land_event = _play_first_of_type(state, "Land")
    if land_event:
        events.append(land_event)

    spell_event = _play_first_non_land(state)
    if spell_event:
        events.append(spell_event)

    return events
