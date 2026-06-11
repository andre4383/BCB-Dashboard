// DOCUMENTAÇÃO TÉCNICA — BCB Dashboard

#set document(
  title: "Documentação Técnica — BCB Dashboard",
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

    #text(size: 22pt, weight: "bold")[Documentação Técnica]

    #v(0.8cm)

    #text(size: 12pt)[
      Dashboard de Meios de Pagamento · Banco Central do Brasil
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

= Introdução

Este documento apresenta a documentação técnica do projeto *BCB Dashboard*, desenvolvido como trabalho acadêmico para a disciplina de Engenharia de Dados na Cesar School.

O projeto tem como objetivo coletar, processar e visualizar dados abertos do Banco Central do Brasil (BCB), especificamente os dados de Meios de Pagamento Trimestral, cobrindo o período de 2015 a 2026. O resultado é um painel interativo que permite analisar a evolução do sistema financeiro brasileiro ao longo da última década.

== Motivação

A transformação digital dos meios de pagamento no Brasil acelerou significativamente a partir de 2020, impulsionada pela pandemia de COVID-19 e pelo lançamento do Pix. Este projeto nasce da necessidade de quantificar e visualizar essas mudanças a partir de dados oficiais do Banco Central.

== Objetivos

- Extrair dados da API pública do Banco Central do Brasil;
- Aplicar a arquitetura medalhão (Bronze → Silver → Gold) para tratamento dos dados;
- Persistir os dados em banco de dados relacional (PostgreSQL);
- Apresentar análises visuais através de um dashboard interativo em Streamlit.

= Arquitetura do Sistema

== Visão Geral

O sistema segue a arquitetura medalhão (_Medallion Architecture_), que organiza o processamento em camadas progressivas de qualidade.

#figure(
  booktable(
    columns: (auto, auto, 1fr),
    align: (center, center, left),
    [Camada],
    [Arquivo],
    [Responsabilidade],
    [Bronze],
    [`bronze.py`],
    [Extração dos dados crus da API do BCB e persistência no banco.],
    [Silver],
    [`silver.py`],
    [Limpeza, normalização de tipos e ordenação cronológica.],
    [Gold],
    [`gold.py`],
    [Transformações analíticas e criação de tabelas por análise.],
    [App],
    [`app.py`],
    [Dashboard interativo com visualizações via Streamlit.],
  ),
  caption: [Camadas da arquitetura medalhão.],
)

== Infraestrutura

O banco de dados é o *PostgreSQL*, executado em contêiner Docker. A comunicação é feita via *SQLAlchemy*.

```text
# docker-compose.yml
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: bcb_dashboard
    ports:
      - "5432:5432"
```

= Fonte de Dados

== API do Banco Central do Brasil

Os dados são obtidos do endpoint `MeiosdePagamentosTrimestralDA` da API OData do BCB.

```text
https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/
versao/v1/odata/MeiosdePagamentosTrimestralDA
```

== Principais Campos

#figure(
  booktable(
    columns: (1fr, auto, 1fr),
    align: (left, center, left),
    [Campo],
    [Tipo],
    [Descrição],
    [`datatrimestre`],
    [String → DateTime],
    [Data de referência do trimestre.],
    [`quantidadeSaques`],
    [Float],
    [Volume de saques (em milhares).],
    [`valorTED`],
    [Float],
    [Valor total de TEDs (em milhões).],
    [`valorPix`],
    [Float],
    [Transações Pix (disponível a partir de nov/2020).],
    [`valorTEC`],
    [Float],
    [TEC descontinuada — valores zerados em todo o período.],
  ),
  caption: [Principais campos retornados pela API.],
)

=== Qualidade dos Dados

- `valorTEC` está zerado em todo o período: o instrumento foi descontinuado.
- `valorPix` e `quantidadePix` são nulos antes do 4.º trimestre de 2020.
- `quantidadePix` é armazenado como `float` mas representa valores em milhares.

= Pipeline de Dados

== Camada Bronze — Extração

```text
def data_extract():
    url = "https://olinda.bcb.gov.br/.../MeiosdePagamentosTrimestralDA
          (trimestre=@trimestre)?@trimestre='20151'&$top=100&$format=json"
    response = requests.get(url)
    df = pd.DataFrame(response.json()['value'])
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    df.to_sql('bronze_meios_pagamento', engine, if_exists='replace', index=False)
    return df
```

== Camada Silver — Tratamento

```text
def silver_data_extract():
    df = data_extract()
    df['datatrimestre'] = pd.to_datetime(df['datatrimestre'])
    df = df.sort_values('datatrimestre').reset_index(drop=True)
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    df.to_sql('silver_meios_pagamento', engine, if_exists='replace', index=False)
    return df
```

Transformações: conversão de tipo, ordenação cronológica, reset de índice.

== Camada Gold — Análise

```text
# Variação percentual de saques
gold_saques['variacao_porc'] = df['quantidadeSaques'].pct_change() * 100

# Rotulação por período (pré/pós Pix)
gold_ted['periodo'] = gold_ted['datatrimestre'].apply(
    lambda x: 'pos_pix' if x >= pd.to_datetime('2020-11-01') else 'pre_pix'
)
```

Tabelas geradas: `gold_volume_total`, `gold_saques`, `gold_ted_cres`.

= Dashboard

O dashboard é construído com *Streamlit* e gráficos via *Matplotlib*. Três análises estão disponíveis em abas separadas:

- *Queda de Saques (2015–2026)* — série temporal com marcadores da pandemia e do Pix;
- *Volume Total de Transações* — crescimento do fluxo financeiro agregado;
- *TED: Crescimento e Estagnação* — inflexão do instrumento após o Pix.

= Execução

```text
# 1. Ambiente virtual
python3 -m venv venv && source venv/bin/activate

# 2. Dependências
pip install -r requirements.txt

# 3. Banco de dados
docker compose up -d

# 4. Pipeline
python bronze.py && python silver.py && python gold.py

# 5. Dashboard
streamlit run app.py   # http://localhost:8501
```

= Dependências

#figure(
  booktable(
    columns: (auto, 1fr),
    [Biblioteca],
    [Finalidade],
    [`streamlit`],
    [Interface web do dashboard],
    [`pandas`],
    [Manipulação e transformação de dados],
    [`requests`],
    [Requisições HTTP à API do BCB],
    [`sqlalchemy`],
    [ORM e conexão com PostgreSQL],
    [`matplotlib`],
    [Geração de gráficos],
    [`python-dotenv`],
    [Variáveis de ambiente],
    [`psycopg2`],
    [Driver PostgreSQL para Python],
  ),
  caption: [Dependências do projeto.],
)

= Considerações Finais

A arquitetura medalhão garante rastreabilidade e separação de responsabilidades entre as camadas. O uso de Docker e de variáveis de ambiente assegura portabilidade do ambiente. O pipeline é linear e reproduzível: qualquer execução a partir dos dados brutos gera os mesmos resultados analíticos.
