import os
import yaml
import logging
import logging.config


class AppLogger():
    def __init__(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, 'log.yaml')

        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)

    def get_logger(self, name=None):
        return logging.getLogger(name)


def get_default_logger():
    return AppLogger().get_logger()
