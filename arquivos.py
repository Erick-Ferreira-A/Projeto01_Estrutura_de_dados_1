"""Persistencia dos produtos em JSON."""

from __future__ import annotations

import json
from pathlib import Path

from produto import Produto


def salvar_produtos(caminho: str | Path, produtos: list[Produto]) -> None:
    """Salva produtos em arquivo JSON."""
    arquivo = Path(caminho)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    dados = [produto.para_dict() for produto in produtos]

    with arquivo.open("w", encoding="utf-8") as saida:
        json.dump(dados, saida, ensure_ascii=True, indent=2)


def carregar_produtos(caminho: str | Path) -> list[Produto]:
    """Carrega produtos de arquivo JSON."""
    arquivo = Path(caminho)
    if not arquivo.exists():
        return []

    with arquivo.open("r", encoding="utf-8") as entrada:
        dados = json.load(entrada)

    if not isinstance(dados, list):
        raise ValueError("Arquivo de dados deve conter uma lista de produtos.")

    return [Produto.de_dict(item) for item in dados]
