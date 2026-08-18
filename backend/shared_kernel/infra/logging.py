"""Define logging configuration for the application."""
import logging
import logging.config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # Adjust the index based on your project structure
LOG_DIR = BASE_DIR / "logs"

LOGGING_LEVEL = logging.DEBUG if __debug__ else logging.INFO

def configure_logging():
    """Configure logging for the application."""
    LOG_DIR.mkdir(exist_ok=True)  # Create logs directory if it doesn't exist

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": LOGGING_LEVEL,
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": str(LOG_DIR / "backend.log"),
                "when": "midnight",
                "formatter": "standard",
                "level": logging.INFO,
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": LOGGING_LEVEL,
                "propagate": True,
            },
        },
    }

    logging.config.dictConfig(logging_config)
