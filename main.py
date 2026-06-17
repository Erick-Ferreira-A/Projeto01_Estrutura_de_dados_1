"""Interface de linha de comando para estoque e vendas."""

from __future__ import annotations

from pathlib import Path

from arquivos import carregar_produtos, salvar_produtos
from estoque import Estoque
from logger_operacoes import registrar_log
from produto import Produto


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "dados" / "produtos.json"
ARQUIVO_LOG = BASE_DIR / "logs" / "operacoes.log"
TAMANHO_PAGINA = 5


def ler_texto(rotulo: str) -> str:
    while True:
        valor = input(rotulo).strip()
        if valor:
            return valor
        print("Entrada obrigatoria. Tente novamente.")


def ler_inteiro(rotulo: str, minimo: int | None = None) -> int:
    while True:
        valor = input(rotulo).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Digite um numero inteiro valido.")
            continue

        if minimo is not None and numero < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue
        return numero


def ler_float(rotulo: str, minimo: float | None = None) -> float:
    while True:
        valor = input(rotulo).strip().replace(",", ".")
        try:
            numero = float(valor)
        except ValueError:
            print("Digite um numero valido.")
            continue

        if minimo is not None and numero < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue
        return numero


def pausar() -> None:
    input("\nPressione ENTER para continuar...")


def confirmar(mensagem: str) -> bool:
    resposta = input(f"{mensagem} [s/N]: ").strip().lower()
    return resposta == "s"


def mostrar_produto(produto: Produto) -> None:
    print(
        f"{produto.codigo:<8} "
        f"{produto.nome:<25.25} "
        f"{produto.categoria:<18.18} "
        f"R$ {produto.preco:>8.2f} "
        f"{produto.quantidade:>6}"
    )


def mostrar_tabela(produtos: list[Produto], paginar: bool = True) -> None:
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    print(
        f"{'Codigo':<8} {'Nome':<25} {'Categoria':<18} "
        f"{'Preco':>11} {'Qtd':>6}"
    )
    print("-" * 74)

    for indice, produto in enumerate(produtos, start=1):
        mostrar_produto(produto)
        if paginar and indice % TAMANHO_PAGINA == 0 and indice < len(produtos):
            input("-- ENTER para proxima pagina --")


def cadastrar_produto(estoque: Estoque) -> None:
    print("\nCadastro de produto")
    codigo = ler_inteiro("Codigo: ", minimo=1)
    nome = ler_texto("Nome: ")
    categoria = ler_texto("Categoria: ")
    preco = ler_float("Preco: ", minimo=0.01)
    quantidade = ler_inteiro("Quantidade: ", minimo=0)

    produto = Produto(codigo, nome, categoria, preco, quantidade)
    estoque.cadastrar(produto)
    salvar_produtos(ARQUIVO_DADOS, estoque.listar_ordenado_por_codigo())
    registrar_log(ARQUIVO_LOG, f"Produto cadastrado: codigo {codigo}")
    print("Produto cadastrado com sucesso.")


def editar_produto(estoque: Estoque) -> None:
    print("\nEdicao de produto")
    codigo = ler_inteiro("Codigo do produto: ", minimo=1)
    produto = estoque.buscar_por_codigo(codigo)
    if produto is None:
        print("Produto nao encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")
    novo_nome = input(f"Nome [{produto.nome}]: ").strip() or None
    nova_categoria = input(f"Categoria [{produto.categoria}]: ").strip() or None
    novo_preco = ler_float_opcional(f"Preco [{produto.preco:.2f}]: ", minimo=0.01)
    nova_quantidade = ler_inteiro_opcional(
        f"Quantidade [{produto.quantidade}]: ",
        minimo=0,
    )

    estoque.editar(
        codigo,
        nome=novo_nome,
        categoria=nova_categoria,
        preco=novo_preco,
        quantidade=nova_quantidade,
    )
    salvar_produtos(ARQUIVO_DADOS, estoque.listar_ordenado_por_codigo())
    registrar_log(ARQUIVO_LOG, f"Produto editado: codigo {codigo}")
    print("Produto editado com sucesso.")


def ler_float_opcional(rotulo: str, minimo: float | None = None) -> float | None:
    while True:
        valor = input(rotulo).strip()
        if not valor:
            return None
        try:
            numero = float(valor.replace(",", "."))
        except ValueError:
            print("Digite um numero valido ou deixe em branco.")
            continue

        if minimo is not None and numero < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue
        return numero


def ler_inteiro_opcional(rotulo: str, minimo: int | None = None) -> int | None:
    while True:
        valor = input(rotulo).strip()
        if not valor:
            return None
        try:
            numero = int(valor)
        except ValueError:
            print("Digite um numero inteiro valido ou deixe em branco.")
            continue

        if minimo is not None and numero < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue
        return numero


def remover_produto(estoque: Estoque) -> None:
    print("\nRemocao de produto")
    codigo = ler_inteiro("Codigo do produto: ", minimo=1)
    produto = estoque.buscar_por_codigo(codigo)
    if produto is None:
        print("Produto nao encontrado.")
        return

    mostrar_tabela([produto], paginar=False)
    if not confirmar("Confirmar remocao?"):
        print("Remocao cancelada.")
        return

    estoque.remover(codigo)
    salvar_produtos(ARQUIVO_DADOS, estoque.listar_ordenado_por_codigo())
    registrar_log(ARQUIVO_LOG, f"Produto removido: codigo {codigo}")
    print("Produto removido com sucesso.")


def buscar_codigo(estoque: Estoque) -> None:
    print("\nBusca por codigo")
    codigo = ler_inteiro("Codigo: ", minimo=1)
    produto = estoque.buscar_por_codigo(codigo)
    if produto is None:
        print("Produto nao encontrado.")
    else:
        mostrar_tabela([produto], paginar=False)


def buscar_nome(estoque: Estoque) -> None:
    print("\nBusca por nome")
    termo = ler_texto("Nome ou parte do nome: ")
    produtos = estoque.buscar_por_nome(termo)
    mostrar_tabela(produtos)


def registrar_venda(estoque: Estoque) -> None:
    print("\nRegistro de venda")
    codigo = ler_inteiro("Codigo do produto: ", minimo=1)
    quantidade = ler_inteiro("Quantidade vendida: ", minimo=1)
    produto = estoque.registrar_venda(codigo, quantidade)
    salvar_produtos(ARQUIVO_DADOS, estoque.listar_ordenado_por_codigo())
    registrar_log(
        ARQUIVO_LOG,
        f"Venda registrada: codigo {codigo}, quantidade {quantidade}",
    )
    print(
        "Venda registrada com sucesso. "
        f"Estoque atual de {produto.nome}: {produto.quantidade}"
    )


def listar_produtos(estoque: Estoque) -> None:
    print("\nProdutos ordenados por codigo")
    mostrar_tabela(estoque.listar_ordenado_por_codigo())


def listar_categoria(estoque: Estoque) -> None:
    print("\nProdutos por categoria")
    categoria = ler_texto("Categoria: ")
    produtos = estoque.listar_por_categoria(categoria)
    mostrar_tabela(produtos)


def relatorio_estoque_baixo(estoque: Estoque) -> None:
    print("\nRelatorio de estoque baixo")
    limite = ler_inteiro("Limite de estoque: ", minimo=0)
    produtos = estoque.relatorio_estoque_baixo(limite)
    mostrar_tabela(produtos)


def relatorio_precos(estoque: Estoque) -> None:
    print("\nRelatorio de menor e maior preco")
    menor = estoque.menor_preco()
    maior = estoque.maior_preco()
    if menor is None or maior is None:
        print("Nenhum produto cadastrado.")
        return

    print("Menor preco:")
    mostrar_tabela([menor], paginar=False)
    print("\nMaior preco:")
    mostrar_tabela([maior], paginar=False)


def salvar_dados(estoque: Estoque) -> None:
    salvar_produtos(ARQUIVO_DADOS, estoque.listar_ordenado_por_codigo())
    registrar_log(ARQUIVO_LOG, "Dados salvos manualmente")
    print(f"Dados salvos em {ARQUIVO_DADOS}.")


def carregar_dados(estoque: Estoque) -> None:
    produtos = carregar_produtos(ARQUIVO_DADOS)
    estoque.substituir_todos(produtos)
    registrar_log(ARQUIVO_LOG, "Dados carregados manualmente")
    print(f"{estoque.total_produtos()} produto(s) carregado(s).")


def montar_menu() -> str:
    return """
================ Estoque e Vendas ================
1. Cadastrar produto
2. Editar produto
3. Remover produto
4. Buscar produto por codigo
5. Buscar produtos por nome
6. Registrar venda
7. Listar produtos ordenados por codigo
8. Listar produtos por categoria
9. Relatorio de estoque baixo
10. Relatorio de menor e maior preco
11. Salvar dados
12. Carregar dados
0. Sair
===================================================
Escolha uma opcao: """


def executar_opcao(opcao: str, estoque: Estoque) -> bool:
    acoes = {
        "1": cadastrar_produto,
        "2": editar_produto,
        "3": remover_produto,
        "4": buscar_codigo,
        "5": buscar_nome,
        "6": registrar_venda,
        "7": listar_produtos,
        "8": listar_categoria,
        "9": relatorio_estoque_baixo,
        "10": relatorio_precos,
        "11": salvar_dados,
        "12": carregar_dados,
    }

    if opcao == "0":
        salvar_produtos(ARQUIVO_DADOS, estoque.listar_ordenado_por_codigo())
        registrar_log(ARQUIVO_LOG, "Sistema encerrado")
        print("Dados salvos. Ate logo!")
        return False

    acao = acoes.get(opcao)
    if acao is None:
        print("Opcao invalida.")
        return True

    try:
        acao(estoque)
    except ValueError as erro:
        print(f"Erro: {erro}")
    return True


def main() -> None:
    try:
        estoque = Estoque(carregar_produtos(ARQUIVO_DADOS))
    except ValueError as erro:
        print(f"Erro ao carregar dados: {erro}")
        estoque = Estoque()

    registrar_log(ARQUIVO_LOG, "Sistema iniciado")
    continuar = True
    while continuar:
        opcao = input(montar_menu()).strip()
        continuar = executar_opcao(opcao, estoque)
        if continuar:
            pausar()


if __name__ == "__main__":
    main()
