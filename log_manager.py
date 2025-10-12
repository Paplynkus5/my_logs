import logging
from pathlib import Path
import sys

def log_setup(LOG_FILE_NAME: str = 'app.log', loggerName: str = 'app'):

    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    if loggerName == 'app':
        formatter = logging.Formatter("(%(asctime)s.%(msecs)03d) %(levelname)s @ %(filename)s, line %(lineno)d: %(message)s", "%H:%M:%S")
    else:
        formatter = logging.Formatter("(%(asctime)s.%(msecs)03d) %(name)s: %(levelname)s @ %(filename)s, line %(lineno)d: %(message)s", "%H:%M:%S")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)  
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    if '/' in LOG_FILE_NAME:
        Path(LOG_FILE_NAME.rpartition('/')[0]).mkdir(parents=True, exist_ok=True)
    open(LOG_FILE_NAME, 'w')
    fileHandler = logging.FileHandler(LOG_FILE_NAME)
    fileHandler.setLevel(logging.WARNING)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger

def get_console_handler(object):
    for handler in object.handlers:
        if isinstance(handler, logging.StreamHandler):
            if handler.stream in (sys.stdout, sys.stderr):
                return handler
    return None

if __name__ == '__main__':
    logger = log_setup()

    try:
        DATA_FILE = open('user.dat', 'r+t')
        logger.info('Opened %s', DATA_FILE.name)
    except:
        logger.error('Failed to open specified file')

    print(get_console_handler(logger))