import pandas as pd


def ler_arquivo_alunos():
    try:
        df = pd.read_excel("Alunos.xlsm")
        print(df.head())
        return df
    except Exception as e:
        print(f"Erro em ler_arquivo_alunos em processar_excel.py: {e}")
