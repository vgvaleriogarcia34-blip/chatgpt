"""Entrypoint del agente de LinkedIn.

Uso:
    python main.py "Publica un post sobre IA aplicada a ventas B2B y gestiona los leads"
    python main.py --loop 3600 "Mantén una cadencia de 1 post diario y cualifica leads"
"""
from __future__ import annotations

import argparse
import asyncio

from linkedin_agent.agent import run_agent, run_loop


def main() -> None:
    parser = argparse.ArgumentParser(description="Agente autónomo de LinkedIn")
    parser.add_argument("objective", help="Objetivo del agente en lenguaje natural")
    parser.add_argument(
        "--loop",
        type=int,
        default=None,
        metavar="SECONDS",
        help="Si se indica, ejecuta el agente en bucle con este intervalo",
    )
    args = parser.parse_args()

    if args.loop:
        asyncio.run(run_loop(args.objective, interval_seconds=args.loop))
    else:
        asyncio.run(run_agent(args.objective))


if __name__ == "__main__":
    main()
