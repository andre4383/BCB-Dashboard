from silver import silver_data_extract
from sqlalchemy import create_engine
import pandas as pd

def gold_transform():
    df = silver_data_extract()
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    
    # volume
    gold_volume = df[['datatrimestre']].copy()
    gold_volume['volume_total'] = df.filter(like='valor').sum(axis=1)
    gold_volume.to_sql('gold_volume_total', engine, if_exists='replace', index=False)
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
    
    
gold_transform()    
    