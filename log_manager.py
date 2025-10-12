import logging
from pathlib import Path
import sys
import inspect
import time

def log_setup(log_file: str = 'app.log', logger_name: str = 'app'):

    if '/' in log_file:
        log_file = log_file.replace('/', '\\')

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if logger_name == 'app':
        formatter = logging.Formatter("(%(asctime)s.%(msecs)03d) %(levelname)s @ %(filename)s, line %(lineno)d: %(message)s", "%H:%M:%S")
    else:
        formatter = logging.Formatter("(%(asctime)s.%(msecs)03d) %(name)s: %(levelname)s @ %(filename)s, line %(lineno)d: %(message)s", "%H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + log_file
    Path(log_file.rpartition('\\')[0]).mkdir(parents=True, exist_ok=True)
    open(log_file, 'w')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def get_console_handler(object):
    for handler in object.handlers:
        if isinstance(handler, logging.StreamHandler):
            if handler.stream in (sys.stdout, sys.stderr):
                return handler
    return None

def archive_logs(archive_file: str = '_'.join(map(str, time.localtime()[0:3])) + ' ' + ':'.join(map(str, time.localtime()[3:6]))):
    print(archive_file)
    pass

if __name__ == '__main__':
    archive_logs()
    test_logger = log_setup('test_logs\\app.log', 'root')
    test_logger.critical('Critical error test')