import logging
from logging.handlers import TimedRotatingFileHandler
import os
import pendulum

class GMT3Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Usa pendulum para ajustar para GMT-3
        dt = pendulum.from_timestamp(record.created, tz='UTC').in_tz('America/Sao_Paulo')
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.strftime("%Y-%m-%d %H:%M:%S")
        return s

def setup_logger(strategy='default', log_dir='../logs', log_level=logging.INFO):
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, f"{strategy}.log")

    logger = logging.getLogger(strategy)
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = TimedRotatingFileHandler(
            log_filename,
            when="midnight",
            interval=1,
            backupCount=14,
            encoding='utf-8'
        )
        formatter = GMT3Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        handler.suffix = "%Y-%m-%d"

        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger
