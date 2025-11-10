# utils/logger.py
import logging
import logging.handlers
import sys

def setup_logger():
    logger = logging.getLogger("metrics_collector")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        "logs/collector.log",
        maxBytes=5_000_000,
        backupCount=3
    )
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

