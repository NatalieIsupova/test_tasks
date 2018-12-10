import pandas as pd


class FirstFiltration:
    """
    класс фильтрует датафрейм:
    отбрасывает строки, в которых отсутствуют все данные
    удаляет дубликаты строк

    на вход - изначальный датафрейм
    на выход - отфильтрованный датафрейм
    """

    @staticmethod
    def filter(df):
        df = df.dropna(axis=0, how='all')
        df = df.drop_duplicates()
        return df
