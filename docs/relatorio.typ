// RELATÓRIO ANALÍTICO — BCB Dashboard

#set document(
  title: "Relatório Analítico — Meios de Pagamento no Brasil",
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
  leading: 0.7em,
  spacing: 1.4em,
)

#set heading(numbering: "1.1")

#show heading.where(level: 1): it => {
  v(2em)
  text(size: 13pt, weight: "bold")[
    #counter(heading).display("1") · #it.body
  ]
  v(0.8em)
}

#show heading.where(level: 2): it => {
  v(1.2em)
  text(size: 11pt, weight: "bold")[
    #counter(heading).display("1.1") · #it.body
  ]
  v(0.5em)
}

#show heading.where(level: 3): it => {
  v(0.8em)
  text(size: 11pt, style: "italic")[#it.body]
  v(0.3em)
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

// Código
#show raw.where(block: true): it => {
  block(width: 100%, inset: (x: 0em, y: 0.5em))[
    #set text(font: "New Computer Modern Mono", size: 9pt)
    #it
  ]
}

#show raw.where(block: false): it => {
  text(font: "New Computer Modern Mono", size: 10pt)[#it]
}

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

    #text(size: 22pt, weight: "bold")[Relatório Analítico]

    #v(0.8cm)

    #text(size: 12pt)[
      A Transformação dos Meios de Pagamento no Brasil\
      2015–2026
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
  #outline(title: none, indent: 1.5em, depth: 3)
]

#counter(page).update(1)

// ================================================
// CONTEÚDO
// ================================================

= Apresentação

Este relatório apresenta as análises realizadas sobre os dados de Meios de Pagamento Trimestral do Banco Central do Brasil, cobrindo o período de *março de 2015 a março de 2026* — 45 trimestres. Os dados foram tratados por um pipeline em Python e visualizados em um dashboard Streamlit.

O período contempla dois eventos de ruptura: a *pandemia de COVID-19* (março/2020) e o *lançamento do Pix* (novembro/2020). As três análises do relatório dialogam diretamente com esses marcos.

= Contextualização

== O Sistema de Pagamentos Brasileiro

O Sistema de Pagamentos Brasileiro (SPB) passou por uma modernização gradual ao longo dos anos 2010, com expansão dos pagamentos digitais, cartões e transferências eletrônicas. A partir de 2020, dois fenômenos precipitaram uma transformação estrutural:

- A pandemia forçou a digitalização acelerada das transações, reduzindo o uso de dinheiro físico;
- O Pix introduziu transferências instantâneas, gratuitas para pessoa física, disponíveis 24h/7d.

== Dados Utilizados

Os dados provêm do endpoint `MeiosdePagamentosTrimestralDA` da API OData do BCB: 45 registros trimestrais com volume e valor dos principais instrumentos (saques, TED, DOC, Pix, cartões).

= Análise 1 — Queda de Saques (2015–2026)

== Descrição e Metodologia

Série temporal de `quantidadeSaques` (em milhares por trimestre) com marcadores nos dois eventos de ruptura: março/2020 (pandemia) e novembro/2020 (Pix).

== Resultados

#figure(
  booktable(
    columns: (auto, 1fr),
    [Período], [Comportamento],
    [2015–2019],          [Estabilidade relativa com oscilações sazonais.],
    [2020/T1 — Pandemia], [Queda abrupta: isolamento social elimina a demanda por dinheiro físico.],
    [2020/T4 — Pix],      [Segunda ruptura: Pix elimina a necessidade de saque no cotidiano.],
    [2021–2026],          [Novo patamar estruturalmente inferior, sem recuperação.],
  ),
  caption: [Comportamento da quantidade de saques por período.]
)

== Interpretação

A queda acumulada entre o pico de 2019 e 2026 supera *50%*. Os dois eventos não são independentes: a pandemia catalisou uma transformação que o Pix consolidou de forma permanente.

= Análise 2 — Volume Total de Transações

== Descrição e Metodologia

Soma horizontal de todas as colunas `valor` do DataFrame Silver, gerando o fluxo financeiro total por trimestre:

```text
valor_total = df.filter(like='valor').sum(axis=1)
```

== Resultados

#figure(
  booktable(
    columns: (auto, 1fr),
    [Período], [Comportamento],
    [2015–2019], [Crescimento moderado e constante.],
    [2020],      [Aceleração: transações digitais suprem necessidades antes atendidas presencialmente.],
    [2021–2026], [Crescimento exponencial sustentado pelo volume do Pix.],
  ),
  caption: [Evolução do volume total de transações.]
)

== Interpretação

O volume financeiro agregado *continua crescendo* mesmo com a queda dos saques. A digitalização não contraiu o mercado — ela o expandiu, incluindo segmentos antes não-bancarizados.

= Análise 3 — TED: Crescimento e Estagnação

== Descrição e Metodologia

Série temporal de `valorTED` com rotulação pré/pós Pix na camada Gold:

```text
gold_ted['periodo'] = gold_ted['datatrimestre'].apply(
    lambda x: 'pos_pix' if x >= pd.to_datetime('2020-11-01') else 'pre_pix'
)
```

== Resultados

#figure(
  booktable(
    columns: (auto, 1fr),
    [Período], [Comportamento],
    [Pré-Pix (2015–2020)],  [Crescimento robusto: valor das TEDs sobe mais de 321%.],
    [Pós-Pix (nov/2020+)],  [Estagnação imediata: crescimento cessa, curva oscila horizontalmente.],
  ),
  caption: [Comportamento das TEDs antes e após o Pix.]
)

== Interpretação

A TED crescia por cinco anos consecutivos. No trimestre seguinte ao Pix, a trajetória é interrompida. O Pix oferece as mesmas funcionalidades — sem custo, 24/7 — tornando a TED redundante para a maioria dos usuários.

= Síntese

#figure(
  booktable(
    columns: (1fr, auto, 1fr),
    align: (left, center, left),
    [Indicador], [Tendência], [Fator determinante],
    [Quantidade de Saques],       [↓ > 50%],            [Pandemia + Pix],
    [Volume Total de Transações], [↑ exponencial],       [Digitalização + Pix],
    [Valor das TEDs],             [→ estagnação],        [Substituição pelo Pix],
  ),
  caption: [Síntese das três análises.]
)

= Conclusão

As análises revelam uma transformação estrutural do sistema financeiro brasileiro. O Pix não apenas criou um novo instrumento de pagamento — reorganizou o ecossistema inteiro, tornando obsoletos padrões consolidados por décadas e expandindo o mercado para novos usuários. Os dados do Banco Central registram, trimestre a trimestre, essa mudança permanente de comportamento.
