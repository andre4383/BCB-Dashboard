# BCB Dashboard - Guia Rápido

Este é o guia passo a passo para você rodar o seu projeto localmente, compatível com **Windows** e **Mac/Linux**.
O projeto é dividido em três partes: Banco de Dados, Backend (Python/FastAPI) e Frontend (React).

## Pré-requisito: Banco de Dados
Antes de rodar o código, certifique-se de que o seu **PostgreSQL** está rodando no seu computador (via Docker).

```bash
docker compose up -d
```

---

## Passo a Passo para Iniciar o Projeto

Sempre que você for trabalhar no projeto, precisará ligar os dois motores abrindo **dois terminais**.

### Terminal 1: Ligar o Backend (API)
1. Abra o terminal na pasta raiz do projeto (`BCB-Dashboard`).
2. Ative o ambiente virtual do Python:
   - **No Windows:** 
     ```cmd
     venv\Scripts\activate
     ```
   - **No Mac/Linux:** 
     ```bash
     source venv/bin/activate
     ```
3. Ligue o servidor da API:
   - **No Windows:** `python -m uvicorn api.api:app --reload`
   - **No Mac/Linux:** `uvicorn api.api:app --reload`
   
   *Deixe esse terminal aberto. A API estará funcionando na porta 8000.*

### Terminal 2: Ligar o Frontend (React)
1. Abra um **novo terminal**.
2. Entre na pasta do site:
   ```bash
   cd frontend
   ```
3. Ligue o servidor do site:
   ```bash
   npm run dev
   ```
   *O terminal mostrará um link para você.*

---

## Como Acessar e Usar o Site
Com os dois terminais rodando (API e Frontend), abra o seu navegador de internet e acesse:

👉 **http://localhost:5173/**

## Preparando os Dados (Apenas 1ª vez ou Atualização)
Se o banco de dados estiver vazio, popule-o rodando (com o ambiente virtual ativado):
```bash
python bronze.py
python silver.py
```

## Como Desligar Tudo
Quando terminar seu trabalho e quiser fechar o projeto, basta ir nos dois terminais e pressionar:
**`Ctrl + C`** (Isso "mata" os processos em andamento).
