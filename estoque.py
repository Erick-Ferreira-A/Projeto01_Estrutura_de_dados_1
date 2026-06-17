"""Operacoes de estoque usando vetores ordenado e nao ordenado."""

from __future__ import annotations

from bisect import bisect_left

from produto import Produto, validar_codigo, validar_quantidade_venda


class Estoque:
    """Controla produtos, vendas e relatorios."""

    def __init__(self, produtos: list[Produto] | None = None) -> None:
        self.produtos: list[Produto] = []
        self.produtos_por_codigo: list[Produto] = []

        if produtos:
            for produto in produtos:
                self.cadastrar(produto)

    def cadastrar(self, produto: Produto) -> None:
        """Cadastra produto novo, mantendo codigo unico."""
        if self.buscar_por_codigo(produto.codigo) is not None:
            raise ValueError("Ja existe produto com esse codigo.")

        self.produtos.append(produto)
        posicao = self._posicao_insercao(produto.codigo)
        self.produtos_por_codigo.insert(posicao, produto)

    def editar(
        self,
        codigo: int | str,
        nome: str | None = None,
        categoria: str | None = None,
        preco: float | None = None,
        quantidade: int | None = None,
    ) -> Produto:
        """Edita um produto pelo codigo."""
        produto = self._obter_por_codigo(codigo)
        produto.atualizar(
            nome=nome,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
        )
        return produto

    def remover(self, codigo: int | str) -> Produto:
        """Remove produto pelo codigo."""
        produto = self._obter_por_codigo(codigo)
        self.produtos.remove(produto)
        indice = self._indice_por_codigo(produto.codigo)
        self.produtos_por_codigo.pop(indice)
        return produto

    def buscar_por_codigo(self, codigo: int | str) -> Produto | None:
        """Busca produto por codigo usando busca binaria O(log n)."""
        indice = self._indice_por_codigo(codigo)
        if indice == -1:
            return None
        return self.produtos_por_codigo[indice]

    def buscar_por_nome(self, termo: str) -> list[Produto]:
        """Busca produtos por nome usando busca linear O(n)."""
        termo_normalizado = termo.strip().lower()
        if not termo_normalizado:
            raise ValueError("Termo de busca nao pode ficar vazio.")

        encontrados = []
        for produto in self.produtos:
            if termo_normalizado in produto.nome.lower():
                encontrados.append(produto)
        return encontrados

    def registrar_venda(self, codigo: int | str, quantidade: int | str) -> Produto:
        """Registra venda e reduz estoque."""
        produto = self._obter_por_codigo(codigo)
        quantidade_validada = validar_quantidade_venda(quantidade)
        produto.registrar_saida(quantidade_validada)
        return produto

    def listar_ordenado_por_codigo(self) -> list[Produto]:
        """Retorna copia dos produtos ordenados por codigo."""
        return list(self.produtos_por_codigo)

    def listar_por_categoria(self, categoria: str) -> list[Produto]:
        """Filtra produtos pela categoria informada."""
        categoria_normalizada = categoria.strip().lower()
        if not categoria_normalizada:
            raise ValueError("Categoria nao pode ficar vazia.")

        return [
            produto
            for produto in self.produtos
            if produto.categoria.lower() == categoria_normalizada
        ]

    def relatorio_estoque_baixo(self, limite: int | str) -> list[Produto]:
        """Lista produtos com quantidade menor que o limite."""
        try:
            limite_int = int(limite)
        except (TypeError, ValueError) as exc:
            raise ValueError("Limite deve ser um numero inteiro.") from exc

        if limite_int < 0:
            raise ValueError("Limite nao pode ser negativo.")

        return [
            produto
            for produto in self.produtos_por_codigo
            if produto.quantidade < limite_int
        ]

    def menor_preco(self) -> Produto | None:
        """Retorna produto com menor preco."""
        if not self.produtos:
            return None
        return min(self.produtos, key=lambda produto: produto.preco)

    def maior_preco(self) -> Produto | None:
        """Retorna produto com maior preco."""
        if not self.produtos:
            return None
        return max(self.produtos, key=lambda produto: produto.preco)

    def substituir_todos(self, produtos: list[Produto]) -> None:
        """Substitui dados do estoque validando codigos duplicados."""
        novo_estoque = Estoque(produtos)
        self.produtos = novo_estoque.produtos
        self.produtos_por_codigo = novo_estoque.produtos_por_codigo

    def total_produtos(self) -> int:
        """Retorna total de itens cadastrados."""
        return len(self.produtos)

    def _obter_por_codigo(self, codigo: int | str) -> Produto:
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            raise ValueError("Produto nao encontrado.")
        return produto

    def _indice_por_codigo(self, codigo: int | str) -> int:
        codigo_validado = validar_codigo(codigo)
        esquerda = 0
        direita = len(self.produtos_por_codigo) - 1

        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            codigo_meio = self.produtos_por_codigo[meio].codigo

            if codigo_meio == codigo_validado:
                return meio
            if codigo_meio < codigo_validado:
                esquerda = meio + 1
            else:
                direita = meio - 1

        return -1

    def _posicao_insercao(self, codigo: int) -> int:
        codigos = [produto.codigo for produto in self.produtos_por_codigo]
        return bisect_left(codigos, codigo)
