from .game import GameState


def play_player_turn(state: GameState) -> None:
    """A naive autoplayer that draws and plays the first card."""
    if state.library:
        state.hand.append(state.library.pop(0))
    if state.hand:
        card = state.hand.pop(0)
        state.battlefield.append(card)
