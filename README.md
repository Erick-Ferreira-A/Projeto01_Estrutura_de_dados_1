# Sistema de Estoque e Vendas

Sistema de linha de comando em Python para controlar produtos, vendas,
estoque e relatorios. O projeto usa os conceitos de Python basico,
complexidade Big-O, vetor nao ordenado e vetor ordenado.

## Funcionalidades

- Cadastrar produto com codigo unico, nome, categoria, preco e quantidade.
- Editar nome, categoria, preco e quantidade.
- Remover produto pelo codigo.
- Buscar produto por codigo com busca binaria em vetor ordenado.
- Buscar produtos por nome com busca linear em vetor nao ordenado.
- Registrar venda com validacao de estoque.
- Listar produtos ordenados por codigo.
- Filtrar produtos por categoria.
- Exibir relatorio de estoque baixo com limite configuravel.
- Exibir menor e maior preco.
- Salvar e carregar dados em JSON.
- Registrar logs simples de operacoes.
- Paginar listagens a cada 5 produtos.

## Estrutura

```text
Projeto01_Estrutura_de_dados_1/
|-- main.py
|-- produto.py
|-- estoque.py
|-- arquivos.py
|-- logger_operacoes.py
|-- dados/
|   `-- produtos.json
|-- logs/
|-- tests/
|   `-- test_estoque.py
|-- RELATORIO.md
|-- README.md
`-- .gitignore
```

## Como executar

1. Abra o terminal na pasta do projeto.
2. Execute:

```bash
python main.py
```

O sistema carrega automaticamente os dados de exemplo em
`dados/produtos.json`. Ao cadastrar, editar, remover ou vender, o arquivo
tambem e salvo automaticamente.

## Como testar

Execute os testes automatizados:

```bash
python -m unittest discover -s tests
```

Tambem e possivel conferir a sintaxe dos arquivos Python com:

```bash
python -m compileall .
```

## Exemplos de uso no menu

- Opcao `1`: cadastrar um produto novo. O codigo nao pode se repetir.
- Opcao `4`: buscar produto por codigo. Esta busca usa o vetor ordenado.
- Opcao `5`: buscar produtos por nome. Esta busca percorre o vetor nao
  ordenado.
- Opcao `6`: registrar venda. O sistema reduz a quantidade em estoque e
  bloqueia venda maior que o estoque disponivel.
- Opcao `9`: informar um limite, por exemplo `10`, para listar produtos com
  quantidade menor que esse valor.

## Complexidade das buscas

O sistema mantem duas listas:

- `produtos`: vetor nao ordenado, na ordem de cadastro.
- `produtos_por_codigo`: vetor ordenado por codigo.

A busca por nome usa busca linear, pois nomes podem se repetir e a consulta
aceita parte do texto. Assim, o algoritmo precisa verificar item por item. A
complexidade e `O(n)`.

A busca por codigo usa busca binaria no vetor ordenado por codigo. Como o
codigo e unico e o vetor permanece ordenado nas insercoes e remocoes, a busca
divide o intervalo pela metade a cada passo. A complexidade e `O(log n)`.

## Dados e logs

- Dados: `dados/produtos.json`
- Logs: `logs/operacoes.log`

O arquivo de log e criado automaticamente durante a execucao. Ele nao precisa
ser enviado para o GitHub.
