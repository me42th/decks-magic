import json
from pathlib import Path
from typing import List, Optional, Tuple
from types import SimpleNamespace

try:  # pragma: no cover - utilizado em testes com monkeypatch
    import requests as _requests
except Exception:  # ``requests`` pode não estar instalado em ambientes mínimos
    _requests = None

# ``requests`` é exposto como um objeto de módulo para que testes e usuários
# possam "monkeypatchar" ``requests.get`` mesmo se a biblioteca real não
# estiver disponível.
def _obter_requisicoes_ausente(*args, **kwargs):  # pragma: no cover - fallback simples
    raise RuntimeError("a biblioteca requests é necessária para buscar dados de cartas")

# ``SimpleNamespace`` cria um objeto com atributos dinâmicos, recurso sem
# equivalente direto em PHP.
requests = _requests or SimpleNamespace(get=_obter_requisicoes_ausente)

from engine.cards import Card
from engine.deck import Deck

URL_API = "https://api.magicthegathering.io/v1/cards"


def _interpretar_linha(linha: str) -> Optional[tuple[int, str]]:
    linha = linha.strip()
    if not linha or linha.startswith("#"):
        return None
    partes = linha.split(" ", 1)
    if len(partes) != 2:
        return None
    qtd_str, nome = partes
    try:
        quantidade = int(qtd_str)
    except ValueError:
        return None
    return quantidade, nome.strip()


def _buscar_carta(nome: str) -> Optional[Card]:
    try:
        resposta = requests.get(URL_API, params={"name": nome}, timeout=10)
        resposta.raise_for_status()  # mantemos o nome do método para compatibilidade com ``requests``
        dados = resposta.json().get("cards", [])
        if not dados:
            print(f"Aviso: carta '{nome}' não encontrada")
            return None
        dados_carta = dados[0]
        poder = dados_carta.get("power")
        resistencia = dados_carta.get("toughness")
        pontos: Optional[Tuple[int, int]] = None
        try:
            if poder is not None and resistencia is not None:
                pontos = (int(poder), int(resistencia))
        except ValueError:
            pontos = None
        return Card(
            id=dados_carta.get("id", nome),
            name=dados_carta.get("name", nome),
            cmc=int(dados_carta.get("cmc", 0)),
            types=dados_carta.get("types", []),
            colors=dados_carta.get("colors", []),
            pt=pontos,
            text_dsl=dados_carta.get("text", ""),
        )
    except Exception as exc:
        print(f"Aviso: falha ao buscar carta '{nome}': {exc}")
        return None


def carregar_baralho(caminho: Path) -> Deck:
    cartas: List[Card] = []  # anotação de tipo com genéricos; PHP não possui equivalente direto
    # ``Path.read_text`` lê todo o conteúdo do arquivo; em PHP normalmente usaríamos ``file_get_contents``.
    for linha in caminho.read_text().splitlines():
        interpretado = _interpretar_linha(linha)
        if not interpretado:
            continue
        quantidade, nome = interpretado
        carta = _buscar_carta(nome)
        if carta is None:
            continue
        # Multiplicar uma lista por um inteiro replica seus elementos; em PHP seria necessário um laço.
        cartas.extend([carta] * quantidade)
    return Deck(cartas)
