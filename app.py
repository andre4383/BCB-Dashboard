import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


st.set_page_config(page_title="BCB Dashboard", layout="wide")

@st.cache_data
def load_data():
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    gold_volume = pd.read_sql('gold_volume_total', engine)
    gold_saques = pd.read_sql('gold_saques', engine)
    gold_ted = pd.read_sql('gold_ted_cres', engine)
    return gold_volume, gold_saques, gold_ted

gold_volume, gold_saques, gold_ted = load_data()

st.title("Dashboard do Banco Central do Brasil")
st.markdown("Análise da evolução dos meios de pagamento no Brasil ao longo da última década (2015 - 2025).")


col1, col2, col3 = st.columns(3)
col1, col2, col3 = st.columns(3)

primeiro_saque = gold_saques['quantidadeSaques'].iloc[0]
ultimo_saque = gold_saques['quantidadeSaques'].iloc[-1]
queda = ((ultimo_saque - primeiro_saque) / primeiro_saque * 100).round(1)

primeiro_ted = gold_ted['valorTED'].iloc[0]
ultimo_ted = gold_ted['valorTED'].iloc[-1]
cresc_ted = ((ultimo_ted - primeiro_ted) / primeiro_ted * 100).round(1)

primeiro_vol = gold_volume['volume_total'].iloc[0]
ultimo_vol = gold_volume['volume_total'].iloc[-1]
cresc_vol = ((ultimo_vol - primeiro_vol) / primeiro_vol * 100).round(1)

col1.metric("Queda de Saques", f"{queda}%", delta=f"{queda}%")
col2.metric("Crescimento TED", f"{cresc_ted}%", delta=f"{cresc_ted}%")
col3.metric("Volume Total", f"{cresc_vol}%", delta=f"{cresc_vol}%")

st.header("Queda de Saques no Brasil (2015-2026)")
st.write("Análise mostrando como o uso de dinheiro em espécie vem caindo, especialmente afetado pela pandemia e pelo lançamento do Pix.")

primeiro = gold_saques['quantidadeSaques'].iloc[0]  
ultimo = gold_saques['quantidadeSaques'].iloc[-1]     
queda = ((ultimo - primeiro) / primeiro * 100).round(1)

col1.metric("Queda de Saques", f"{queda}%")

graphic_saques = px.line(gold_saques, x='datatrimestre', y='quantidadeSaques')
graphic_saques.add_vline(x='2020-03-01', line_dash='dash', line_color='red', annotation_text='Pandemia')
graphic_saques.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')

st.plotly_chart(graphic_saques)

st.info("**O que isso significa:** Este gráfico ilustra como as pessoas estão sacando menos dinheiro físico. Note que as quedas mais bruscas coincidem com o início da pandemia (março/2020) e com o lançamento do Pix (novembro/2020).")
st.divider()
st.header("Evolução do volume total de transações")
st.write("Visão macro do crescimento exponencial do mercado de pagamentos brasileiro.")

graphic_transaction = px.line(gold_volume, x= 'datatrimestre', y = 'volume_total')

st.plotly_chart(graphic_transaction)

st.info("**O que isso significa:** Aqui vemos que o volume total de dinheiro transacionado continua subindo com o tempo. Isso mostra o crescimento acelerado da economia digital no Brasil.")

st.divider()
st.header("TED: Crescimento e Estagnação")
st.write("O TED teve um crescimento impressionante na década, mas estagnou com o lançamento do Pix.")

graphic_ted = px.line(gold_ted, x= 'datatrimestre',y = 'valorTED' )
graphic_ted.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')

st.plotly_chart(graphic_ted)

st.info("**O que isso significa:** A TED vinha em uma trajetória de alto crescimento. Porém, assim que o Pix foi lançado (linha vermelha), a TED parou de crescer e se estabilizou, indicando que as pessoas preferem usar o Pix no dia a dia.")