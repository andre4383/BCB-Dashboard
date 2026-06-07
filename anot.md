# O MAPA (5 passos)

- Subir Postgres no Docker
- Criar as tabelas bronze e silver
- Bater na API do BCB → salvar CRU em bronze
- Ler bronze → limpar/tratar → salvar em silver
- Logar e provar que funcionou

# Contexto de analises:
1. Evolução trimestral de volume (tu já pensou nessa) → Gráfico de linha: valor total de transações por trimestre ao longo dos anos. Mostra crescimento do mercado de pagamentos brasileiro.
2. > 1- Por que a quantidade de Saques desceram mais de 50% nos ultimos 10 anos?
>>2- Quantidade de Saques no eixo y e datatrimestre no eixo x
>>>3 - Grafico de Linhas
>>>>4- Criar 5 partes do grafico significando cada parte desse periodo de 10 anos
3. *? Ainda falta ?*