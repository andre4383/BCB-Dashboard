# Dashboard BCB (Banco Central do Brasil)

Este projeto realiza a extração, tratamento e visualização de dados abertos do Banco Central do Brasil focados nos Meios de Pagamento. A arquitetura utiliza a metodologia medalhão (Bronze, Silver e Gold), banco de dados em PostgreSQL (via Docker) e uma interface de relatórios interativa desenvolvida em Streamlit.

## Passo a Passo para Rodar o Projeto

### 1. Criar e Ativar o Ambiente Virtual

No Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto com as seguintes credenciais:
```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=bcb_dashboard
```

### 4. Inicializar o Banco de Dados (Docker)

```bash
docker compose up -d
```

### 5. Executar o Pipeline de Dados (Bronze, Silver e Gold)

Passo 1: Extrair dados crus (Camada Bronze):
```bash
python pipeline/bronze.py
```

Passo 2: Tratar e limpar os dados (Camada Silver):
```bash
python pipeline/silver.py
```

```
Passo 3: Agregar e transformar os dados para visualização (Camada Gold):
```bash
python pipeline/gold.py
```

### 6. Inicializar o Dashboard (Streamlit)

```bash
streamlit run app/app.py
```

## Integrantes

| Nome | E-mail |
|---|---|
| André Montenegro | agmos@cesar.school |
| Lucas Gabriel Cardoso de Souza | lgcs2@cesar.school |
