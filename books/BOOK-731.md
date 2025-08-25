# Título
Autor: Codex

## 1. Visão Rápida
- **O que o projeto faz hoje:** simulador mínimo do formato "Horda" de Magic: The Gathering com otimizador genético e carregamento de decklists.
- **Mapa da arquitetura:**
  - `engine/` contém modelos de domínio como `Card`, `Deck` e regras de horda.
  - `sim/` executa partidas e coleta métricas.
  - `opt/` fornece busca genética.
  - `cli.py` expõe os comandos `simulate` e `optimize`.
  - `store/` e `decklist_txt_loader.py` tratam decklists e integração com API MTG.
- **Como iniciar em 5 minutos:**
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install requests fastapi pytest
  python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
  ```

## 2. Ambiente e Dependências
- Gerenciamento via `pip`; não há `requirements.txt` nem `poetry`.
- Dependências principais: `requests` para API MTG e `fastapi` para o servidor opcional.
- Problema comum: `ModuleNotFoundError: requests`. Solução:
  ```bash
  pip install requests
  ```
- Não há uso de `.env` ou variáveis de ambiente.

## 3. Modelagem de Domínio
- `engine/cards.py` define `Card`:
  ```python
  from dataclasses import dataclass
  from typing import List, Optional, Tuple

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
- `engine/deck.py` valida limite de quatro cópias:
  ```python
  class Deck:
      def __init__(self, cards: List[Card]):
          self.cards = cards
          self.validate()

      def validate(self) -> None:
          counts = Counter(card.id for card in self.cards)
          for card in self.cards:
              is_basic_land = "Basic" in card.types and "Land" in card.types
              if not is_basic_land and counts[card.id] > 4:
                  raise ValueError(f"Card {card.name} exceeds four-copy limit")
  ```
- `engine/game.py` modela o estado:
  ```python
  @dataclass
  class GameState:
      library: List[Card]
      hand: List[Card] = field(default_factory=list)
      battlefield: List[Card] = field(default_factory=list)
      graveyard: List[Card] = field(default_factory=list)
      life: int = 20
  ```
- `engine/horde_rules.py` implementa o turno da horda:
  ```python
  def play_horde_turn(state: GameState, horde_library: List[Card], rng: random.Random) -> None:
      revealed = reveal_until_non_token(horde_library)
      tokens = [c for c in revealed if "Token" in c.types]
      non_tokens = [c for c in revealed if "Token" not in c.types]
      state.battlefield.extend(tokens)
      if non_tokens:
          state.battlefield.extend(non_tokens)
      total_power = sum(card.pt[0] for card in state.battlefield if card.pt)
      state.life -= total_power
  ```

## 4. CLI
- Comandos:
  - `simulate` aceita `--deck`, `--horde`, `--seeds` e `--logfile`.
  - `optimize` aceita `--pop` e `--gens`.
- Saída em JSON com métricas; códigos de erro padrão do Python.
- Exemplo reproduzível:
  ```bash
  python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 2 --logfile jogo.log
  ```

## 5. Parsing de Decklists
- Formatos: `.json` e `.txt`.
- `.txt` usa MTG API para detalhes via `decklist_txt_loader.carregar_baralho`.
- Teste de parsing garante comportamento:
  ```python
  def teste_carregar_baralho_do_txt(monkeypatch, tmp_path: Path) -> None:
      monkeypatch.setattr("decklist_txt_loader.requests.get", obter_falso)
      arquivo_baralho = tmp_path / "deck.txt"
      arquivo_baralho.write_text("2 Forest\n")
      baralho = carregar_baralho(arquivo_baralho)
      assert len(baralho.cards) == 2
  ```

## 6. Motor de Simulação
- `sim/runner.py` executa turnos fixos:
  ```python
  for _ in range(3):
      events.extend(play_player_turn(state))
      player_power = sum(card.pt[0] for card in state.battlefield if card.pt)
      mill(horde_lib, player_power)
      play_horde_turn(state, horde_lib, rng)
  ```
- Métricas coletadas: `winrate`, `avg_turns`, `avg_damage`.
- Logs opcionais em JSON via `--logfile`.

## 7. Formato Horda
- Dano ao jogador reduz `life`; dano ao oponente mói o grimório (`mill`).
- Tokens têm ímpeto e atacam imediatamente.
- Difere do 1v1: a horda não possui vida, apenas biblioteca.

## 8. Padrões de Projeto e Arquitetura
- Separação modular favorece o padrão Strategy nas funções `constraint_penalty` e `compute_fitness`.
- **Refatorações sugeridas:**
  1. Parametrizar turnos na simulação:
     ```diff
     def run_game(deck: Deck, horde: List[Card], seed: int, logfile: str | None = None,
-               ) -> dict:
-    for _ in range(3):
+               turns: int = 3) -> dict:
+    for _ in range(turns):
         ...
     ```
  2. Usar `logging` em vez de `print` no carregador de deck:
     ```diff
     import logging
-    print(f"Aviso: carta '{nome}' não encontrada")
+    logger = logging.getLogger(__name__)
+    logger.warning("carta '%s' não encontrada", nome)
     ```
  3. Evitar import dinâmico em `cli.py`:
     ```diff
-    elif sufixo == ".txt":
-        from decklist_txt_loader import carregar_baralho as carregar_baralho_txt
-        return carregar_baralho_txt(caminho).cards
+    elif sufixo == ".txt":
+        return carregar_baralho_txt(caminho).cards
     ```
     ```python
     from decklist_txt_loader import carregar_baralho as carregar_baralho_txt
     ```

## 9. Testes e Qualidade
- Testes existentes: `tests/test_deck.py` e `tests/test_decklist_txt_loader.py`.
- Executar:
  ```bash
  pytest
  ```
- Não há linting configurado. Sugestão mínima `pyproject.toml`:
  ```toml
  [tool.black]
  line-length = 88

  [tool.ruff]
  select = ["E", "F"]
  ```
- Adotar `pre-commit` para padronizar qualidade.

## 10. Observabilidade e Erros
- Uso de `print` para avisos; não há logging estruturado.
- Sugestão:
  ```python
  import logging
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  logger.info("inicio da simulação")
  ```

## 11. Produção
- Não há `pyproject.toml` ou entry points; criar estrutura para empacotamento.
- Exemplo de `Dockerfile` multi-stage:
  ```Dockerfile
  FROM python:3.12-slim AS builder
  WORKDIR /app
  COPY . .
  RUN pip install --upgrade pip && pip install .

  FROM python:3.12-slim
  WORKDIR /app
  COPY --from=builder /usr/local /usr/local
  CMD ["python", "cli.py"]
  ```
- CI/CD sugerido (`.github/workflows/ci.yml`):
  ```yaml
  name: ci
  on: [push]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: '3.12'
        - run: pip install requests fastapi pytest
        - run: pytest
  ```

## 12. Segurança e Licença
- Dependências não pinadas; usar versões específicas em produção.
- Licença ausente; adotar MIT ou equivalente.

## 13. Roadmap de Manutenção
- Melhorar cobertura de testes para `engine/autoplayer.py` e `sim/runner.py`.
- Implementar logging estruturado em `decklist_txt_loader.py` e `cli.py`.
- Adicionar parametrização de turnos em `sim/runner.py`.
- Convenções: commits no padrão Conventional Commits, versionamento SemVer e `CHANGELOG.md`.
- Guia de PR: descreva objetivo, passos de teste e impactos.

## 14. Apêndices
- **Cheatsheet Python → PHP:**
  - `list` ↔ arrays; compreensão de listas não existe em PHP.
  - `with` para contextos; usar `try/finally` em PHP.
  - `venv` cria ambientes isolados; em PHP usar gerenciador como Composer.
- **Fórmula hipergeométrica:**
  \[ P(X = k) = \frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}} \]
  Útil para calcular chances de comprar cartas específicas no baralho.
