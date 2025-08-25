# decks-magic

Projeto base para estudo e manutenção de um simulador "Horde" de Magic: The Gathering.
O código é deliberadamente pequeno, mas demonstra um fluxo completo:

* a micro game engine with a deterministic autoplayer,
* Horde rules where damage to the Horde mills its library,
* a toy genetic algorithm that evaluates decks by simulating games, and
* a loader for plain-text deck lists using the MTG API (it falls back gracefully
  if the `requests` package is not installed).
## Instalação rápida

Requer Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install requests fastapi pytest
```

## Uso

Simular um baralho contra a horda básica:

```bash
python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
```

Simular usando uma lista em texto e registrar cada jogo:

```bash
python cli.py simulate --deck doctorWho_commander.txt --horde data/horde_basic.json --seeds 5 --logfile game.log
```

Executar o otimizador genético:

```bash
python cli.py optimize --pop 5 --gens 2
```

## Testes

```bash
pytest
```

## Contribuição

1. Faça um fork e crie um branch.
2. Execute `pytest` antes de enviar.
3. Abra um pull request descrevendo as mudanças.

## Publicação

Ainda não há pipeline de publicação. Um fluxo mínimo seria:

```bash
python -m build
```

## Documentação

Consulte [books/BOOK-731.md](books/BOOK-731.md) para detalhes completos do projeto.

## Licença

Nenhuma licença definida. Recomenda-se MIT.
