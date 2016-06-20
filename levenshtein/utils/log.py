import os
import json
import logging
import traceback
import pkg_resources

from logging.config import dictConfig

DEFAULT_LOG_PATH = pkg_resources.resource_filename('levenshtein.utils', 'log.json')

def setup_logging(
    default_path=DEFAULT_LOG_PATH,
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    try:
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    except IOError:
        logging.basicConfig(level=default_level)
        WARNING_FORMAT = ("Failed to read from logging config file, '{0}'. " +
                          "Using basicConfig with level '{1}' instead.")
        warn_msg = WARNING_FORMAT.format(path, default_level)
        raise IOError(warn_msg)
    except ValueError:
        WARNING_FORMAT = ("JSON logfile '{0}' is incorrectly formatted.")
        warn_msg = WARNING_FORMAT.format(LOGFILE_NAME)
        raise ValueError(warn_msg + traceback.format_exc())



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerManager(object):
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        setup_logging()

    @staticmethod
    def get_logger(name=None):
        if not name:
            logging.basicConfig()
            return logging.getLogger()
        elif name not in LoggerManager._loggers.keys():
            logging.basicConfig()
            LoggerManager._loggers[name] = logging.getLogger(str(name))
        return LoggerManager._loggers[name]
