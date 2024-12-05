import pandas as pd 

def info_tabela(tabela):
    texto = tabela.shape, tabela.columns, tabela.dtypes, tabela.head()

    return texto
