# Relatorio curto - escolhas de busca e ordenacao

## Objetivo

O sistema foi organizado para atender ao controle de produtos, estoque,
vendas e relatorios por terminal, aplicando vetores nao ordenados, vetores
ordenados e analise de complexidade Big-O.

## Vetor nao ordenado

A lista `produtos` guarda os produtos na ordem de cadastro. Ela representa o
vetor nao ordenado do projeto.

Essa estrutura foi usada para a busca por nome porque:

- nomes podem se repetir;
- o usuario pode buscar apenas parte do nome;
- nao existe uma ordenacao unica que resolva todos os termos parciais.

Por isso, a busca por nome percorre todos os produtos e compara o texto
informado com o nome de cada item. A complexidade e `O(n)`.

## Vetor ordenado por codigo

A lista `produtos_por_codigo` mantem os mesmos objetos da lista principal,
mas sempre ordenados pelo campo `codigo`.

Essa estrutura foi usada para:

- buscar produto por codigo;
- listar produtos em ordem crescente de codigo.

Como o codigo e unico, a busca binaria e adequada. A cada comparacao, metade
do vetor e descartada, resultando em complexidade `O(log n)`.

## Insercao e remocao

Ao cadastrar um produto, o sistema:

1. valida se o codigo ja existe;
2. adiciona o item ao vetor nao ordenado;
3. encontra a posicao correta no vetor ordenado;
4. insere o produto nessa posicao.

A insercao em vetor ordenado pode exigir deslocamento de elementos, portanto
tem custo `O(n)`. Essa escolha foi aceita porque melhora a busca por codigo,
um requisito obrigatorio do projeto.

Na remocao, o produto e removido das duas listas para manter as estruturas
sincronizadas.

## Persistencia

Os dados sao salvos em JSON no arquivo `dados/produtos.json`. O JSON foi
escolhido por ser simples, legivel e suficiente para armazenar os campos do
produto sem bibliotecas externas.

## Validacoes

O sistema impede:

- codigo duplicado;
- preco menor ou igual a zero;
- quantidade negativa;
- venda com estoque insuficiente;
- campos de texto vazios.
