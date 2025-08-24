import json
import random
from pathlib import Path
from typing import List

from engine.cards import Card
from engine.deck import Deck
from sim.runner import run, load_seed_bank
from .fitness import compute_fitness
from .constraints import constraint_penalty


sample_card = Card(
    id="sample",
    name="Sample Creature",
    cmc=1,
    types=["Creature"],
    colors=["C"],
    pt=(1, 1),
)

forest_card = Card(
    id="forest",
    name="Forest",
    cmc=0,
    types=["Basic", "Land"],
    colors=["G"],
    pt=None,
)


def _load_horde_cards() -> List[Card]:
    path = Path("data/horde_basic.json")
    data = json.loads(path.read_text())
    return [Card(**item) for item in data]


SEEDS = load_seed_bank(Path("sim/seed_bank.json"))[:5]
HORDE_CARDS = _load_horde_cards()


def init_population(p: int) -> List[Deck]:
    decklist = [sample_card] * 4 + [forest_card] * 56
    return [Deck(decklist) for _ in range(p)]


def evaluate(deck: Deck) -> dict:
    """Simulate ``deck`` against the basic Horde and compute metrics."""

    metrics = run(deck, SEEDS, HORDE_CARDS)
    metrics["penalties"] = constraint_penalty(deck)
    return metrics


def search_ga(pop: int, generations: int) -> Deck:
    population = init_population(pop)
    for _ in range(generations):
        scores = [(deck, compute_fitness(evaluate(deck))) for deck in population]
        scores.sort(key=lambda x: x[1], reverse=True)
        population = [d for d, _ in scores]
    return population[0]
