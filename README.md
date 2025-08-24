# decks-magic

Skeleton MVP for a Magic: The Gathering Horde simulator and optimizer.

## Setup

Requires Python 3.10+.

## CLI

Simulate a deck against the basic Horde:

```bash
python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
```

Run the (toy) genetic algorithm optimizer:

```bash
python cli.py optimize --pop 5 --gens 2
```

## Tests

```bash
pytest
```
