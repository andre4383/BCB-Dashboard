"""
Gera gráficos estáticos modernos usando Plotly.
Foco em visualização minimalista, sem legenda e em formato quadrado/retrato 
para ocupar apenas metade do slide.
"""

import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine

os.makedirs("charts", exist_ok=True)

engine  = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
saques  = pd.read_sql("gold_saques",         engine)
ted     = pd.read_sql("gold_ted_cres",       engine)
transf  = pd.read_sql("gold_transferencias", engine)
pix_deb = pd.read_sql("gold_pix_vs_debito",  engine)
gold_ms = pd.read_sql("gold_market_share",   engine)

saques['datatrimestre'] = saques['datatrimestre'].astype(str)
ted['datatrimestre'] = ted['datatrimestre'].astype(str)
transf['datatrimestre'] = transf['datatrimestre'].astype(str)
pix_deb['datatrimestre'] = pix_deb['datatrimestre'].astype(str)
gold_ms['datatrimestre'] = gold_ms['datatrimestre'].astype(str)

TRILHAO = 1e12
BILHAO  = 1e9

# Dimensões compactas para caber em meia-tela no slide
WIDTH = 600
HEIGHT = 550

# Cores vibrantes
COLOR_PIX = "#10b981"    # Verde esmeralda
COLOR_TED = "#6366f1"    # Roxo índigo
COLOR_DOC = "#f59e0b"    # Laranja
COLOR_SAQUE = "#3b82f6"  # Azul
COLOR_DEB = "#ef4444"    # Vermelho

# Configuração de fonte moderna e limpa
LAYOUT_DEFAULTS = dict(
    width=WIDTH,
    height=HEIGHT,
    template="plotly_white",
    showlegend=False,
    margin=dict(l=20, r=60, t=80, b=40),
    font=dict(family="Inter, Roboto, sans-serif", size=13, color="#475569"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

def format_axes(fig, y_title="", y_tickformat=""):
    fig.update_xaxes(
        showgrid=False, 
        zeroline=False, 
        showline=True, linewidth=1, linecolor="#cbd5e1"
    )
    fig.update_yaxes(
        title=y_title,
        showgrid=True, gridwidth=1, gridcolor="#f1f5f9",
        zeroline=False,
        tickformat=y_tickformat,
        showline=False
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# 1. QUEDA DE SAQUES
# ─────────────────────────────────────────────────────────────────────────────
fig = go.Figure()
y_tri = saques["valorSaques"] / TRILHAO
x_date = saques["datatrimestre"]

fig.add_trace(go.Scatter(
    x=x_date, y=y_tri,
    mode='lines',
    line=dict(color=COLOR_SAQUE, width=4, shape='spline', smoothing=0.3),
    fill='tozeroy',
    fillcolor='rgba(59, 130, 246, 0.1)'
))

# Anotação na ponta da linha
fig.add_annotation(
    x=x_date.iloc[-1], y=y_tri.iloc[-1],
    text="<b>Queda de 60%</b>",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor=COLOR_SAQUE,
    ax=0, ay=-40, font=dict(color=COLOR_SAQUE, size=14)
)

# Eventos
fig.add_vline(x="2020-11-01", line_width=1, line_dash="dash", line_color=COLOR_PIX)
fig.add_annotation(
    x="2020-11-01", y=y_tri.max(), text="Lançamento do Pix",
    showarrow=False, xanchor="left", xshift=5, font=dict(color=COLOR_PIX, size=11)
)

fig.update_layout(
    title=dict(text="<b>Queda de Saques em Espécie</b><br><sup>Valores em R$ trilhões por trimestre</sup>", font_size=20, font_color="#0f172a"),
    **LAYOUT_DEFAULTS
)
format_axes(fig, y_tickformat=".2f")
fig.update_yaxes(ticksuffix=" tri")
fig.write_image("charts/1_queda_saques.png", scale=2)
print("✔ charts/1_queda_saques.png")


# ─────────────────────────────────────────────────────────────────────────────
# 2. TED – CRESCIMENTO E ESTAGNAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
fig = go.Figure()
x_date = ted["datatrimestre"]
y_tri = ted["valorTED"] / TRILHAO
pre = ted["periodo"] == "pre_pix"
pos = ted["periodo"] == "pos_pix"

fig.add_trace(go.Scatter(
    x=x_date[pre], y=y_tri[pre],
    mode='lines',
    line=dict(color=COLOR_TED, width=4, shape='spline')
))
fig.add_trace(go.Scatter(
    x=x_date[pos], y=y_tri[pos],
    mode='lines',
    line=dict(color="#94a3b8", width=4, dash='dot', shape='spline') # Cinza pontilhado
))

fig.add_annotation(
    x=x_date[pre].iloc[-1], y=y_tri[pre].iloc[-1],
    text="<b>Crescimento (+112%)</b>", showarrow=False,
    xanchor="right", xshift=-10, font=dict(color=COLOR_TED, size=13)
)
fig.add_annotation(
    x=x_date[pos].iloc[-1], y=y_tri[pos].iloc[-1],
    text="<b>Estagnação</b>", showarrow=False,
    xanchor="left", xshift=10, font=dict(color="#94a3b8", size=13)
)

fig.add_vline(x="2020-11-01", line_width=1, line_dash="dash", line_color=COLOR_PIX)
fig.add_annotation(
    x="2020-11-01", y=y_tri.max(), text="Pix",
    showarrow=False, xanchor="left", xshift=5, font=dict(color=COLOR_PIX, size=12)
)

fig.update_layout(
    title=dict(text="<b>Efeito do Pix no TED</b><br><sup>Valores em R$ trilhões por trimestre</sup>", font_size=20, font_color="#0f172a"),
    **LAYOUT_DEFAULTS
)
format_axes(fig, y_tickformat=".1f")
fig.update_yaxes(ticksuffix=" tri")
fig.write_image("charts/2_ted_crescimento.png", scale=2)
print("✔ charts/2_ted_crescimento.png")


# ─────────────────────────────────────────────────────────────────────────────
# 3. TED vs DOC vs PIX (escala log)
# ─────────────────────────────────────────────────────────────────────────────
fig = go.Figure()
x_date = transf["datatrimestre"]

# Filtrar zeros e nulos
doc_data = transf[transf['valorDOC'] > 0]

fig.add_trace(go.Scatter(x=x_date, y=transf["valorTED"]/BILHAO, mode='lines', line=dict(color=COLOR_TED, width=3, shape='spline')))
fig.add_trace(go.Scatter(x=doc_data["datatrimestre"], y=doc_data["valorDOC"]/BILHAO, mode='lines', line=dict(color=COLOR_DOC, width=3, shape='spline')))
fig.add_trace(go.Scatter(x=transf[transf["valorPix"]>0]["datatrimestre"], y=transf[transf["valorPix"]>0]["valorPix"]/BILHAO, mode='lines', line=dict(color=COLOR_PIX, width=4, shape='spline')))

# Inline labels
fig.add_annotation(x=x_date.iloc[-1], y=transf["valorTED"].iloc[-1]/BILHAO, text="<b>TED</b>", showarrow=False, xanchor="left", xshift=10, font=dict(color=COLOR_TED, size=14))
fig.add_annotation(x=x_date.iloc[-1], y=transf["valorPix"].iloc[-1]/BILHAO, text="<b>Pix</b>", showarrow=False, xanchor="left", xshift=10, font=dict(color=COLOR_PIX, size=14))
fig.add_annotation(x=doc_data["datatrimestre"].iloc[-1], y=doc_data["valorDOC"].iloc[-1]/BILHAO, text="<b>DOC (extinto)</b>", showarrow=False, xanchor="left", xshift=10, font=dict(color=COLOR_DOC, size=14))

fig.update_layout(
    title=dict(text="<b>O Fim do DOC e a Era do Pix</b><br><sup>Valores em R$ bilhões (escala log)</sup>", font_size=20, font_color="#0f172a"),
    yaxis_type="log",
    **LAYOUT_DEFAULTS
)
format_axes(fig)
fig.update_yaxes(tickformat=",", tickprefix="R$ ", ticksuffix=" bi")
fig.write_image("charts/3_ted_doc_pix.png", scale=2)
print("✔ charts/3_ted_doc_pix.png")


# ─────────────────────────────────────────────────────────────────────────────
# 4. PIX vs CARTÃO DE DÉBITO
# ─────────────────────────────────────────────────────────────────────────────
fig = go.Figure()
x_date = pix_deb["datatrimestre"]

# Aqui como é eixo duplo mas minimalista, vamos converter os dois pra bilhões ou trilhões?
# Vamos converter tudo para BILHÕES para que ambos os eixos tenham o mesmo sufixo " bi",
# mas como o Pix chega a 10 trilhões (10.000 bilhões), vamos exibir a grandeza limpa
fig.add_trace(go.Scatter(
    x=x_date, y=pix_deb["valorPix"]/TRILHAO,
    mode='lines', line=dict(color=COLOR_PIX, width=4, shape='spline'),
    yaxis="y1"
))
fig.add_trace(go.Scatter(
    x=x_date, y=pix_deb["valorCartaoDebito"]/BILHAO,
    mode='lines', line=dict(color=COLOR_DEB, width=3, shape='spline'),
    yaxis="y2"
))

# Labels inline
fig.add_annotation(x=x_date.iloc[-1], y=pix_deb["valorPix"].iloc[-1]/TRILHAO, text="<b>Pix</b>", showarrow=False, xanchor="left", xshift=10, font=dict(color=COLOR_PIX, size=14), yref="y1")
fig.add_annotation(x=x_date.iloc[-1], y=pix_deb["valorCartaoDebito"].iloc[-1]/BILHAO, text="<b>Débito</b>", showarrow=False, xanchor="left", xshift=10, font=dict(color=COLOR_DEB, size=14), yref="y2")

fig.update_layout(
    title=dict(text="<b>Pix vs Cartão de Débito</b><br><sup>Pix em Trilhões (esq) | Débito em Bilhões (dir)</sup>", font_size=20, font_color="#0f172a"),
    yaxis=dict(title=dict(text="Pix (Trilhões)", font_color=COLOR_PIX), tickformat=".1f", ticksuffix=" tri", tickfont=dict(color=COLOR_PIX), showgrid=False, zeroline=False),
    yaxis2=dict(title=dict(text="Débito (Bilhões)", font_color=COLOR_DEB), tickformat=".0f", ticksuffix=" bi", tickfont=dict(color=COLOR_DEB), overlaying="y", side="right", showgrid=False, zeroline=False),
    **LAYOUT_DEFAULTS
)
fig.update_xaxes(showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor="#cbd5e1")
fig.write_image("charts/4_pix_vs_debito.png", scale=2)
print("✔ charts/4_pix_vs_debito.png")


# ─────────────────────────────────────────────────────────────────────────────
# 5. MARKET SHARE: 2015 vs 2026 (Donut)
# ─────────────────────────────────────────────────────────────────────────────
datas = gold_ms['datatrimestre'].sort_values().unique()
ms_ini = gold_ms[gold_ms['datatrimestre'] == datas[0]]
ms_fim = gold_ms[gold_ms['datatrimestre'] == datas[-1]]

# Nomes limpos
nome_legivel = {
    'TED': 'TED', 'Pix': 'Pix', 'TransIntrabancaria': 'Intrabancária',
    'Boleto': 'Boleto', 'CartaoCredito': 'Crédito', 'CartaoDebito': 'Débito',
    'DOC': 'DOC', 'Saques': 'Saques'
}
ms_ini_labels = ms_ini['meio'].map(lambda m: nome_legivel.get(m, m))
ms_fim_labels = ms_fim['meio'].map(lambda m: nome_legivel.get(m, m))

# Criar dois donuts lado a lado
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

fig.add_trace(go.Pie(
    labels=ms_ini_labels, values=ms_ini['percentual'],
    name="2015", hole=0.6,
    textinfo='label+percent', textposition='outside',
    marker=dict(line=dict(color='#ffffff', width=2))
), 1, 1)

fig.add_trace(go.Pie(
    labels=ms_fim_labels, values=ms_fim['percentual'],
    name="2026", hole=0.6,
    textinfo='label+percent', textposition='outside',
    marker=dict(line=dict(color='#ffffff', width=2))
), 1, 2)

# Adicionar o ano no centro do donut
fig.add_annotation(x=0.225, y=0.5, text="<b>2015</b>", showarrow=False, font=dict(size=20, color="#475569"))
fig.add_annotation(x=0.775, y=0.5, text="<b>2026</b>", showarrow=False, font=dict(size=20, color="#475569"))

fig.update_layout(
    title=dict(text="<b>Evolução do Market Share</b><br><sup>Como o Pix revolucionou o mix de pagamentos</sup>", font_size=20, font_color="#0f172a", x=0.05),
    width=700,
    height=400, # Formato paisagem, mas menor
    template="plotly_white",
    showlegend=False,
    margin=dict(l=40, r=40, t=80, b=40),
    font=dict(family="Inter, Roboto, sans-serif", size=11, color="#475569"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
# Agrupar valores pequenos (opcional) limitando o texto
fig.update_traces(textfont_size=11, marker=dict(colors=[COLOR_PIX if l == 'Pix' else COLOR_TED if l == 'TED' else COLOR_DEB if l == 'Débito' else COLOR_DOC if l == 'DOC' else '#cbd5e1' for l in ms_ini_labels]))
fig.write_image("charts/5_market_share.png", scale=2)
print("✔ charts/5_market_share.png")


print("\n✅ Gráficos minimalistas Plotly salvos em charts/")
