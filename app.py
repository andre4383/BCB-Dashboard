import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from silver import silver_data_extract

st.set_page_config(page_title="Dashboard BCB", layout="wide")

st.title("Dashboard do Banco Central do Brasil")
st.markdown("Análise da evolução dos meios de pagamento no Brasil ao longo da última década (2015 - 2025).")

@st.cache_data
def load_data():
    return silver_data_extract()

df = load_data()

tab1, tab2, tab3 = st.tabs([
    "Queda de Saques", 
    "Evolução de Transações", 
    "Crescimento do TED"
])

with tab1:
    st.header("Queda de Saques no Brasil (2015-2026)")
    st.write("Análise mostrando como o uso de dinheiro em espécie vem caindo, especialmente afetado pela pandemia e pelo lançamento do Pix.")
    
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df['datatrimestre'], df['quantidadeSaques'], linewidth=2)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    pand_date = pd.to_datetime('2020-03-01')
    pix_date = pd.to_datetime('2020-11-01')
    
    ax1.axvline(x=pand_date, color='red', linestyle='--', label='Início da Pandemia')
    ax1.axvline(x=pix_date, color='green', linestyle='--', label='Lançamento do Pix')
    ax1.legend()
    ax1.set_ylabel("Quantidade (em milhares)")
    ax1.set_xlabel("Trimestre")
    
    st.pyplot(fig1)
    
    st.info("**O que isso significa:** Este gráfico ilustra como as pessoas estão sacando menos dinheiro físico. Note que as quedas mais bruscas coincidem com o início da pandemia (março/2020) e com o lançamento do Pix (novembro/2020).")
    
with tab2:
    st.header("Evolução do volume total de transações")
    st.write("Visão macro do crescimento exponencial do mercado de pagamentos brasileiro.")
    
    valor_total = df.filter(like='valor').sum(axis=1)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(df['datatrimestre'], valor_total, linewidth=2, color='orange')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    ax2.set_ylabel("Volume de Transações (em milhares)")
    ax2.set_xlabel("Trimestre")
    
    st.pyplot(fig2)
    
    st.info("**O que isso significa:** Aqui vemos que o volume total de dinheiro transacionado continua subindo com o tempo. Isso mostra o crescimento acelerado da economia digital no Brasil.")

with tab3:
    st.header("TED: Crescimento e Estagnação")
    st.write("O TED teve um crescimento impressionante na década, mas estagnou com o lançamento do Pix.")
    
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(df['datatrimestre'], df['valorTED'], linewidth=2, color='purple')
    
    pix_date = pd.to_datetime('2020-11-01')
    ax3.axvline(x=pix_date, color='red', linestyle='--', label='Lançamento do Pix')
    ax3.legend()
    
    ax3.set_ylabel("Valor da TED (em milhões)")
    ax3.set_xlabel("Trimestre")
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot(fig3)
    
    st.info("**O que isso significa:** A TED vinha em uma trajetória de alto crescimento. Porém, assim que o Pix foi lançado (linha vermelha), a TED parou de crescer e se estabilizou, indicando que as pessoas preferem usar o Pix no dia a dia.")
