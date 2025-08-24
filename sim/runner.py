import json
import random
from pathlib import Path
from typing import Iterable, List

from engine.cards import Card
from engine.deck import Deck
from engine.game import GameState
from engine.autoplayer import play_player_turn
from engine.horde_rules import play_horde_turn, mill


def load_seed_bank(path: Path) -> List[int]:
    return json.loads(path.read_text())


def run_game(
    deck: Deck, horde: List[Card], seed: int, logfile: str | None = None
) -> dict:
    rng = random.Random(seed)
    state = GameState(library=list(deck.cards), life=20)
    horde_lib = list(horde)
    events = []

    # Play three turns as placeholder
    for _ in range(3):
        events.extend(play_player_turn(state))

        # Player creatures always attack; damage mills the Horde library
        player_power = sum(card.pt[0] for card in state.battlefield if card.pt)
        mill(horde_lib, player_power)
        events.append({"event": "player_attack", "damage": player_power, "horde_size": len(horde_lib)})

        life_before = state.life
        play_horde_turn(state, horde_lib, rng)
        damage = life_before - state.life
        events.append({"event": "horde_attack", "damage": damage, "life": state.life})

    if logfile:
        Path(logfile).write_text(json.dumps(events, indent=2))
    return {"won": state.life > 0, "life": state.life, "turns": 3}


def run(
    deck: Deck, seeds: Iterable[int], horde: List[Card], logfile: str | None = None
) -> dict:
    results = [run_game(deck, horde, s, logfile) for s in seeds]
    winrate = sum(r["won"] for r in results) / len(results)
    avg_turns = sum(r["turns"] for r in results) / len(results)
    avg_damage = sum(20 - r["life"] for r in results) / len(results)
    return {
        "winrate": winrate,
        "avg_turns": avg_turns,
        "avg_damage": avg_damage,
    }
