from bronze import data_extract
import pandas as pd
from sqlalchemy import create_engine

def silver_data_extract():
    df = data_extract()

    df['datatrimestre'] = pd.to_datetime(df['datatrimestre'])
    df = df.sort_values('datatrimestre')
    df = df.reset_index(drop=True)
    df['quantidadeSaques'] = df['quantidadeSaques'] * 1000000
    valor_cols = [c for c in df.columns if c.startswith('valor')]
    df[valor_cols] = df[valor_cols] * 1000000
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    df.to_sql('silver_meios_pagamento', engine, if_exists='replace', index=False)
    return df
silver_data_extract()
