# BCB-Dashboard

## Arquitetura
API BCB (Olinda) → bronze.py → silver.py → gold.py → Postgres → Streamlit

## Banco
PostgreSQL via Docker. Connection: postgresql://postgres:postgres@localhost:5432/bcb_dashboard

## Tabelas existentes
- bronze_meios_pagamento (dado cru)
- silver_meios_pagamento (limpo, datetime, ordenado)
- gold_volume_total (datatrimestre, volume_total)
- gold_saques (datatrimestre, quantidadeSaques, variacao_porc)
- gold_ted_cres (datatrimestre, valorTED, periodo)

## Tabelas a criar
- gold_market_share (datatrimestre, meio, valor, percentual)
- gold_transferencias (datatrimestre, valorTED, valorDOC, valorPix)
- gold_pix_vs_debito (datatrimestre, valorPix, valorCartaoDebito)

## Stack
Python, pandas, sqlalchemy, psycopg2, plotly, streamlit

## Regra
Dado no banco = número. Formatação = só no Streamlit.
Valores da API já estão em milhões (documentação BCB).