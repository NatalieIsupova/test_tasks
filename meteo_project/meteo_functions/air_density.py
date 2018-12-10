from math import exp
from meteo_functions import constants


class AirDensity:
    """
    на вход датафрейм
    считаем АД по формуле для каждой строчки
    выход - список значений
    """

    @staticmethod
    def calculate(df):
        r0 = constants.r0
        p0 = constants.p0
        rw = constants.rw
        k0 = constants.k0
        pw = [0.0000205 * exp(0.0631846 * (item + k0)) for item in df["TEMP_1"]]
        return ((1 / (df["TEMP_1"] + k0)) * \
                (((df["BP_1"] * p0) / r0) - ((df["RH_1"] * pw) / p0) * (1 / r0 - 1 / rw)))
