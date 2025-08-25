# decks-magic

Simulador mínimo de Magic: The Gathering no formato Horde. O repositório serve como base de estudo e manutenção do código.

## Requisitos

- Python 3.10+
- Dependências opcionais: `requests` para buscar cartas em decklists `.txt` e `fastapi` para o endpoint `api/`.

## Setup rápido

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # inexistente; instale as libs manualmente
```

## Como rodar

Simular um baralho contra a horda básica:

```bash
python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
```

Com decklist em texto e log em arquivo:

```bash
python cli.py simulate --deck doctorWho_commander.txt --horde data/horde_basic.json --seeds 5 --logfile game.log
```

Rodar o otimizador genético:

```bash
python cli.py optimize --pop 5 --gens 2
```

## Testes

```bash
pytest
```

## Qualidade de código

Não há linter ou formatter configurado. Recomenda-se `black`, `ruff` e `mypy`.

## Contribuição

- Crie branches a partir de `main`.
- Adicione testes para novos recursos.
- Envie pull requests curtos e com mensagens de commit objetivas.

## Publicação

Ainda não há `pyproject.toml` ou processo de build. Consulte o livro para um exemplo mínimo.

## Licença

Nenhuma licença foi fornecida; defina uma antes de publicar.

## Documentação

Leia [books/BOOK-137.md](books/BOOK-137.md) para detalhes completos.
