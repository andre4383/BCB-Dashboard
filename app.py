import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


st.set_page_config(page_title="BCB Dashboard", layout="wide")


@st.cache_data
def load_data():
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    gold_saques  = pd.read_sql('gold_saques', engine)
    gold_ted     = pd.read_sql('gold_ted_cres', engine)
    gold_transf  = pd.read_sql('gold_transferencias', engine)
    gold_pix_deb = pd.read_sql('gold_pix_vs_debito', engine)
    gold_ms      = pd.read_sql('gold_market_share', engine)
    return gold_saques, gold_ted, gold_transf, gold_pix_deb, gold_ms


gold_saques, gold_ted, gold_transf, gold_pix_deb, gold_ms = load_data()

# ---------------------------------------------------------------------------
# Cabeçalho e contexto
# ---------------------------------------------------------------------------
st.title("Dashboard de Meios de Pagamento — Banco Central do Brasil")
st.markdown(
    "Análise da evolução dos meios de pagamento no Brasil entre 2015 e 2026, a partir dos "
    "dados públicos trimestrais do Banco Central (API Olinda). O recorte cobre 45 trimestres "
    "e inclui dois marcos decisivos do período: a pandemia de 2020 e o lançamento do Pix, "
    "em novembro de 2020."
)
st.markdown(
    "**Metodologia.** Os saques são medidos pelo montante sacado em reais, indicador que "
    "reflete o volume de dinheiro em espécie em circulação. Os demais meios são comparados "
    "pelo número de transações, indicador que reflete a frequência de uso no dia a dia — "
    "dimensão na qual o Pix se tornou o meio dominante. As duas métricas contam histórias "
    "diferentes: por valor movimentado, transferências corporativas (TED) lideram; por "
    "número de transações, o Pix concentra a maior parte do mercado."
)

st.divider()

# ---------------------------------------------------------------------------
# Indicadores-chave
# ---------------------------------------------------------------------------
st.subheader("Indicadores-chave (2015 a 2026)")
col1, col2, col3 = st.columns(3)

primeiro_saque = gold_saques['valorSaques'].iloc[0]
ultimo_saque   = gold_saques['valorSaques'].iloc[-1]
queda_saques   = ((ultimo_saque - primeiro_saque) / primeiro_saque * 100).round(1)

pico_ted     = gold_ted['quantidadeTED'].max()
ultimo_ted   = gold_ted['quantidadeTED'].iloc[-1]
queda_ted    = ((ultimo_ted - pico_ted) / pico_ted * 100).round(1)

ultimo_tri = gold_ms['datatrimestre'].max()
pix_share  = gold_ms[(gold_ms['datatrimestre'] == ultimo_tri) & (gold_ms['meio'] == 'Pix')]['percentual'].iloc[0]

col1.metric("Queda no montante sacado", f"{queda_saques}%", delta=f"{queda_saques}%")
col2.metric("TED desde o pico (2020)", f"{queda_ted}%", delta=f"{queda_ted}%")
col3.metric("Pix — participação atual", f"{pix_share}%")

# ---------------------------------------------------------------------------
# 1. Queda no uso de dinheiro em espécie
# ---------------------------------------------------------------------------
st.divider()
st.header("Queda no Uso de Dinheiro em Espécie (2015–2026)")
st.write(
    "Montante sacado em caixas eletrônicos por trimestre. A trajetória de queda reflete a "
    "migração do dinheiro físico para meios digitais, acelerada pela pandemia e pelo Pix."
)

graphic_saques = px.line(
    gold_saques, x='datatrimestre', y='valorSaques',
    labels={'valorSaques': 'Montante sacado (R$)', 'datatrimestre': 'Trimestre'},
)
graphic_saques.update_xaxes(hoverformat='%Y-%m-%d')
graphic_saques.add_vline(x='2020-03-01', line_dash='dash', line_color='red', annotation_text='Pandemia')
graphic_saques.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')
st.plotly_chart(graphic_saques, key="saques")

# Tabela de apoio (data sem horário, montante em trilhões para leitura)
saques_display = gold_saques.copy()
saques_display['Trimestre']                = saques_display['datatrimestre'].dt.strftime('%Y-%m-%d')
saques_display['Montante sacado (R$ tri)'] = (saques_display['valorSaques'] / 1e12).round(3)
saques_display['Variação (%)']             = saques_display['variacao_porc']
saques_display = saques_display[['Trimestre', 'Montante sacado (R$ tri)', 'Variação (%)']]
st.dataframe(saques_display, use_container_width=True, hide_index=True)

st.info(
    "Leitura: em 2015 o país sacava cerca de R$ 1,1 trilhão por trimestre em caixas "
    "eletrônicos. Em 2026 esse montante caiu para a faixa de R$ 0,46 trilhão. As quedas "
    "mais acentuadas coincidem com o início da pandemia (março de 2020) e com a adoção do "
    "Pix (a partir de novembro de 2020)."
)

# ---------------------------------------------------------------------------
# 2. TED: crescimento e estagnação
# ---------------------------------------------------------------------------
st.divider()
st.header("TED: Crescimento e Estagnação")
st.write(
    "Número de transações via TED por trimestre. O volume cresceu de forma consistente até "
    "o fim de 2020 e passou a recuar com a popularização do Pix."
)

graphic_ted = px.line(
    gold_ted, x='datatrimestre', y='quantidadeTED',
    labels={'quantidadeTED': 'Nº de transações TED', 'datatrimestre': 'Trimestre'},
)
graphic_ted.update_xaxes(hoverformat='%Y-%m-%d')
graphic_ted.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')
st.plotly_chart(graphic_ted, key="ted")

st.info(
    "Leitura: o número de TEDs atingiu o pico no quarto trimestre de 2020 e, a partir daí, "
    "entrou em declínio. O Pix passou a absorver as transferências do dia a dia, antes feitas "
    "por TED."
)

# ---------------------------------------------------------------------------
# 3. TED vs DOC vs Pix
# ---------------------------------------------------------------------------
st.divider()
st.header("TED vs DOC vs Pix (2015–2026)")
st.write("Comparação do número de transferências entre os três meios ao longo do período.")

graphic_transf = px.line(
    gold_transf, x='datatrimestre',
    y=['quantidadeTED', 'quantidadeDOC', 'quantidadePix'],
    labels={'value': 'Nº de transações', 'datatrimestre': 'Trimestre', 'variable': 'Meio'},
)
graphic_transf.update_xaxes(hoverformat='%Y-%m-%d')
graphic_transf.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')
graphic_transf.add_vline(x='2024-01-01', line_dash='dash', line_color='orange', annotation_text='DOC descontinuado')
st.plotly_chart(graphic_transf, key="transf")

st.info(
    "Leitura: em número de transações o Pix dispara e ultrapassa o TED já em 2021. O DOC, "
    "que vinha em queda, foi descontinuado em 2024 e zera no fim da série."
)

# ---------------------------------------------------------------------------
# 4. Pix vs Cartão de Débito
# ---------------------------------------------------------------------------
st.divider()
st.header("O Momento em que o Pix Superou o Débito")
st.write(
    "Número de transações via Pix e via cartão de débito. O cruzamento marca quando o Pix "
    "passou a ser mais usado que um meio consolidado há décadas."
)

crossover = gold_pix_deb[
    gold_pix_deb['quantidadePix'] >= gold_pix_deb['quantidadeCartaoDebito']
]['datatrimestre'].min()

graphic_pix_deb = px.line(
    gold_pix_deb, x='datatrimestre',
    y=['quantidadePix', 'quantidadeCartaoDebito'],
    labels={'value': 'Nº de transações', 'datatrimestre': 'Trimestre', 'variable': 'Meio'},
)
graphic_pix_deb.update_xaxes(hoverformat='%Y-%m-%d')
if pd.notna(crossover):
    graphic_pix_deb.add_vline(x=str(crossover), line_dash='dash', line_color='yellow',
                              annotation_text='Pix supera o Débito')
st.plotly_chart(graphic_pix_deb, key="pix_deb")

st.info(
    "Leitura: no primeiro trimestre de 2022 o Pix ultrapassou o cartão de débito em número "
    "de transações, evidenciando uma velocidade de adoção sem precedentes."
)

# ---------------------------------------------------------------------------
# 5. Market share: primeiro vs último trimestre
# ---------------------------------------------------------------------------
st.divider()

datas     = pd.to_datetime(gold_ms['datatrimestre'].sort_values().unique())
data_ini  = datas[0]
data_fim  = datas[-1]
label_ini = f"{data_ini.year} — Q{(data_ini.month - 1) // 3 + 1}"
label_fim = f"{data_fim.year} — Q{(data_fim.month - 1) // 3 + 1}"

st.header(f"Participação por Meio de Pagamento: {label_ini} vs {label_fim}")
st.write("Participação de cada meio no total de transações, medida pelo número de transações.")

ms_ini = gold_ms[gold_ms['datatrimestre'] == datas[0]]
ms_fim = gold_ms[gold_ms['datatrimestre'] == datas[-1]]

col_a, col_b = st.columns(2)
with col_a:
    st.subheader(label_ini)
    st.plotly_chart(px.pie(ms_ini, names='meio', values='percentual', hole=0.4), key="ms_ini")
with col_b:
    st.subheader(label_fim)
    st.plotly_chart(px.pie(ms_fim, names='meio', values='percentual', hole=0.4), key="ms_fim")

st.info(
    "Leitura: em 2015 o Pix ainda não existia e o cartão de débito liderava em número de "
    "transações. No fim da série o Pix concentra mais da metade do mercado, sintetizando a "
    "transformação dos meios de pagamento no Brasil ao longo da década."
)
