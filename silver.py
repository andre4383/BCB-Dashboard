from bronze import data_extract
import pandas as pd

df = data_extract()

df['datatrimestre'] = pd.to_datetime(df['datatrimestre'])
df = df.sort_values('datatrimestre')
df = df.reset_index(drop=True)
print(df.head())
print(df.dtypes)

