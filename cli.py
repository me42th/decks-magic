import argparse
import json
from pathlib import Path
from typing import List

from engine.cards import Card
from engine.deck import Deck
from sim.runner import run
from opt.search_ga import search_ga


def load_cards(path: Path) -> List[Card]:
    data = json.loads(path.read_text())
    return [Card(**item) for item in data]


def load_deck(path: Path) -> Deck:
    return Deck(load_cards(path))


def cmd_simulate(args: argparse.Namespace) -> None:
    deck = load_deck(Path(args.deck))
    horde = load_cards(Path(args.horde))
    seeds = range(args.seeds)
    metrics = run(deck, seeds, horde)
    print(json.dumps(metrics, indent=2))


def cmd_optimize(args: argparse.Namespace) -> None:
    best = search_ga(args.pop, args.gens)
    print(f"Best deck has {len(best.cards)} cards")


def main() -> None:
    parser = argparse.ArgumentParser(description="MTG Horde Lab MVP")
    sub = parser.add_subparsers(dest="cmd")

    sim_p = sub.add_parser("simulate")
    sim_p.add_argument("--deck", required=True)
    sim_p.add_argument("--horde", required=True)
    sim_p.add_argument("--seeds", type=int, default=10)
    sim_p.set_defaults(func=cmd_simulate)

    opt_p = sub.add_parser("optimize")
    opt_p.add_argument("--pop", type=int, default=30)
    opt_p.add_argument("--gens", type=int, default=5)
    opt_p.set_defaults(func=cmd_optimize)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
