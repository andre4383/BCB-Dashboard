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

st.title("Dashboard do Banco Central do Brasil")
st.markdown("Análise da evolução dos meios de pagamento no Brasil ao longo da última década (2015 - 2026).")

# --- Métricas ---
col1, col2, col3 = st.columns(3)

primeiro_saque = gold_saques['quantidadeSaques'].iloc[0]
ultimo_saque   = gold_saques['quantidadeSaques'].iloc[-1]
queda          = ((ultimo_saque - primeiro_saque) / primeiro_saque * 100).round(1)

primeiro_ted = gold_ted['valorTED'].iloc[0]
ultimo_ted   = gold_ted['valorTED'].iloc[-1]
cresc_ted    = ((ultimo_ted - primeiro_ted) / primeiro_ted * 100).round(1)

pix_data     = gold_transf[gold_transf['valorPix'] > 0]
primeiro_pix = pix_data['valorPix'].iloc[0]
ultimo_pix   = pix_data['valorPix'].iloc[-1]
cresc_pix    = ((ultimo_pix - primeiro_pix) / primeiro_pix * 100).round(1)

col1.metric("Queda de Saques", f"{queda}%", delta=f"{queda}%")
col2.metric("Crescimento TED", f"{cresc_ted}%", delta=f"{cresc_ted}%")
col3.metric("Crescimento Pix", f"{cresc_pix}%", delta=f"{cresc_pix}%")

# --- 1. Queda de Saques ---
st.header("Queda de Saques no Brasil (2015-2026)")
st.write("Análise mostrando como o uso de dinheiro em espécie vem caindo, especialmente afetado pela pandemia e pelo lançamento do Pix.")

graphic_saques = px.line(gold_saques, x='datatrimestre', y='quantidadeSaques',
                          labels={'quantidadeSaques': 'Quantidade de Saques', 'datatrimestre': 'Trimestre'})
graphic_saques.add_vline(x='2020-03-01', line_dash='dash', line_color='red', annotation_text='Pandemia')
graphic_saques.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')

st.plotly_chart(graphic_saques, key="saques")
st.dataframe(gold_saques, use_container_width=True, hide_index=True)
st.info("**O que isso significa:** Este gráfico ilustra como as pessoas estão sacando menos dinheiro físico. Note que as quedas mais bruscas coincidem com o início da pandemia (março/2020) e com o lançamento do Pix (novembro/2020).")

# --- 2. TED: Crescimento e Estagnação ---
st.divider()
st.header("TED: Crescimento e Estagnação")
st.write("O TED teve um crescimento impressionante na década, mas estagnou com o lançamento do Pix.")

graphic_ted = px.line(gold_ted, x='datatrimestre', y='valorTED',
                       labels={'valorTED': 'Valor TED (R$)', 'datatrimestre': 'Trimestre'})
graphic_ted.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')

st.plotly_chart(graphic_ted, key="ted")
st.info("**O que isso significa:** A TED vinha em uma trajetória de alto crescimento. Porém, assim que o Pix foi lançado, a TED parou de crescer e se estabilizou, indicando que as pessoas preferem usar o Pix no dia a dia.")

# --- 3. TED vs DOC vs Pix ---
st.divider()
st.header("TED vs DOC vs Pix (2015–2026)")
st.write("Como o Pix substituiu TED e DOC nas transferências eletrônicas.")

graphic_transf = px.line(gold_transf, x='datatrimestre',
                          y=['valorTED', 'valorDOC', 'valorPix'],
                          labels={'value': 'Valor (R$)', 'datatrimestre': 'Trimestre', 'variable': 'Meio'})
graphic_transf.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')
graphic_transf.add_vline(x='2024-01-01', line_dash='dash', line_color='orange', annotation_text='DOC descontinuado')

st.plotly_chart(graphic_transf, key="transf")
st.info("**O que isso significa:** Com o lançamento do Pix, o DOC foi rapidamente abandonado e descontinuado em 2024. O TED resistiu mais, mas também perdeu força.")

# --- 4. Pix vs Cartão de Débito ---
st.divider()
st.header("O momento em que o Pix superou o Débito")
st.write("O Pix cresceu tão rapidamente que superou o cartão de débito em volume transacionado.")



crossover = gold_pix_deb[
    gold_pix_deb['valorPix'] >= gold_pix_deb['valorCartaoDebito']
]['datatrimestre'].min()

graphic_pix_deb = px.line(gold_pix_deb, x='datatrimestre',
                            y=['valorPix', 'valorCartaoDebito'],
                            labels={'value': 'Valor (R$)', 'datatrimestre': 'Trimestre', 'variable': 'Meio'})
if pd.notna(crossover):
    graphic_pix_deb.add_vline(x=str(crossover), line_dash='dash', line_color='yellow',
                               annotation_text='Pix supera Débito')

st.plotly_chart(graphic_pix_deb, key="pix_deb")
st.info("**O que isso significa:** Em poucos anos após o lançamento, o Pix superou o cartão de débito — um meio de pagamento consolidado há décadas — mostrando a velocidade de adoção sem precedentes.")

# --- 5. Market Share: primeiro vs último trimestre ---
st.divider()

datas      = pd.to_datetime(gold_ms['datatrimestre'].sort_values().unique())
data_ini   = datas[0]
data_fim   = datas[-1]
label_ini  = f"{data_ini.year} — Q{(data_ini.month - 1) // 3 + 1}"
label_fim  = f"{data_fim.year} — Q{(data_fim.month - 1) // 3 + 1}"

st.header(f"Market Share: {label_ini} vs {label_fim}")
st.write("Como o mix de meios de pagamento transformou-se em uma década.")

ms_ini = gold_ms[gold_ms['datatrimestre'] == datas[0]]
ms_fim = gold_ms[gold_ms['datatrimestre'] == datas[-1]]

col_a, col_b = st.columns(2)
with col_a:
    st.subheader(label_ini)
    st.plotly_chart(px.pie(ms_ini, names='meio', values='percentual', hole=0.4), key="ms_ini")
with col_b:
    st.subheader(label_fim)
    st.plotly_chart(px.pie(ms_fim, names='meio', values='percentual', hole=0.4), key="ms_fim")

st.info("**O que isso significa:** Em 2015, Pix não existia. Em 2025, ele domina o mix. Este donut mostra a revolução dos meios de pagamento no Brasil em uma única imagem.")
