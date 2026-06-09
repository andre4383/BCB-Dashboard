from silver import silver_data_extract
import pandas as pd
import matplotlib.pyplot as plt

df = silver_data_extract()

def queda_saques():
    plt.plot(df['datatrimestre'],df['quantidadeSaques'])
    plt.grid(True)
    pand_date = pd.to_datetime('2020-03-01')# 2020-Q2
    pand_valor= 1033408.05 
    pix_date = pd.to_datetime('2020-11-01')
    pix_valor= 1082571.13 

    plt.axvline(x= pand_date,color='red',linestyle= '--', label='Inicio da Pandemia')
    plt.axvline(x= pix_date,color='green',linestyle= '--', label='lancamento do pix')
    plt.legend()
    plt.title("Queda de Saques no Brasil(2015-2025)")
    plt.ylabel("Quantidade em milhares")
    plt.xlabel("Trimestre")
    plt.show()


def volume_total_transacoes():
    valor_total = df.filter(like='valor').sum(axis=1)
    plt.grid(True)
    plt.plot(df['datatrimestre'],valor_total)
    plt.title('Evolução do volume total de transações')
    plt.ylabel("Evoluçao do volume de transaçoes(em milhares)")
    plt.xlabel("Trimestre")
    plt.show()

def ted_cres():        
    plt.plot(df['datatrimestre'], df['valorTED'])
    pix_date = pd.to_datetime('2020-11-01')
    plt.axvline(x= pix_date,color='red',linestyle= '--', label='lancamento do pix')
    plt.legend()
    plt.title('TED: crescimento e estagnação')
    plt.ylabel("valor da  Transferência Eletrônica Direta(milhoes)")
    plt.xlabel("Trimestre")
    plt.grid()
    plt.show()

queda_saques()
volume_total_transacoes()
ted_cres()