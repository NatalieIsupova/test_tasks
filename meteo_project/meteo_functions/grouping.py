import pandas as pd
import numpy as np


class Group:
    """
    группируем по колонке и шагу
    """

    @staticmethod
    def make(df, column_name, min, max, step):
        """
        :param df: изначальный датафрейм
        :param column_name: колонка WD_sig из config
        :param step: шаг из config
        :return: датафрейм с группированными значениями
        """
        bins = np.arange(start=min, stop=max + step, step=step)
        labels = [item + step / 2 for item in bins]
        df_groups = pd.cut(df[column_name], bins, right=False, labels=labels[0:-1])
        return df.groupby(df_groups)
