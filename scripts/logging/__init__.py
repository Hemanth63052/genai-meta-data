from scripts.config import LoggingConfig
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from logging import getLogger, Logger
import os

class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.logger = cls._initialize_logger()
        return cls._instance

    @staticmethod
    def _initialize_logger() -> Logger:
        logger_config_dict = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": LoggingConfig.LOG_FORMAT,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": StreamHandler,
                },
                "rotating_file": {
                    "class": RotatingFileHandler,
                    "filename": LoggingConfig.LOG_FILE,
                    "maxBytes": 10485760,
                    "backupCount": 20,
                    "encoding": "utf8",
                },
            }
        }
        logger = getLogger("genai-meta-data")
        for handler_name, handler_config in logger_config_dict["handlers"].items():
            if handler_name == "rotating_file":
                os.makedirs(os.path.dirname(handler_config["filename"]), exist_ok=True)
            handler_class = handler_config.pop("class")
            handler = handler_class(**handler_config)
            logger.addHandler(handler)
        logger.setLevel(LoggingConfig.LOG_LEVEL)
        return logger

def get_logger() -> Logger:
    return LoggerSingleton().logger

# Initialize the logger once
logger = get_logger()
