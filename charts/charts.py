"""
Gera gráficos estáticos em alta resolução para slide.
Salva os arquivos em charts/
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sqlalchemy import create_engine

os.makedirs("charts", exist_ok=True)

engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
saques = pd.read_sql("gold_saques", engine)
ted    = pd.read_sql("gold_ted_cres", engine)
transf = pd.read_sql("gold_transferencias", engine)
pix_deb = pd.read_sql("gold_pix_vs_debito", engine)

TRILHAO = 1e12
BILHAO  = 1e9

# ── Estilo global ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "axes.grid":         True,
    "grid.color":        "#e8e8e8",
    "grid.linewidth":    0.8,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.spines.left":  False,
    "axes.spines.bottom": False,
    "font.family":       "DejaVu Sans",
    "axes.labelcolor":   "#444444",
    "xtick.color":       "#888888",
    "ytick.color":       "#888888",
    "xtick.labelsize":   11,
    "ytick.labelsize":   11,
})

PAND_DATE = pd.Timestamp("2020-03-01")
PIX_DATE  = pd.Timestamp("2020-11-01")
DOC_DATE  = pd.Timestamp("2024-01-01")

# ─────────────────────────────────────────────────────────────────────────────
# 1. QUEDA DE SAQUES
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))

y = saques["valorSaques"] / TRILHAO
x = pd.to_datetime(saques["datatrimestre"])

ax.plot(x, y, color="#2563eb", linewidth=2.5, zorder=3)
ax.fill_between(x, y, alpha=0.08, color="#2563eb")

ax.axvline(PAND_DATE, color="#ef4444", linewidth=1.5, linestyle="--")
ax.axvline(PIX_DATE,  color="#16a34a", linewidth=1.5, linestyle="--")

ax.text(PAND_DATE, y.max() * 0.97, "  Pandemia\n  Mar/2020",
        color="#ef4444", fontsize=10, va="top")
ax.text(PIX_DATE,  y.max() * 0.97, "  Pix\n  Nov/2020",
        color="#16a34a", fontsize=10, va="top")

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R$ {v:.2f} tri"))
ax.set_xlabel("Trimestre", fontsize=12)
ax.set_ylabel("Valor Sacado (R$ trilhões)", fontsize=12)
ax.set_title("Queda de Saques no Brasil (2015–2026)", fontsize=16, fontweight="bold", pad=16)

plt.tight_layout()
plt.savefig("charts/1_queda_saques.png", dpi=180, bbox_inches="tight")
plt.close()
print("✔ charts/1_queda_saques.png")

# ─────────────────────────────────────────────────────────────────────────────
# 2. TED – CRESCIMENTO E ESTAGNAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))

y = pd.to_numeric(ted["valorTED"]) / TRILHAO
x = pd.to_datetime(ted["datatrimestre"])

pre  = ted["periodo"] == "pre_pix"
pos  = ted["periodo"] == "pos_pix"

ax.plot(x[pre], y[pre], color="#6366f1", linewidth=2.5, label="Crescimento (pré-Pix)", zorder=3)
ax.plot(x[pos], y[pos], color="#a78bfa", linewidth=2.5, linestyle="--", label="Estagnação (pós-Pix)", zorder=3)

ax.axvline(PIX_DATE, color="#16a34a", linewidth=1.5, linestyle="--")
ax.text(PIX_DATE, y.max() * 0.97, "  Pix\n  Nov/2020",
        color="#16a34a", fontsize=10, va="top")

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R$ {v:.1f} tri"))
ax.set_xlabel("Trimestre", fontsize=12)
ax.set_ylabel("Valor TED (R$ trilhões)", fontsize=12)
ax.set_title("TED: Crescimento e Estagnação (2015–2026)", fontsize=16, fontweight="bold", pad=16)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("charts/2_ted_crescimento.png", dpi=180, bbox_inches="tight")
plt.close()
print("✔ charts/2_ted_crescimento.png")

# ─────────────────────────────────────────────────────────────────────────────
# 3. TED vs DOC vs PIX (escala log)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))

x = pd.to_datetime(transf["datatrimestre"])
ax.semilogy(x, transf["valorTED"] / BILHAO, color="#6366f1", linewidth=2.5, label="TED")
ax.semilogy(x, transf["valorDOC"].replace(0, float("nan")) / BILHAO,
            color="#f59e0b", linewidth=2.5, label="DOC")
ax.semilogy(x, transf["valorPix"].replace(0, float("nan")) / BILHAO,
            color="#10b981", linewidth=2.5, label="Pix")

ax.axvline(PIX_DATE, color="#16a34a", linewidth=1.4, linestyle="--")
ax.axvline(DOC_DATE, color="#f59e0b", linewidth=1.4, linestyle="--")
ax.text(PIX_DATE, ax.get_ylim()[0] * 5, "  Pix\n  Nov/2020", color="#16a34a", fontsize=10)
ax.text(DOC_DATE, ax.get_ylim()[0] * 5, "  DOC\n  desc. 2024", color="#f59e0b", fontsize=10)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R$ {v:,.0f} bi"))
ax.set_xlabel("Trimestre", fontsize=12)
ax.set_ylabel("Valor (R$ bilhões, escala log)", fontsize=12)
ax.set_title("TED vs DOC vs Pix (2015–2026)", fontsize=16, fontweight="bold", pad=16)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("charts/3_ted_doc_pix.png", dpi=180, bbox_inches="tight")
plt.close()
print("✔ charts/3_ted_doc_pix.png")

# ─────────────────────────────────────────────────────────────────────────────
# 4. PIX vs CARTÃO DE DÉBITO (eixo duplo)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

x = pd.to_datetime(pix_deb["datatrimestre"])
pix_val = pix_deb["valorPix"] / TRILHAO
deb_val = pix_deb["valorCartaoDebito"] / BILHAO

pix_line, = ax1.plot(x, pix_val, color="#2563eb", linewidth=2.5, label="Pix (trilhões)")
deb_line, = ax2.plot(x, deb_val, color="#ef4444", linewidth=2.5, label="Cartão de Débito (bilhões)")

# Crossover
cross = pix_deb[pix_deb["valorPix"] >= pix_deb["valorCartaoDebito"]]["datatrimestre"].min()
if pd.notna(cross):
    ax1.axvline(pd.Timestamp(cross), color="gold", linewidth=1.5, linestyle="--")
    ax1.text(pd.Timestamp(cross), pix_val.max() * 0.95,
             "  Pix supera\n  Débito", color="#b45309", fontsize=10, va="top")

ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R$ {v:.1f} tri"))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R$ {v:.0f} bi"))
ax1.set_xlabel("Trimestre", fontsize=12)
ax1.set_ylabel("Pix (R$ trilhões)", color="#2563eb", fontsize=12)
ax2.set_ylabel("Cartão de Débito (R$ bilhões)", color="#ef4444", fontsize=12)
ax1.tick_params(axis="y", colors="#2563eb")
ax2.tick_params(axis="y", colors="#ef4444")

# Remover spines do eixo secundário
ax2.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)

lines = [pix_line, deb_line]
ax1.legend(lines, [l.get_label() for l in lines], fontsize=11, loc="upper left")
ax1.set_title("O momento em que o Pix superou o Cartão de Débito", fontsize=16, fontweight="bold", pad=16)

ax1.grid(True, color="#e8e8e8", linewidth=0.8)
ax2.grid(False)

plt.tight_layout()
plt.savefig("charts/4_pix_vs_debito.png", dpi=180, bbox_inches="tight")
plt.close()
print("✔ charts/4_pix_vs_debito.png")

print("\n✅ Todos os gráficos salvos em charts/")
