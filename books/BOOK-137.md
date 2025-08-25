# decks-magic: Guia de Estudo e Manutenção
Autor: Codex

## 1. Visão Rápida
### O que o projeto faz hoje
- Simula partidas simplificadas de Magic: The Gathering no formato Horde.
- Avalia baralhos com um algoritmo genético.
- Carrega listas de cartas em JSON ou texto consultando a API oficial.

### Mapa da arquitetura
- `cli.py`: interface de linha de comando.
- `engine/`: núcleo do jogo (`cards.py`, `deck.py`, `game.py`, `autoplayer.py`, `horde_rules.py`).
- `sim/`: execução de partidas (`runner.py`).
- `opt/`: algoritmo genético e constraints.
- `store/decklist.py` e `decklist_txt_loader.py`: parsing de decklists e integração com API.
- `api/`: esqueleto FastAPI.

### Como iniciar em 5 minutos
```bash
python -m venv .venv
source .venv/bin/activate
pip install requests fastapi
python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
```

## 2. Ambiente e Dependências
- Gestão via `pip`. Não há `requirements.txt`; instale manualmente.
- Falta de `requests` gera `RuntimeError` em `decklist_txt_loader.py`.
- Variáveis de ambiente: nenhuma exigida; logs opcionais via `--logfile`.

## 3. Modelagem de Domínio
### Card (`engine/cards.py`)
```python
@dataclass(frozen=True)
class Card:
    id: str
    name: str
    cmc: int
    types: List[str]
    colors: List[str]
    pt: Optional[Tuple[int, int]] = None
    text_dsl: str = ""
```
### Deck (`engine/deck.py`)
```python
class Deck:
    def validate(self) -> None:
        counts = Counter(card.id for card in self.cards)
        ...
        if not is_basic_land and counts[card.id] > 4:
            raise ValueError(f"Card {card.name} exceeds four-copy limit")
```
### GameState (`engine/game.py`)
```python
@dataclass
class GameState:
    library: List[Card]
    hand: List[Card] = field(default_factory=list)
    battlefield: List[Card] = field(default_factory=list)
    graveyard: List[Card] = field(default_factory=list)
    life: int = 20
```
Invariantes: `Deck` aplica limite de quatro cópias; `GameState.life` deve permanecer >=0.

## 4. CLI
Arquivo `cli.py` define dois comandos:
- `simulate`: executa partidas entre baralho e horda.
- `optimize`: roda o algoritmo genético.
Exemplo reprodutível:
```bash
python cli.py simulate --deck doctorWho_commander.txt --horde data/horde_basic.json --seeds 5 --logfile game.log
```
Códigos de saída: 0 em sucesso; exceções não tratadas propagam.

## 5. Parsing de Decklists
Suporta:
- JSON nativo (lista de cartas).
- Texto via `decklist_txt_loader.py`, utilizando `requests`:
```python
def carregar_baralho(caminho: Path) -> Deck:
    ...
    carta = _buscar_carta(nome)
    if carta is None:
        continue
    cartas.extend([carta] * quantidade)
```
Tests: `tests/test_decklist_txt_loader.py` cobre casos de sucesso e falhas.

## 6. Motor de Simulação
`sim/runner.py` processa turnos:
```python
for _ in range(3):
    events.extend(play_player_turn(state))
    player_power = sum(card.pt[0] for card in state.battlefield if card.pt)
    mill(horde_lib, player_power)
    ...
    play_horde_turn(state, horde_lib, rng)
```
Métricas retornadas por `run`: `winrate`, `avg_turns`, `avg_damage`. Cada partida usa seeds determinísticas.

## 7. Formato Horda
`engine/horde_rules.py` implementa regras:
- `reveal_until_non_token` revela cartas até achar não-token.
- `mill` aplica dano como moagem do grimório.
- `play_horde_turn` faz tokens com ímpeto e causa dano com todas criaturas.

## 8. Padrões de Projeto e Arquitetura
- `Deck.validate` funciona como *guard clause* simples.
- `search_ga` usa abordagem de *Strategy* ao combinar `compute_fitness` e `constraint_penalty`.
- `store/decklist.py` é um *Repository* para loaders de baralho.

### Antipadrões e refatorações
1. **Uso de `print` para avisos**
   Antes (`decklist_txt_loader.py`):
   ```python
   if not dados:
       print(f"Aviso: carta '{nome}' não encontrada")
   ...
   except Exception as exc:
       print(f"Aviso: falha ao buscar carta '{nome}': {exc}")
   ```
   Depois (proposta):
   ```python
   import logging
   logger = logging.getLogger(__name__)
   ...
   if not dados:
       logger.warning("carta '%s' não encontrada", nome)
   ...
   except Exception as exc:
       logger.warning("falha ao buscar carta '%s': %s", nome, exc)
   ```

2. **Constantes globais em `opt/search_ga.py`**
   Antes:
   ```python
   SEEDS = load_seed_bank(Path("sim/seed_bank.json"))[:5]
   HORDE_CARDS = _load_horde_cards()
   def evaluate(deck: Deck) -> dict:
       metrics = run(deck, SEEDS, HORDE_CARDS)
   ```
   Depois:
   ```python
   def evaluate(deck: Deck, seeds: List[int], horde: List[Card]) -> dict:
       metrics = run(deck, seeds, horde)
   ```
   `search_ga` passa `seeds` e `horde` como parâmetros, permitindo testes isolados.

3. **Duplicação em `engine/autoplayer.py`**
   Antes:
   ```python
   def _play_first_of_type(state, card_type):
       ...
   def _play_first_non_land(state):
       ...
   ```
   Depois:
   ```python
   def _play_first(state: GameState, pred: Callable[[Card], bool]):
       for idx, card in enumerate(state.hand):
           if pred(card):
               state.battlefield.append(state.hand.pop(idx))
               return {"event": "play", "card": card.name}
       return None
   ```
   Chamadas:
   ` _play_first(state, lambda c: "Land" in c.types)` e `_play_first(state, lambda c: "Land" not in c.types)`.

4. **Loop fixo de 3 turnos em `sim/runner.py`** (extra)
   Antes:
   ```python
   for _ in range(3):
       ...
   ```
   Depois:
   ```python
   while state.life > 0 and horde_lib:
       ...
   ```
   Permite terminar quando o jogo acaba.

## 9. Testes e Qualidade
- `pytest` com exemplos em `tests/`.
- Não há cobertura ou property-based; podem ser adicionados com `hypothesis`.
- Ferramentas recomendadas:
  ```bash
  pip install black ruff mypy pre-commit
  pre-commit run --files engine/cards.py
  ```

## 10. Observabilidade e Erros
- Não há logging estruturado; maioria das mensagens usa `print`.
- Sugestão: padronizar `logging` com níveis e prefixo de módulo.
- Erros críticos propagam como exceções, facilitando falha rápida.

## 11. Produção
- Não existe `pyproject.toml`. Exemplo mínimo:
  ```toml
  [project]
  name = "decks-magic"
  version = "0.1.0"
  dependencies = ["requests", "fastapi"]
  [project.scripts]
  decks-magic = "cli:principal"
  ```
- Dockerfile multi-stage sugerido:
  ```Dockerfile
  FROM python:3.11-slim AS build
  WORKDIR /app
  COPY . .
  RUN pip install --user --upgrade build && python -m build

  FROM python:3.11-slim
  WORKDIR /app
  COPY --from=build /root/.cache/pypoetry/... /app  # ajustar conforme packaging
  CMD ["python", "cli.py", "simulate", "--help"]
  ```
- CI/CD (GitHub Actions) simplificado:
  ```yaml
  name: ci
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-python@v4
          with: {python-version: '3.11'}
        - run: pip install -r requirements.txt || true
        - run: pytest
  ```

## 12. Segurança e Licença
- Sem arquivo de licença: defina ex. MIT.
- Dependências não fixadas; crie `requirements.txt` com versões e use `pip install -r requirements.txt`.
- Atualize regularmente para correções de segurança.

## 13. Roadmap de Manutenção
- Adicionar logging estruturado em `decklist_txt_loader.py` e `sim/runner.py`.
- Parametrizar sementes e hordas em `opt/search_ga.py` para facilitar testes.
- Encerrar jogos dinamicamente em `sim/runner.py`.
- Criar `pyproject.toml` e `Dockerfile` oficiais.
- Cobrir `engine/autoplayer.py` com testes.
- Convenções: commits no formato *feat/fix/docs*, versionamento semântico, `CHANGELOG.md`.

## 14. Apêndices
### Cheatsheet Python para quem vem de PHP
- Compreensão de lista: `[Card(**item) for item in dados]`.
- `dataclasses` fornecem `__init__` e `__repr__`.
- Operador `/` em `Path`: `tmp_path / "deck.txt"`.
- Tipagem estática via `List[Card]` e `Optional[str]`.
- Context manager:
  ```python
  with open("arquivo") as f:
      conteudo = f.read()
  ```

### Fórmulas úteis
Distribuição hipergeométrica para draws:
\[
P(X = k) = \frac{\binom{K}{k} \binom{N-K}{n-k}}{\binom{N}{n}}
\]
Exemplo em Python para chance de 1 terreno nas 7 primeiras cartas de um baralho com 20 terrenos:
```python
from math import comb
def hypergeom(K, N, n, k):
    return comb(K, k) * comb(N-K, n-k) / comb(N, n)
prob = hypergeom(20, 60, 7, 1)
```
Use para avaliar mulligans no simulador.
