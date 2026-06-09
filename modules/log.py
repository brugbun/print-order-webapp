import logging

LOG_PATH = "./logs"

def infolog(filename, message):
    logger = logging.basicConfig(filename=f"{LOG_PATH}/{filename}", level=logging.INFO)
    logger.info(message)

def warnlog(filename, message):
    logger = logging.basicConfig(filename=f"{LOG_PATH}/{filename}", level=logging.WARNING)
    logger.warn(message)

def errorlog(filename, message):
    logger = logging.basicConfig(filename=f"{LOG_PATH}/{filename}", level=logging.ERROR)
    logger.error(message)
