import sys


logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] "
                      "#%(levelname)-8s "
                      "%(filename)s:%(lineno)d - %(name)s:%(funcName)s - %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": sys.stdout
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "default",
            "stream": sys.stderr
        },
    },
    "loggers": {},
    "root": {
        "level": "DEBUG",
        "formatter": "default",
        "handlers": ["stdout", "stderr"]
    }
}