from bronze import data_extract
import pandas as pd
from sqlalchemy import create_engine

def silver_data_extract():
    df = data_extract()

    df['datatrimestre'] = pd.to_datetime(df['datatrimestre'])
    df = df.sort_values('datatrimestre')
    df = df.reset_index(drop=True)
    valor_cols = list(df.filter(like='valor').columns)
    df[valor_cols] = df[valor_cols] * 1000000  # R$ milhoes -> R$ absoluto
    quantidade_cols = list(df.filter(like='quantidade').columns)
    df[quantidade_cols] = df[quantidade_cols] * 1000  # milhares -> unidades
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    df.to_sql('silver_meios_pagamento', engine, if_exists='replace', index=False)
    return df

if __name__ == '__main__':
    silver_data_extract()
