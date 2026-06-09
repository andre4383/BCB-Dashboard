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

## COMO RODAR:

1. Clone o repo
2. Crie o ambiente virtual: `python -m venv venv` (ou `python3 -m venv venv` no Mac)
3. Ative o ambiente virtual:
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`
4. Instale dependências: `pip install -r requirements.txt`
5. Crie o `.env` com POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
6. Suba o banco: `docker compose up -d`
7. Rode o pipeline: `python bronze.py` depois `python silver.py`
8. Inicie a API (Backend): `uvicorn api.api:app --reload` (Mantenha esse terminal aberto)
9. Em um NOVO terminal, vá para a pasta frontend (`cd frontend`) e inicie o site: `npm run dev`

## RODANDO NO DIA A DIA (Quando já tem tudo instalado e o banco pronto):

1. **Suba o banco de dados (se estiver desligado):** `docker compose up -d`
2. **Ligue a API:** Abra um terminal, ative o venv (`source venv/bin/activate` ou `venv\Scripts\activate`) e rode `uvicorn api.api:app --reload`
3. **Ligue o Site:** Abra outro terminal, vá para a pasta frontend (`cd frontend`) e rode `npm run dev`