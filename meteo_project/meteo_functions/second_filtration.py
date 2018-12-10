import pandas as pd


class SecondFiltration:
    """
    фильтруем датафрейм по параметрам
    получаем на вход датафрейм, имя колонки, минимум и максимум
    на выход - отфильтрованный датафрейм
    """

    @staticmethod
    def filter(df, column_name, min, max):
        a = df[column_name] >= min
        b = df[column_name] <= max
        return df[a & b]
