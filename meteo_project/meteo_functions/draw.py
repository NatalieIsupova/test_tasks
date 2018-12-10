import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os.path


class Graphic:

    @staticmethod
    def scatter(df, df_avg, config):
        plt.figure(figsize=(20, 10))
        x = df[config["WD_sig"]]
        y = df[config["WS_sig"]]
        a = df_avg[config["WD_sig"]]
        b = df_avg[config["WS_sig"]]
        # рисуем график по отфильтрованным данным
        fig1 = plt.scatter(x, y, marker=".", linewidths=0.5)
        # рисуем график по усредненным данным
        fig2 = plt.scatter(a, b, c="r", marker="^")
        plt.legend([fig1, fig2],
                   [config["WS_sig"], config["WS_sig"] + "_Avg"],
                   loc='upper left')
        plt.title("Wind Speed vs Wind Direction")
        plt.grid()
        plt.savefig(config["outpath"] + "scatter.png", format="png", dpi=300)  # todo убрать конкатинацию

    @staticmethod
    def plot(df, config):
        plt.figure(figsize=(20, 10))
        date = pd.to_datetime(df.index)
        plt.plot(date, df["AD_1"])
        plt.title("Air Density vs Daytime")
        plt.grid()
        plt.savefig(config["outpath"] + "plot.png", format="png", dpi=300)

    @staticmethod
    def hist(df, config):
        plt.figure(figsize=(20, 10))
        plt.hist(df[config["WS_sig"]], label=config["WS_sig"])
        plt.title("Wind Speed Histogram")
        plt.ylabel("Frequency")
        plt.legend(loc='upper right')
        # делаем шаг по оси Х в 1 м/с
        plt.xticks(np.arange(config["WS_min"], config["WS_max"] + 1, 1.0))
        plt.grid()
        plt.savefig(config["outpath"] + "hist.png", format="png", dpi=300)

    @staticmethod
    def windrose(df, config):
        """
        роза ветров - график зависимости частоты и направления ветров
        берем оригинальный датафрейм после первичной фильтрации (чтобы были все направления)
        чтобы он не был очень детализированным, сгруппируем по шагу из config
        для отрисовки нужны углы (angles), переведенные в радианы (rad), и частота таких ветров (count)
        """
        fig = plt.figure(figsize=(10, 10))
        # группируем по шагу из config
        bins = np.arange(start=0, stop=360, step=config["step"])
        labels = [item + config["step"] / 2 for item in bins]
        a = pd.cut(df["WD_1"], bins, right=False, labels=labels[0:-1])
        # считаем частоту ветров на каждом отрезке
        b = df.groupby(a).count()
        angles = list(b.index)
        count = list(b[config["WD_sig"]])
        # переводим градусы в радианы
        rad = [math.radians(i) for i in angles]
        ax = fig.add_subplot(111, projection='polar')
        ax.plot(rad, count, color="b", linewidth=2, label="Wind direction")
        # замыкаем розу ветров (соединяем конец с началом)
        ax.plot((rad[-1], rad[0]), (count[-1], count[0]), color="b", linewidth=2)
        plt.legend(loc='upper right')
        plt.title("Wind Rose")
        plt.savefig(config["outpath"] + "windrose.png", format="png", dpi=300)
