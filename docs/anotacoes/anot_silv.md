# SILVER DOCUMENT

1. Ajeitar `datatrimestre` passar de `str` para `datetime`
2. `valorTEC` esta zerado, TEC foi descontinuada, valores representam uma ausencia real de transacoes
3. `valorPix` esta zerado, pois o pix foi *criado no final de 2020*, logo nao sera necessario mexer nos valores, apenas deve ficar documentado
4. `quantidadePix` = `825368.19` esse valor esta em `float` porem foi documentado que ele esta em *milhares*
5. Valores precisam vir em ordem crescente de acordo com `datatrimestre` para comecar de 2015.1
6. Indice foi resetado

## ANALISES:
1. "Por que saques caíram 50% em 10 anos?" — isso conta história real do Brasil: Pix, pagamento por aproximação, menos dinheiro físico.
- 1. Por que a quantidade de Saques desceram mais de 50% nos ultimos 10 anos?
- 2. Quantidade de Saques no eixo y e datatrimestre no eixo x
- 3. Grafico de Linhas
- 4. Criar 5 partes do grafico significando cada parte desse periodo de 10 anos
2. 

## TUAS 3 ANÁLISES FINAIS
1. Queda de saques em 10 anos |Linha

2. Evolução do volume total de transações |Linha
>
3. Crescimento do TED |Linha
> TED cresceu 321% na década, mas a partir de 2021 estagnou com oscilações — possível efeito da concorrência do Pix.
<!-- 
Para estruturar esses dados no seu dashboard, temos exatamente 45 trimestres (de março de 2015 a março de 2026). Como você quer dividir isso em 5 períodos, existem duas abordagens principais na engenharia de dados para resolver isso: a **Visão de Negócio** (anos agrupados) ou a **Visão Matemática** (distribuição perfeitamente igualitária).

Aqui estão as duas formas de fazer essa quebra, junto com o código Pandas para aplicar no seu pipeline.

---

### Abordagem 1: Visão de Negócios (Agrupamento por Anos)

Essa é a melhor opção se o objetivo for exibir os dados em gráficos no dashboard. O usuário final entende melhor "anos fechados" do que quebras no meio do ano. Como temos 11 anos completos e 1 trimestre de 2026, podemos agrupar em blocos de 2 a 3 anos.

**A Divisão:**

* **P1 (2015 - 2016):** 8 trimestres
* **P2 (2017 - 2018):** 8 trimestres
* **P3 (2019 - 2020):** 8 trimestres
* **P4 (2021 - 2022):** 8 trimestres
* **P5 (2023 - 2026):** 13 trimestres *(Agrupa o cenário macroeconômico mais recente e o dado isolado de 2026)*

**Como aplicar no Pandas:**

```python
# Garante que a coluna de data é do tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Função para mapear os anos para os períodos
def classificar_periodo(data):
    ano = data.year
    if ano <= 2016: 
        return '2015-2016'
    elif ano <= 2018: 
        return '2017-2018'
    elif ano <= 2020: 
        return '2019-2020'
    elif ano <= 2022: 
        return '2021-2022'
    else: 
        return '2023-2026'

# Cria a nova coluna no DataFrame
df['Periodo_Dashboard'] = df['Data'].apply(classificar_periodo)

```

---

### Abordagem 2: Visão Matemática (Baldes Iguais)

Se você for fazer cálculos de média, soma total ou comparações de volume entre os períodos, o ideal é que todos tenham o **mesmo peso**. Como temos 45 linhas exatas, podemos dividir em 5 blocos de exatamente 9 trimestres cada (2 anos e 1 trimestre por período).

**A Divisão (9 trimestres em cada):**

* **P1:** Mar/2015 até Mar/2017
* **P2:** Jun/2017 até Jun/2019
* **P3:** Set/2019 até Set/2021
* **P4:** Dez/2021 até Dez/2023
* **P5:** Mar/2024 até Mar/2026

**Como aplicar no Pandas:**
Como os dados da API do Banco Central já vêm ordenados cronologicamente, você pode simplesmente multiplicar uma lista de rótulos. Isso é muito eficiente computacionalmente:

```python
import numpy as np

# Cria uma repetição exata: 9 vezes o P1, 9 vezes o P2, etc. (Total = 45)
# Requisito: O DataFrame precisa estar ordenado da data mais antiga para a mais nova
df['Periodo_Matematico'] = np.repeat(['P1', 'P2', 'P3', 'P4', 'P5'], 9)

```

**Qual escolher?**
Se o foco for a interface visual para o usuário ler, vá na **Abordagem 1**. Se o foco for criar agregações (`groupby`) estatisticamente precisas onde um período não pode ter mais dados que o outro, use a **Abordagem 2**. -->