// STORYTELLING — BCB Dashboard

#set document(
  title: "O Brasil que Deixou de Sacar",
  author: "Lucas Cardoso & André Montenegro",
)

#set page(
  paper: "a4",
  margin: (top: 3.5cm, bottom: 3.5cm, left: 3.5cm, right: 3cm),
  footer: context [
    #set align(center)
    #set text(size: 9pt, fill: rgb("#aaaaaa"))
    #counter(page).display("1")
  ],
)

#set text(
  font: "New Computer Modern",
  size: 11pt,
  lang: "pt",
)

#set par(
  justify: true,
  leading: 0.8em,
  spacing: 1.5em,
)

#set heading(numbering: "1.")

#show heading.where(level: 1): it => {
  v(2em)
  text(size: 13pt, weight: "bold")[
    #counter(heading).display("1") · #it.body
  ]
  v(0.8em)
}

#show heading.where(level: 2): it => {
  v(1.2em)
  text(size: 11pt, style: "italic", weight: "bold")[#it.body]
  v(0.5em)
}

// Tabelas estilo booktabs
#set table(stroke: none, inset: (x: 0.5em, y: 0.5em))
#show table.cell.where(y: 0): set text(weight: "bold")

#let booktable(..args) = {
  block(width: 100%)[
    #line(length: 100%, stroke: 0.8pt)
    #v(0.2em)
    #table(..args)
    #v(0.2em)
    #line(length: 100%, stroke: 0.8pt)
  ]
}

// Citação em recuo
#let aside(body) = block(
  width: 100%,
  inset: (left: 2em, top: 0.5em, bottom: 0.5em, right: 0em),
)[
  #set text(size: 10.5pt, style: "italic")
  #body
]

// Figuras
#set figure(gap: 0.8em)
#show figure.caption: set text(size: 9pt, style: "italic")

// ================================================
// CAPA
// ================================================

#page(footer: none)[
  #v(6cm)
  #align(center)[
    #text(size: 11pt, tracking: 2pt)[CESAR SCHOOL]

    #v(2.5cm)

    #text(size: 22pt, weight: "bold")[O Brasil que Deixou de Sacar]

    #v(0.8cm)

    #text(size: 12pt, style: "italic")[
      Como uma pandemia e um aplicativo\
      reescreveram a história do dinheiro no Brasil
    ]

    #v(3.5cm)

    #text(size: 10.5pt)[Lucas Cardoso & André Montenegro]

    #v(0.5em)

    #text(size: 9.5pt, fill: rgb("#666666"))[
      Professor: Marco Aurelio Tomaz Mialaret Junior
    ]

    #v(2.5cm)

    #text(size: 9pt, fill: rgb("#aaaaaa"))[
      Recife, #datetime.today().display("[year]")
    ]
  ]
]

// ================================================
// SUMÁRIO
// ================================================

#page(footer: none)[
  #v(2cm)
  #text(size: 13pt, weight: "bold")[Sumário]
  #v(1cm)
  #outline(title: none, indent: 1.5em, depth: 2)
]

#counter(page).update(1)

// ================================================
// CONTEÚDO
// ================================================

= Prólogo: Uma Carteira Cada Vez Mais Leve

Pense na última vez que você foi a um caixa eletrônico sacar dinheiro.

Se você tem menos de 30 anos, provavelmente está tentando se lembrar. Se tem mais de 40, a memória vem fácil — o barulho da máquina contando notas, o envelope branco, a sensação de segurar o dinheiro na mão antes de ir ao mercado, pagar o almoço ou dividir a conta com os amigos.

Essa cena está desaparecendo do Brasil.

Não de forma gradual, como o declínio de uma tecnologia substituída lentamente ao longo de gerações. O que os dados do Banco Central revelam é algo mais abrupto: uma ruptura, um antes e um depois, marcado por dois eventos que chegaram ao mesmo tempo e mudaram tudo.

Este documento não é um relatório técnico. É a história que os números contam.

= O Mundo Antes do Pix (2015–2019)

No início de 2015, o Brasil vivia um sistema financeiro dual. De um lado, o dinheiro físico: para o mercadinho da esquina, o pagamento do pedreiro, a mesada dos filhos. De outro, os instrumentos digitais — TED, DOC, cartão — cada um com sua taxa, seu horário, suas limitações.

Quem precisava transferir dinheiro tinha um ritual:

#aside[
  Entrar no internet banking antes das 17h, escolher entre TED (mais rápido, mais caro) ou DOC (mais barato, cai só no dia seguinte), digitar todos os dados bancários do destinatário, confirmar com senha, aguardar.
]

Era funcional. Era o que existia. E o volume de TEDs crescia ano após ano — a economia digital brasileira se expandia, mas dentro de um modelo ainda caro e excludente. Os saques mantinham-se estáveis. O dinheiro físico ainda era rei.

= Dois Choques em Oito Meses

== Março de 2020 — O Mundo Para

Em março de 2020, o coronavírus transformou a normalidade em memória. Decretos de isolamento fecharam comércios, esvaziaram ruas, levaram as pessoas para dentro de casa. Com as pessoas, foi também o dinheiro físico.

O gráfico de saques revela uma queda vertical nesse momento — não uma inclinação suave, mas uma quebra abrupta. Em um único trimestre, o volume de saques despencou para níveis que o Brasil não via há anos.

#aside[
  Quando você não pode sair de casa, não precisa de dinheiro no bolso. Quando não há dinheiro no bolso, não há motivo para ir ao caixa eletrônico. É uma lógica simples — e ela se manifestou nos dados em tempo real.
]

== Novembro de 2020 — O Pix Chega

Oito meses depois, enquanto o país ainda lidava com a pandemia, o Banco Central lançou o Pix: transferências instantâneas, gratuitas para pessoa física, disponíveis 24 horas por dia, 7 dias por semana, incluindo feriados. Sem horário de corte, sem tarifa, sem burocracia.

O que aconteceu a seguir está nos dados.

= O Antes e o Depois

== A Curva que Não Voltou

Após o Pix, os saques bancários não se recuperaram. Esse é o detalhe mais revelador de toda a análise.

Sem o Pix, seria razoável esperar uma recuperação parcial com o fim do isolamento. Com o Pix, isso não aconteceu. O Pix eliminou a necessidade de saque para a maioria das situações cotidianas: o mercadinho instalou QR Code, o pedreiro recebe via transferência instantânea, a mesada chega em segundos.

#aside[
  A pandemia forçou as pessoas a experimentarem o digital. O Pix fez com que elas não quisessem voltar atrás.
]

== A TED que Parou de Crescer

Por cinco anos, o valor das TEDs cresceu consistentemente, trimestre após trimestre. No trimestre seguinte ao Pix, esse crescimento cessou. A curva passou a oscilar horizontalmente. A TED não morreu — mas parou de crescer.

O mecanismo é direto: cada real transferido via TED passou a ser enviado via Pix. Mais rápido, sem custo, sem limite de horário.

== O Mercado que Não Parou

Se os saques caíram mais de 50% e a TED estacionou, seria razoável imaginar retração no volume financeiro total. O que os dados mostram é o oposto: o volume total *continuou crescendo*, de forma acelerada.

A digitalização não contraiu o mercado — ela o expandiu. Pessoas que antes operavam exclusivamente em dinheiro físico passaram a realizar transações digitais pela primeira vez. O Pix incluiu o não-bancarizado.

= O Que os Dados Revelam Sobre Nós

Esta história não é apenas sobre tecnologia. É sobre comportamento humano.

Os dados do Banco Central são registros de escolhas: quantas vezes alguém decidiu sacar, quanto foi transferido eletronicamente, como essas escolhas mudaram ao longo do tempo. E as mudanças são permanentes.

#aside[
  Dados não mentem, mas tampouco explicam sozinhos. A história por trás de uma queda de 50% nos saques é feita de padarias que instalaram QR Code, de avós que aprenderam a usar o aplicativo do banco, de trabalhadores informais que recebem agora sem precisar de conta corrente.
]

= Epílogo — O Que Vem a Seguir

Os dados chegam até março de 2026. O Pix já é o instrumento mais utilizado no Brasil em número de transações. O dinheiro físico encolhe trimestre após trimestre. A TED enfrenta uma questão existencial.

#figure(
  booktable(
    columns: (1fr, auto, 1fr),
    align: (left, center, left),
    [O que medimos], [Direção], [O que significa],
    [Quantidade de Saques],       [↓], [Dinheiro físico em declínio estrutural],
    [Volume Total de Transações], [↑], [Economia digital em expansão],
    [Valor das TEDs],             [→], [Substituição silenciosa pelo Pix],
  ),
  caption: [Os três indicadores e o que revelam.]
)

A história que este projeto conta não tem fim nos nossos dados. Ela continua acontecendo, neste momento, em cada QR Code lido, em cada Pix enviado às 2h da manhã de um domingo, em cada caixa eletrônico que fica um pouco mais ocioso do que no trimestre anterior.

O Brasil mudou a forma como lida com o dinheiro. E os números estão aí para provar.

#v(3em)
#align(center)[
  #set text(size: 9pt, fill: rgb("#aaaaaa"), style: "italic")
  Dados: API OData do Banco Central do Brasil — Meios de Pagamento Trimestral (2015–2026).\
  Pipeline Bronze/Silver/Gold em Python. Visualização: Streamlit. Cesar School, #datetime.today().display("[year]").
]
