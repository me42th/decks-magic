import argparse
import json
from pathlib import Path
from typing import List

from engine.cards import Card
from engine.deck import Deck
from sim.runner import run
from opt.search_ga import search_ga


def carregar_cartas(caminho: Path) -> List[Card]:
    sufixo = caminho.suffix.lower()
    if sufixo == ".json":
        dados = json.loads(caminho.read_text())
        # Compreensão de lista com desempacotamento ``**`` de dicionário, algo inexistente em PHP.
        return [Card(**item) for item in dados]
    elif sufixo == ".txt":
        from decklist_txt_loader import carregar_baralho as carregar_baralho_txt

        return carregar_baralho_txt(caminho).cards
    else:
        raise ValueError(f"Formato de baralho não suportado: {sufixo}")


def carregar_baralho(caminho: Path) -> Deck:
    return Deck(carregar_cartas(caminho))


def comando_simular(argumentos: argparse.Namespace) -> None:
    baralho = carregar_baralho(Path(argumentos.deck))
    horda = carregar_cartas(Path(argumentos.horde))
    sementes = range(argumentos.seeds)  # ``range`` cria um iterador sem gerar uma lista inteira.
    metricas = run(baralho, sementes, horda, logfile=argumentos.logfile)
    print(json.dumps(metricas, indent=2))


def comando_otimizar(argumentos: argparse.Namespace) -> None:
    melhor = search_ga(argumentos.pop, argumentos.gens)
    print(f"Melhor baralho possui {len(melhor.cards)} cartas")


def principal() -> None:
    analisador = argparse.ArgumentParser(description="MTG Horde Lab MVP")
    subcomandos = analisador.add_subparsers(dest="cmd")

    parser_simular = subcomandos.add_parser("simulate")
    parser_simular.add_argument("--deck", required=True)
    parser_simular.add_argument("--horde", required=True)
    parser_simular.add_argument("--seeds", type=int, default=10)
    parser_simular.add_argument("--logfile")
    parser_simular.set_defaults(func=comando_simular)

    parser_otimizar = subcomandos.add_parser("optimize")
    parser_otimizar.add_argument("--pop", type=int, default=30)
    parser_otimizar.add_argument("--gens", type=int, default=5)
    parser_otimizar.set_defaults(func=comando_otimizar)

    argumentos = analisador.parse_args()
    if hasattr(argumentos, "func"):
        argumentos.func(argumentos)
    else:
        analisador.print_help()


if __name__ == "__main__":
    principal()
