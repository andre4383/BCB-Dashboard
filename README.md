# BCB Dashboard - Guia Rápido

Este é o guia passo a passo para você rodar o seu projeto localmente no seu Mac.
O projeto é dividido em três partes: Banco de Dados, Backend (Python/FastAPI) e Frontend (React).

## Pré-requisito: Banco de Dados
Antes de rodar o código, certifique-se de que o seu **PostgreSQL** está rodando no seu computador (seja pelo aplicativo nativo do Postgres ou via Docker).

---

## Passo a Passo para Iniciar o Projeto

Sempre que você for trabalhar no projeto, precisará ligar os dois motores abrindo **duas abas** no seu terminal.

### Aba 1: Ligar o Backend (API)
1. Abra o terminal na pasta raiz do projeto (`BCB-Dashboard`).
2. Ative o ambiente virtual do Python:
   ```bash
   source venv/bin/activate
   ```
3. Ligue o servidor da API:
   ```bash
   uvicorn api.api:app --reload
   ```
   *Deixe essa aba quieta. A API já estará funcionando e enviando os dados do banco.*

### Aba 2: Ligar o Frontend (React)
1. Abra uma **nova aba** no terminal (`Cmd + T` no Mac).
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
Com as duas abas do terminal rodando (com os comandos travados nelas), basta abrir o seu navegador de internet e acessar:

👉 **http://localhost:5173/**

## Como Desligar Tudo
Quando você terminar seu trabalho e quiser fechar o projeto, basta ir nas duas abas do terminal e pressionar:
**`Ctrl + C`** (Isso "mata" o processo em andamento).
