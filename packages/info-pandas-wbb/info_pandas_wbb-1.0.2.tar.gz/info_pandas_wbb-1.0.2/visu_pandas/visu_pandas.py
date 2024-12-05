import pandas as pd 

def info_tabela(tabela):
    print("Tamanho:", tabela.shape)

    print("Colunas:", tabela.columns)

    print("Tipagens:", tabela.dtypes)

    print(tabela.head())
