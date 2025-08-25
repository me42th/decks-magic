# decks-magic

Base de estudo e manutenção de um simulador mínimo de Magic: The Gathering no
formato "Horde" e de um otimizador de decks. O repositório demonstra:

* uma micro engine de jogo com autoplayer determinístico;
* regras de Horde onde dano ao inimigo exila cartas do grimório;
* um algoritmo genético de exemplo que avalia decks simulando partidas; e
* um carregador de decklists em texto simples via API do MTG.

## Requisitos

Python 3.10+.

## Setup rápido

```bash
python -m venv .venv && source .venv/bin/activate
pip install requests fastapi pytest
```

## Como rodar

```bash
python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
python cli.py simulate --deck doctorWho_commander.txt --horde data/horde_basic.json --seeds 5 --logfile game.log
python cli.py optimize --pop 5 --gens 2
```

## Como testar

```bash
pytest
```

## Qualidade de código

Não há linters configurados; recomenda-se adicionar `ruff` ou `flake8` e
`black`.

## Contribuição

Abra uma issue ou pull request descrevendo sua mudança e inclua testes
reproduzíveis. Veja o guia completo em [`./books/BOOK-472.md`](./books/BOOK-472.md).

## Publicação

Nenhum processo automatizado de publicação está definido. Um exemplo de
Dockerfile multi-stage e pipeline de CI/CD encontra-se no livro.

## Licença

Ainda sem licença definida.
