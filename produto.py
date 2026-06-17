"""Modelo e validacoes de produto."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Produto:
    """Representa um produto do estoque."""

    codigo: int
    nome: str
    categoria: str
    preco: float
    quantidade: int

    def __post_init__(self) -> None:
        self.codigo = validar_codigo(self.codigo)
        self.nome = validar_texto(self.nome, "nome")
        self.categoria = validar_texto(self.categoria, "categoria")
        self.preco = validar_preco(self.preco)
        self.quantidade = validar_quantidade(self.quantidade)

    def atualizar(
        self,
        nome: str | None = None,
        categoria: str | None = None,
        preco: float | None = None,
        quantidade: int | None = None,
    ) -> None:
        """Atualiza campos editaveis do produto."""
        if nome is not None:
            self.nome = validar_texto(nome, "nome")
        if categoria is not None:
            self.categoria = validar_texto(categoria, "categoria")
        if preco is not None:
            self.preco = validar_preco(preco)
        if quantidade is not None:
            self.quantidade = validar_quantidade(quantidade)

    def registrar_saida(self, quantidade: int) -> None:
        """Reduz o estoque do produto apos uma venda."""
        quantidade = validar_quantidade_venda(quantidade)
        if quantidade > self.quantidade:
            raise ValueError("Estoque insuficiente para a venda.")
        self.quantidade -= quantidade

    def para_dict(self) -> dict[str, int | str | float]:
        """Converte o produto para um dicionario serializavel."""
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade,
        }

    @classmethod
    def de_dict(cls, dados: dict[str, object]) -> "Produto":
        """Cria produto a partir de um dicionario."""
        return cls(
            codigo=int(dados["codigo"]),
            nome=str(dados["nome"]),
            categoria=str(dados["categoria"]),
            preco=float(dados["preco"]),
            quantidade=int(dados["quantidade"]),
        )


def validar_codigo(codigo: int | str) -> int:
    """Valida codigo numerico positivo."""
    try:
        codigo_int = int(codigo)
    except (TypeError, ValueError) as exc:
        raise ValueError("Codigo deve ser um numero inteiro.") from exc

    if codigo_int <= 0:
        raise ValueError("Codigo deve ser positivo.")
    return codigo_int


def validar_texto(valor: str, campo: str) -> str:
    """Valida campos de texto obrigatorios."""
    texto = str(valor).strip()
    if not texto:
        raise ValueError(f"{campo.capitalize()} nao pode ficar vazio.")
    return texto


def validar_preco(preco: float | str) -> float:
    """Valida preco positivo."""
    try:
        preco_float = float(str(preco).replace(",", "."))
    except (TypeError, ValueError) as exc:
        raise ValueError("Preco deve ser um numero.") from exc

    if preco_float <= 0:
        raise ValueError("Preco deve ser positivo.")
    return round(preco_float, 2)


def validar_quantidade(quantidade: int | str) -> int:
    """Valida quantidade maior ou igual a zero."""
    try:
        quantidade_int = int(quantidade)
    except (TypeError, ValueError) as exc:
        raise ValueError("Quantidade deve ser um numero inteiro.") from exc

    if quantidade_int < 0:
        raise ValueError("Quantidade nao pode ser negativa.")
    return quantidade_int


def validar_quantidade_venda(quantidade: int | str) -> int:
    """Valida quantidade de venda maior que zero."""
    quantidade_int = validar_quantidade(quantidade)
    if quantidade_int <= 0:
        raise ValueError("Quantidade da venda deve ser maior que zero.")
    return quantidade_int
