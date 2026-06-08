from bronze import data_extract
import pandas as pd


def silver_data_extract():
    df = data_extract()

    df['datatrimestre'] = pd.to_datetime(df['datatrimestre'])
    df = df.sort_values('datatrimestre')
    df = df.reset_index(drop=True)
    return df

