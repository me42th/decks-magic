import json
import random
from pathlib import Path
from typing import Iterable, List

from engine.cards import Card
from engine.deck import Deck
from engine.game import GameState
from engine.autoplayer import play_player_turn
from engine.horde_rules import play_horde_turn


CARD_SAMPLE = Card("token", "Zombie Token", 0, ["Token", "Creature", "Zombie"], [], (2, 2))


def load_seed_bank(path: Path) -> List[int]:
    return json.loads(path.read_text())


def run_game(deck: Deck, horde: List[Card], seed: int) -> dict:
    rng = random.Random(seed)
    state = GameState(library=list(deck.cards), life=20)
    horde_lib = list(horde)
    # Play three turns as placeholder
    for _ in range(3):
        play_player_turn(state)
        play_horde_turn(state, horde_lib, rng)
    return {"won": state.life > 0, "life": state.life, "turns": 3}


def run(deck: Deck, seeds: Iterable[int], horde: List[Card]) -> dict:
    results = [run_game(deck, horde, s) for s in seeds]
    winrate = sum(r["won"] for r in results) / len(results)
    avg_turns = sum(r["turns"] for r in results) / len(results)
    avg_damage = sum(20 - r["life"] for r in results) / len(results)
    return {
        "winrate": winrate,
        "avg_turns": avg_turns,
        "avg_damage": avg_damage,
    }
