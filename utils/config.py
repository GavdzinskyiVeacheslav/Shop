import configparser

from utils import log

config = None


def get_config():

    global config

    if config is None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        if not config.sections():
            log.write('Ошибка чтения конфигурации', 'info')
    return config
