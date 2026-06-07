import pandas as pd
import requests

def data_extract():
    url = "https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosTrimestralDA(trimestre=@trimestre)?@trimestre='20151'&$top=100&$format=json"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['value'])
    return df
    