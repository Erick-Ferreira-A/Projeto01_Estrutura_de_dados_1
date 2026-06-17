"""Logs simples de operacoes do sistema."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def registrar_log(caminho: str | Path, mensagem: str) -> None:
    """Registra uma linha de log com data e hora."""
    arquivo = Path(caminho)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with arquivo.open("a", encoding="utf-8") as saida:
        saida.write(f"[{data_hora}] {mensagem}\n")
