import tempfile
import unittest
from pathlib import Path

from arquivos import carregar_produtos, salvar_produtos
from estoque import Estoque
from produto import Produto


class EstoqueTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.estoque = Estoque(
            [
                Produto(30, "Mouse USB", "Informatica", 39.90, 10),
                Produto(10, "Caderno", "Papelaria", 18.90, 20),
                Produto(20, "Caneta Azul", "Papelaria", 2.50, 50),
            ]
        )

    def test_cadastro_mantem_vetor_ordenado_por_codigo(self) -> None:
        codigos = [
            produto.codigo
            for produto in self.estoque.listar_ordenado_por_codigo()
        ]
        self.assertEqual(codigos, [10, 20, 30])

    def test_nao_permite_codigo_duplicado(self) -> None:
        with self.assertRaises(ValueError):
            self.estoque.cadastrar(
                Produto(10, "Outro Caderno", "Papelaria", 20.00, 5)
            )

    def test_busca_por_codigo_encontra_produto(self) -> None:
        produto = self.estoque.buscar_por_codigo(20)
        self.assertIsNotNone(produto)
        self.assertEqual(produto.nome, "Caneta Azul")

    def test_busca_por_nome_usa_termo_parcial(self) -> None:
        encontrados = self.estoque.buscar_por_nome("caneta")
        self.assertEqual(len(encontrados), 1)
        self.assertEqual(encontrados[0].codigo, 20)

    def test_venda_reduz_estoque(self) -> None:
        produto = self.estoque.registrar_venda(30, 3)
        self.assertEqual(produto.quantidade, 7)

    def test_venda_com_estoque_insuficiente_falha(self) -> None:
        with self.assertRaises(ValueError):
            self.estoque.registrar_venda(30, 99)

    def test_filtro_categoria_e_estoque_baixo(self) -> None:
        papelaria = self.estoque.listar_por_categoria("papelaria")
        baixo = self.estoque.relatorio_estoque_baixo(15)
        self.assertEqual({produto.codigo for produto in papelaria}, {10, 20})
        self.assertEqual({produto.codigo for produto in baixo}, {30})

    def test_edicao_e_remocao(self) -> None:
        editado = self.estoque.editar(
            10,
            nome="Caderno Brochura",
            preco=12.90,
            quantidade=15,
            categoria="Papelaria",
        )
        removido = self.estoque.remover(20)

        self.assertEqual(editado.nome, "Caderno Brochura")
        self.assertEqual(removido.codigo, 20)
        self.assertIsNone(self.estoque.buscar_por_codigo(20))

    def test_persistencia_json(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "produtos.json"
            salvar_produtos(caminho, self.estoque.listar_ordenado_por_codigo())
            carregados = carregar_produtos(caminho)

        self.assertEqual(len(carregados), 3)
        self.assertEqual(carregados[0].codigo, 10)


if __name__ == "__main__":
    unittest.main()
