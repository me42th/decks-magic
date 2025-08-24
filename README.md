# decks-magic

Skeleton MVP for a Magic: The Gathering Horde simulator and optimizer.

## Setup

Requires Python 3.10+.

## CLI

The command-line interface accepts deck and horde lists in JSON or plain text
formats. When a `.txt` deck list is used, card details are fetched from the
Magic: The Gathering API.

Simulate a deck against the basic Horde:

```bash
python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
```

Simulate using a text deck list and log each game to a file:

```bash
python cli.py simulate --deck doctorWho_commander.txt --horde data/horde_basic.json --seeds 5 --logfile game.log
```

Run the (toy) genetic algorithm optimizer:

```bash
python cli.py optimize --pop 5 --gens 2
```

## Tests

```bash
pytest
```
