import json
import random
from pathlib import Path
from typing import Iterable, List

from engine.cards import Card
from engine.deck import Deck
from engine.game import GameState
from engine.horde_rules import play_horde_turn


CARD_SAMPLE = Card("token", "Zombie Token", 0, ["Token", "Creature", "Zombie"], [], (2, 2))


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
        if state.library:
            drawn = state.library.pop(0)
            state.hand.append(drawn)
            events.append({"event": "draw", "card": drawn.name})
        if state.hand:
            played = state.hand.pop(0)
            state.battlefield.append(played)
            events.append({"event": "play", "card": played.name})
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
