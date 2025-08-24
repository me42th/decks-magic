import random
from typing import List

from engine.cards import Card
from engine.deck import Deck
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


def init_population(p: int) -> List[Deck]:
    decklist = [sample_card] * 4 + [forest_card] * 56
    return [Deck(decklist) for _ in range(p)]


def evaluate(deck: Deck) -> dict:
    # Placeholder evaluation that returns random metrics
    return {
        "winrate": random.random(),
        "avg_turns": random.uniform(5, 10),
        "avg_damage": random.uniform(0, 20),
        "penalties": constraint_penalty(deck),
    }


def search_ga(pop: int, generations: int) -> Deck:
    population = init_population(pop)
    for _ in range(generations):
        scores = [(deck, compute_fitness(evaluate(deck))) for deck in population]
        scores.sort(key=lambda x: x[1], reverse=True)
        population = [d for d, _ in scores]
    return population[0]
