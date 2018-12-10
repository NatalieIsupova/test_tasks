import json


class ConfigWork:

    @staticmethod
    def read(path_config):
        with open(path_config, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def write(path_config):
        with open(path_config, "w", encoding="utf-8") as file:
            json.dump(path_config, file)
