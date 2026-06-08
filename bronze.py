import pandas as pd
import requests
from sqlalchemy import create_engine


def data_extract():
    url = "https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosTrimestralDA(trimestre=@trimestre)?@trimestre='20151'&$top=100&$format=json"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['value'])
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bcb_dashboard")
    df.to_sql('bronze_meios_pagamento', engine, if_exists='replace', index=False)
    return df
