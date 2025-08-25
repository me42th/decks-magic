# Título
Autor: Codex

## 1. Visão Rápida
- Objetivo atual: simular partidas no formato Horde de Magic: The Gathering e experimentar otimização de decks.
- Arquitetura:
  - `cli.py` expõe comandos de simulação e otimização.
  - `engine/` contém `cards.py`, `deck.py`, `game.py`, `autoplayer.py` e `horde_rules.py`.
  - `sim/runner.py` executa partidas determinísticas e gera métricas.
  - `opt/` aplica um algoritmo genético simples.
  - `decklist_txt_loader.py` e `store/decklist.py` tratam listas de cartas.
  - `api/` oferece exemplos de integração com FastAPI e a API oficial de cartas.
- Como iniciar em 5 minutos:
  1. `python -m venv .venv && source .venv/bin/activate`
  2. `pip install requests fastapi pytest`
  3. `python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5`

## 2. Ambiente e Dependências
- Gerenciamento via `pip`; não há `pyproject.toml`.
- Dependências principais: `requests`, `fastapi`, `pytest`.
- Problemas comuns: `ModuleNotFoundError: requests` → `pip install requests`.
- Não há arquivos `.env`; variáveis de ambiente não são usadas.

## 3. Modelagem de Domínio
- Cartas (`engine/cards.py`):
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
- Baralhos (`engine/deck.py`): validação de quantidade por card.
- Estado de jogo (`engine/game.py`): armazena bibliotecas, mão, campo e vida.

## 4. CLI
- Comando `simulate`:
```bash
python cli.py simulate --deck data/sample_deck.json --horde data/horde_basic.json --seeds 5
```
- Comando `optimize`:
```bash
python cli.py optimize --pop 5 --gens 2
```
- Saída: métricas em JSON; erros via exceções Python.

## 5. Parsing de Decklists
- Formatos suportados: JSON e texto plano.
- Texto plano (`decklist_txt_loader.py`):
```python
for linha in caminho.read_text().splitlines():
    interpretado = _interpretar_linha(linha)
    ...
```
- Integração com a API oficial (`store/decklist.py` usa `api/mgt_api.py`).
- Teste principal: `tests/test_decklist_txt_loader.py` cobre casos de parsing e mocks de rede.

## 6. Motor de Simulação
- Loop de jogo (`sim/runner.py`): três turnos fixos, milando a biblioteca da Horde.
- Autoplayer (`engine/autoplayer.py`) realiza compra, joga um terreno e uma magia.
- Métricas coletadas em `run`: `winrate`, `avg_turns`, `avg_damage`.

## 7. Formato Horda
- Regras em `engine/horde_rules.py`:
```python
revealed = reveal_until_non_token(horde_library)
... # tokens entram com ímpeto
mill(horde_lib, player_power)
```
- Danos ao jogador resultam da soma do poder das criaturas da Horde.

## 8. Padrões de Projeto e Arquitetura
- Uso de módulos funcionais e dataclasses simples.
- Padrão Strategy implícito na separação de `play_player_turn` e `play_horde_turn`.
- Antipadrões e refatorações:
  1. **Uso de `print` para avisos** (`decklist_txt_loader._buscar_carta`):
```python
except Exception as exc:
    print(f"Aviso: falha ao buscar carta '{nome}': {exc}")
```
    *Refatorar para logging*:
```python
import logging
logger = logging.getLogger(__name__)
...
except Exception as exc:
    logger.warning("falha ao buscar carta '%s': %s", nome, exc)
```
  2. **Loop de turnos rígido** (`sim/runner.run_game`):
```python
for _ in range(3):
    ...
```
    *Proposta*: parametrizar quantidade de turnos e interromper quando `state.life <= 0`.
  3. **Seleção de formato na CLI via condicional** (`cli.py.carregar_cartas`):
```python
if sufixo == ".json":
    ...
elif sufixo == ".txt":
    ...
```
    *Refatorar para dispatcher*:
```python
LOADERS = {".json": carregar_json, ".txt": carregar_baralho_txt}
def carregar_cartas(caminho: Path) -> List[Card]:
    try:
        return LOADERS[caminho.suffix.lower()](caminho)
    except KeyError:
        raise ValueError("Formato de baralho não suportado")
```

## 9. Testes e Qualidade
- Executar testes:
```bash
pytest
```
- Não há `ruff`, `flake8`, `black` ou `mypy`; recomenda-se adicioná-los.

## 10. Observabilidade e Erros
- Logging inexistente; substituir `print` por `logging`.
- Mensagens de erro atuais são propagadas por exceções padrão.

## 11. Produção
- Não há empacotamento via `pyproject.toml`; scripts são executados diretamente.
- Exemplo mínimo de Dockerfile multi-stage:
```dockerfile
FROM python:3.11-slim AS build
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

FROM python:3.11-slim
WORKDIR /app
COPY --from=build /usr/local /usr/local
CMD ["python", "cli.py"]
```
- CI/CD sugerido (GitHub Actions): lint, teste, build e publicação em artefatos.

## 12. Segurança e Licença
- Sem arquivo de licença definido.
- Dependências não pinadas; usar `requirements.txt` para fixar versões.

## 13. Roadmap de Manutenção
- Melhorar `sim/runner.py` com número de turnos configurável.
- Unificar parsing de decklists entre `decklist_txt_loader.py` e `store/decklist.py`.
- Adicionar logging estruturado e `pyproject.toml`.
- Convenções: mensagens de commit curtas em português; abrir PRs com testes.

## 14. Apêndices
- *Cheatsheet Python → PHP*:
  - `dataclasses` → não há equivalente direto; ver `engine/cards.py`.
  - Compreensão de listas em `cli.py` e `decklist_txt_loader.py`.
  - `Path` sobrecarrega `/` para concatenar (`tests/test_decklist_txt_loader.py`).
- *Fórmula hipergeométrica* para probabilidade de comprar pelo menos uma carta X:
  `1 - comb(N-K, n)/comb(N, n)`, onde `N` é tamanho do baralho, `K` cópias de X e `n` cartas compradas.
  - Exemplo: probabilidade de comprar pelo menos uma `Forest` nos 7 primeiros cards de um baralho de 60 com 20 `Forest`.
