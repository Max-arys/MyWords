from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent
BASE_DIR = WORK_DIR.parent.parent
USERS_FILE = WORK_DIR.joinpath('data', 'users.json')
LOGS_FILE = WORK_DIR.joinpath('logs', 'log.log')
DATA_DIR = WORK_DIR.joinpath('data')

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(name)s-%(asctime)s-%(levelname)s-%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(name)s-%(levelname)s-%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "formatter": "default",
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_FILE,
            "backupCount": 2,
        },
        "verbose_output": {
            "formatter": "simple",
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "my_words": {
            "level": "DEBUG",
            "handlers": [
                "verbose_output",
                "logfile",
            ],
        },
        "users": {
            "level": "DEBUG",
            "handlers": [
                "verbose_output",
                "logfile",
            ],
        },
        "words": {
            "level": "DEBUG",
            "handlers": [
                "verbose_output",
                "logfile",
            ],
        },
    },
    # "root": {"level": "INFO", "handlers": ["logfile"]},
}
