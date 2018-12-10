import sys
from meteo_functions import meteostation

if __name__ == "__main__":
    path = sys.argv[1]
    meteostation.MeteoStation.calculate("config.json", path)
