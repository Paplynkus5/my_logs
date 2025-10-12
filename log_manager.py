import logging
import sys
import os
import inspect
import time
from pathlib import Path

def log_setup(log_file: str = 'app.log', log_file_mode: str = 'a', logger_name: str = 'app'):

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
    file_handler = logging.FileHandler(log_file, mode=log_file_mode)
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

def archive_logs(object, 
                 archive_file: str = 'archived_logs\\' + '-'.join(map(str, time.localtime()[0:3])) + ' ' + 
                 ''.join(f'{time_element:02s}' for time_element in map(str, time.localtime()[3:6])) + '.log',
                 source_file: str = ''):
    
    if '/' in archive_file:
        archive_file = archive_file.replace('/', '\\')
    if '/' in source_file:
        source_file = source_file.replace('/', '\\')
    
    archive_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + archive_file
    Path(archive_file.rpartition('\\')[0]).mkdir(parents=True, exist_ok=True)

    for handler in object.handlers:
        if isinstance(handler, logging.FileHandler):
            with open(archive_file, 'a') as archive_access:
                log_file = open(handler.baseFilename, 'r')
                archive_access.write(log_file.read())
                log_file = open(handler.baseFilename, 'w')
                return archive_file
    try:
        source_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + source_file
        if os.path.isfile(source_file) == True:
            log_file = open(source_file, 'r')
        else: 
            raise FileNotFoundError
        with open(archive_file, 'a') as archive_access:
            archive_access.write(log_file.read())
            log_file = open(source_file, 'w')
            return
    except FileNotFoundError:
        pass
    
    if source_file == '':
        raise FileNotFoundError('Could not find a FileHandler instance in specified logger, and no source_file was specified')
    else:
        raise FileNotFoundError('Could not find a FileHandler instance in specified logger nor the specified source_file')

#TO DO: merge archived logs, wipe archive

if __name__ == '__main__':
    test_logger = log_setup('test_logs\\app.log', 'w', logger_name='root')
    test_logger.critical('Critical error test')
    test_logger.warning('Test warning')
    for handler in test_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            test_logger.removeHandler(handler)
            handler.close()
    archive_logs(test_logger, source_file='test_logs/app.log')
