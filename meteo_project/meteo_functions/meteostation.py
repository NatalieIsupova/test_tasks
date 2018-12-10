import pandas as pd
from meteo_functions import configwork
from meteo_functions import first_filtration
from meteo_functions import second_filtration
from meteo_functions import air_density
from meteo_functions import grouping
from meteo_functions import draw


class MeteoStation:
    """
    читаем файл config.json
    читаем data.csv
    проводим предварительную фильтрацию - убираем полностью пустые строки и строки-дубликаты
    проводим основную фильтрацию - вызываем класс фильтрации по параметрам скорости (1) и направления (2)
    записываем отфильтрованные данные в df_filt
    вычисляем air density и добавляем в отдельную колонку AD_1 датафрейма
    группируем по указанному столбцу и шагу из config, записываем файл df_avg
    рисуем графики (точечный, роза ветров, гистограмма, непрерывный), сохраняем в отдельные файлы
    """

    @staticmethod
    def calculate(conf_path, data_path):
        """
        :param conf_path: путь до config
        :param data_path: путь до data.csv
        """
        conf = configwork.ConfigWork.read(conf_path)
        df = pd.read_csv(data_path, sep=";", index_col="Timestamp")

        df = first_filtration.FirstFiltration.filter(df)
        df.to_csv(conf["outpath"] + "\\data_orig.csv")
        df_orig = df

        df = second_filtration.SecondFiltration.filter(df, conf['WS_sig'], conf["WS_min"], conf["WS_max"])
        df = second_filtration.SecondFiltration.filter(df, conf['WD_sig'], conf["WD_min"], conf["WD_max"])

        # записываем отфильтрованные данные
        df.to_csv(conf["outpath"] + "\\data_filt.csv")

        df["AD_1"] = air_density.AirDensity.calculate(df)

        # сгруппированный датафрейм с усредненными значениями
        df_avg = grouping.Group.make(df, conf["WD_sig"], conf["WD_min"], conf["WD_max"], conf["step"]).mean()

        # записываем усредненные данные
        df_avg.to_csv(conf["outpath"] + "\\data_avg.csv")

        draw.Graphic.scatter(df, df_avg, conf)
        draw.Graphic.windrose(df_orig, conf)
        draw.Graphic.hist(df, conf)
        draw.Graphic.plot(df, conf)
