from silver import silver_data_extract
from sqlalchemy import create_engine
import pandas as pd

def gold_transform():
    df = silver_data_extract()

    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    
    #queda de saques
    gold_saques = df[['datatrimestre', 'quantidadeSaques']].copy()
    gold_saques['variacao_porc'] = df['quantidadeSaques'].pct_change() * 100
    gold_saques['variacao_porc'] = gold_saques['variacao_porc'].fillna(0)
    gold_saques['variacao_porc'] = gold_saques['variacao_porc'].round(2)
    gold_saques.to_sql('gold_saques', engine, if_exists='replace', index=False)
    
    #ted
    gold_ted_cres = df[['datatrimestre' , 'valorTED']].copy()
    gold_ted_cres['periodo'] = gold_ted_cres['datatrimestre'].apply(
        lambda x:'pos_pix' if x >= pd.to_datetime('2020-11-01') else 'pre_pix'
    )
    gold_ted_cres.to_sql('gold_ted_cres', engine, if_exists='replace', index=False)

    # transferencias (TED vs DOC vs Pix)
    gold_transf = df[['datatrimestre', 'valorTED', 'valorDOC', 'valorPix']].copy()
    gold_transf.to_sql('gold_transferencias', engine, if_exists='replace', index=False)

    # pix vs cartao debito
    gold_pix_deb = df[['datatrimestre', 'valorPix', 'valorCartaoDebito']].copy()
    gold_pix_deb.to_sql('gold_pix_vs_debito', engine, if_exists='replace', index=False)

    # market share (primeiro e ultimo trimestre) - exclui valorSaques (nao eh meio de pagamento)
    trimestres_alvo = [df['datatrimestre'].min(), df['datatrimestre'].max()]
    df_ms = df[df['datatrimestre'].isin(trimestres_alvo)].copy()
    valor_cols = [c for c in df_ms.columns if c.startswith('valor') and c != 'valorSaques']
    rows = []
    for _, row in df_ms.iterrows():
        total = sum(row[c] for c in valor_cols)
        for c in valor_cols:
            rows.append({
                'datatrimestre': row['datatrimestre'],
                'meio': c.replace('valor', ''),
                'valor': row[c],
                'percentual': round(row[c] / total * 100, 2) if total else 0
            })
    gold_ms = pd.DataFrame(rows)
    gold_ms.to_sql('gold_market_share', engine, if_exists='replace', index=False)


if __name__ == '__main__':
    gold_transform()
