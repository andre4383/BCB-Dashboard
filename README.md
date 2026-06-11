# Dashboard BCB (Banco Central do Brasil)

Este projeto realiza a extração, tratamento e visualização de dados abertos do Banco Central do Brasil focados nos **Meios de Pagamento**. A arquitetura utiliza a metodologia medalhão (Bronze e Silver), banco de dados em PostgreSQL (via Docker) e uma interface de relatórios interativa desenvolvida em Streamlit.

---

## Passo a Passo para Rodar o Projeto

Siga o passo a passo abaixo para inicializar toda a estrutura, desde o banco de dados até o painel visual no seu navegador.

### 1. Criar e Ativar o Ambiente Virtual
O ambiente virtual (`venv`) isola as bibliotecas do projeto da sua máquina.

**No Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

*(Lembre-se: Sempre que for trabalhar no projeto, ative o ambiente virtual para que o prefixo `(venv)` apareça no seu terminal).*

### 2. Instalar as Dependências
Com o ambiente ativado, instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto (caso não exista) com as seguintes credenciais:
```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=bcb_dashboard
```

### 4. Inicializar o Banco de Dados (Docker)
O banco de dados PostgreSQL roda dentro de um container Docker. Para subir esse container em segundo plano, rode:
```bash
docker compose up -d
```
*(Se no futuro quiser desligar o banco, basta rodar `docker compose down`).*

### 5. Executar o Pipeline de Dados (Bronze e Silver)
Agora que o banco está no ar, vamos extrair os dados da API do Banco Central e tratá-los:

**Passo 1:** Extrair dados crus (Camada Bronze):
```bash
python bronze.py
```
**Passo 2:** Tratar e limpar os dados (Camada Silver):
```bash
python silver.py
```

### 6. Inicializar o Dashboard (Streamlit)
Com os dados limpos e preparados na camada Silver, inicialize o painel visual para ver as análises e gráficos:
```bash
streamlit run app.py
```

Após rodar este comando, o servidor do Streamlit será iniciado e seu navegador abrirá automaticamente a aba do painel (geralmente no link `http://localhost:8501`).

---

**Para encerrar o Streamlit**, volte no terminal e pressione `Control + C`.
