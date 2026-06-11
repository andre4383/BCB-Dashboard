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

# ── Conversão de escala ──────────────────────────────────────────────────────
# Todos os valores da API do BCB estão em REAIS ABSOLUTOS.
# Convertemos para trilhões (÷ 1e12) para legibilidade nos gráficos.
TRILHAO = 1e12
BILHAO  = 1e9

def fmt_tri(val):
    """Formata um valor em reais para string em trilhões."""
    return f"R$ {val / TRILHAO:.2f} tri"

# Colunas de valor → trilhões
for col in ['valorTED']:
    gold_ted[col + '_tri'] = gold_ted[col] / TRILHAO

for col in ['valorTED', 'valorDOC', 'valorPix']:
    gold_transf[col + '_tri'] = gold_transf[col] / TRILHAO

for col in ['valorPix', 'valorCartaoDebito']:
    gold_pix_deb[col + '_tri'] = gold_pix_deb[col] / TRILHAO

# quantidadeSaques da API já está em unidades absolutas (não em milhares)
# dividimos por 1 milhão para exibir em "milhões de operações"
gold_saques['saques_tri'] = gold_saques['valorSaques'] / TRILHAO

# ── Métricas ─────────────────────────────────────────────────────────────────
st.title("Dashboard do Banco Central do Brasil")
st.markdown("Análise da evolução dos meios de pagamento no Brasil ao longo da última década (2015–2026).")

col1, col2, col3 = st.columns(3)

primeiro_saque = gold_saques['quantidadeSaques'].iloc[0]
ultimo_saque   = gold_saques['quantidadeSaques'].iloc[-1]
queda          = ((ultimo_saque - primeiro_saque) / primeiro_saque * 100).round(1)

primeiro_ted = gold_ted['valorTED'].iloc[0]
ultimo_ted   = gold_ted['valorTED'].iloc[-1]
cresc_ted    = ((ultimo_ted - primeiro_ted) / primeiro_ted * 100).round(1)

pix_data  = gold_transf[gold_transf['valorPix'] > 0]
ultimo_pix = pix_data['valorPix'].iloc[-1]

col1.metric("Queda de Saques",  f"{queda}%",      delta=f"{queda}%",     delta_color="inverse")
col2.metric("Crescimento TED",  f"{cresc_ted}%",  delta=f"{cresc_ted}%")
col3.metric("Pix (último tri.)", f"R$ {ultimo_pix/TRILHAO:.1f} tri", delta="Q1 2026")

# ── 1. Queda de Saques ───────────────────────────────────────────────────────
st.header("Queda de Saques no Brasil (2015–2026)")
st.write("Análise mostrando como o uso de dinheiro em espécie vem caindo, especialmente afetado pela pandemia e pelo lançamento do Pix.")

fig_saques = px.line(
    gold_saques,
    x='datatrimestre',
    y='saques_tri',
    labels={'saques_tri': 'Valor Sacado (R$ trilhões)', 'datatrimestre': 'Trimestre'},
)
fig_saques.add_vline(x='2020-03-01', line_dash='dash', line_color='red',   annotation_text='Pandemia')
fig_saques.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')
fig_saques.update_yaxes(tickformat='.2f', ticksuffix=' tri')
st.plotly_chart(fig_saques, use_container_width=True, key="saques")
st.dataframe(gold_saques[['datatrimestre', 'valorSaques', 'quantidadeSaques', 'variacao_porc']], use_container_width=True, hide_index=True)
st.info("**O que isso significa:** Este gráfico ilustra como as pessoas estão sacando menos dinheiro físico. Note que as quedas mais bruscas coincidem com o início da pandemia (março/2020) e com o lançamento do Pix (novembro/2020).")

# ── 2. TED: Crescimento e Estagnação ────────────────────────────────────────
st.divider()
st.header("TED: Crescimento e Estagnação")
st.write("O TED teve um crescimento impressionante na década, mas estagnou com o lançamento do Pix.")

fig_ted = px.line(
    gold_ted,
    x='datatrimestre',
    y='valorTED_tri',
    labels={'valorTED_tri': 'Valor TED (R$ trilhões)', 'datatrimestre': 'Trimestre'},
)
fig_ted.add_vline(x='2020-11-01', line_dash='dash', line_color='green', annotation_text='Lançamento do Pix')
fig_ted.update_yaxes(tickformat=".1f", ticksuffix=" tri")
st.plotly_chart(fig_ted, use_container_width=True, key="ted")
st.info("**O que isso significa:** A TED vinha em uma trajetória de alto crescimento. Porém, assim que o Pix foi lançado, a TED parou de crescer e se estabilizou, indicando que as pessoas preferem usar o Pix no dia a dia.")

# ── 3. TED vs DOC vs Pix ────────────────────────────────────────────────────
st.divider()
st.header("TED vs DOC vs Pix (2015–2026)")
st.write("Como o Pix substituiu TED e DOC nas transferências eletrônicas.")
st.caption("⚠️ Eixo Y em escala logarítmica para que DOC (R$ bilhões) e TED/Pix (R$ trilhões) apareçam no mesmo gráfico.")

# DOC está em bilhões; TED e Pix em trilhões — usar log_y para mostrar todos juntos
gold_transf['valorDOC_bi'] = gold_transf['valorDOC'] / BILHAO   # bilhões
gold_transf['valorTED_bi'] = gold_transf['valorTED'] / BILHAO
gold_transf['valorPix_bi'] = gold_transf['valorPix'] / BILHAO

fig_transf = px.line(
    gold_transf,
    x='datatrimestre',
    y=['valorTED_bi', 'valorDOC_bi', 'valorPix_bi'],
    log_y=True,
    labels={
        'value': 'Valor (R$ bilhões, escala log)',
        'datatrimestre': 'Trimestre',
        'variable': 'Meio',
    },
)
newnames = {'valorTED_bi': 'TED', 'valorDOC_bi': 'DOC', 'valorPix_bi': 'Pix'}
fig_transf.for_each_trace(lambda t: t.update(name=newnames.get(t.name, t.name)))
fig_transf.add_vline(x='2020-11-01', line_dash='dash', line_color='green',  annotation_text='Lançamento do Pix')
fig_transf.add_vline(x='2024-01-01', line_dash='dash', line_color='orange', annotation_text='DOC descontinuado')
st.plotly_chart(fig_transf, use_container_width=True, key="transf")
st.info("**O que isso significa:** O DOC sempre foi muito menor que o TED (R$40–52 bi vs R$3–12 tri). Com o Pix, o DOC foi descontinuado em 2024 e o TED perdeu força. A escala logarítmica permite ver os três instrumentos ao mesmo tempo.")

# ── 4. Pix vs Cartão de Débito ───────────────────────────────────────────────
st.divider()
st.header("O momento em que o Pix superou o Débito")
st.write("O Pix cresceu tão rapidamente que superou o cartão de débito em volume transacionado.")
st.caption("Pix no eixo esquerdo (R$ trilhões) · Cartão de Débito no eixo direito (R$ bilhões) para que ambos fiquem visíveis.")

crossover = gold_pix_deb[
    gold_pix_deb['valorPix'] >= gold_pix_deb['valorCartaoDebito']
]['datatrimestre'].min()

import plotly.graph_objects as go

fig_pix_deb = go.Figure()
fig_pix_deb.add_trace(go.Scatter(
    x=gold_pix_deb['datatrimestre'],
    y=gold_pix_deb['valorPix'] / TRILHAO,
    name='Pix (eixo esq.)',
    yaxis='y1',
    line=dict(color='royalblue'),
))
fig_pix_deb.add_trace(go.Scatter(
    x=gold_pix_deb['datatrimestre'],
    y=gold_pix_deb['valorCartaoDebito'] / BILHAO,
    name='Cartão de Débito (eixo dir.)',
    yaxis='y2',
    line=dict(color='tomato'),
))
fig_pix_deb.update_layout(
    xaxis=dict(title='Trimestre'),
    yaxis=dict(title='Pix (R$ trilhões)', tickformat='.1f', ticksuffix=' tri'),
    yaxis2=dict(title='Débito (R$ bilhões)', tickformat='.0f', ticksuffix=' bi',
                overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99),
)
if pd.notna(crossover):
    fig_pix_deb.add_vline(
        x=str(crossover), line_dash='dash', line_color='gold',
        annotation_text='Pix supera Débito'
    )
st.plotly_chart(fig_pix_deb, use_container_width=True, key="pix_deb")
st.info("**O que isso significa:** O cartão de débito estava em R$91–264 bilhões/trimestre. O Pix chegou a R$10 trilhões/trimestre — ~40x maior. Os eixos separados mostram a trajetória de cada um sem esconder o débito.")

# ── 5. Market Share ──────────────────────────────────────────────────────────
st.divider()

datas     = pd.to_datetime(gold_ms['datatrimestre'].sort_values().unique())
data_ini  = datas[0]
data_fim  = datas[-1]
label_ini = f"{data_ini.year} — Q{(data_ini.month - 1) // 3 + 1}"
label_fim = f"{data_fim.year} — Q{(data_fim.month - 1) // 3 + 1}"

st.header(f"Market Share: {label_ini} vs {label_fim}")
st.write("Como o mix de meios de pagamento transformou-se em uma década.")

# Nomes legíveis para o market share
nome_legivel = {
    'TED':                  'TED',
    'Pix':                  'Pix',
    'TransIntrabancaria':   'Transf. Intrabancária',
    'Boleto':               'Boleto',
    'CartaoCredito':        'Cartão de Crédito',
    'CartaoDebito':         'Cartão de Débito',
    'DebitoDireto':         'Débito Direto',
    'Convenios':            'Convênios',
    'Cheque':               'Cheque',
    'DOC':                  'DOC',
    'CartaoPrePago':        'Cartão Pré-pago',
    'TEC':                  'TEC',
    'Saques':               'Saques',
}

for df_ms in [gold_ms]:
    df_ms['meio_legivel'] = df_ms['meio'].map(lambda m: nome_legivel.get(m, m))

ms_ini = gold_ms[gold_ms['datatrimestre'] == datas[0]]
ms_fim = gold_ms[gold_ms['datatrimestre'] == datas[-1]]

col_a, col_b = st.columns(2)
with col_a:
    st.subheader(label_ini)
    st.plotly_chart(
        px.pie(ms_ini, names='meio_legivel', values='percentual', hole=0.4),
        use_container_width=True, key="ms_ini"
    )
with col_b:
    st.subheader(label_fim)
    st.plotly_chart(
        px.pie(ms_fim, names='meio_legivel', values='percentual', hole=0.4),
        use_container_width=True, key="ms_fim"
    )

st.info("**O que isso significa:** Em 2015, Pix não existia. Em 2026, ele domina o mix. Este donut mostra a revolução dos meios de pagamento no Brasil em uma única imagem.")
