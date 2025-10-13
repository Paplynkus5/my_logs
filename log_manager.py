import logging
import sys
import os
import inspect
import time
from pathlib import Path

def log_setup(log_file: str = 'app.log', log_file_mode: str = 'a', logger_name: str = 'app'):
    # ^ use log_file_mode = 'w' to clear leftover log_file contents with the start of each run, 'a' to append to current contents

    #format log_file input in same style as value returned by inspect.stack()[1][1]
    if '/' in log_file:
        log_file = log_file.replace('/', '\\')

    #set up a basic logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if logger_name == 'app': #only include logger name in log messages if it is different from default
        formatter = logging.Formatter("(%(asctime)s.%(msecs)03d) %(levelname)s @ %(filename)s, line %(lineno)d: %(message)s", "%H:%M:%S")
        #example log message: (12:34:56.789) WARNING @ file.py, line 2137: Hello World!
    else:
        formatter = logging.Formatter("(%(asctime)s.%(msecs)03d) %(name)s: %(levelname)s @ %(filename)s, line %(lineno)d: %(message)s", "%H:%M:%S")
        #example log message: (12:34:56.789) root: WARNING @ file.py, line 2137: Hello World!

    #set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    #set up file handler
    log_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + log_file #append log_file path to caller's parent directory path
    Path(log_file.rpartition('\\')[0]).mkdir(parents=True, exist_ok=True) #if log_file is set to be in a nested directory, create its parent folders if missing
    file_handler = logging.FileHandler(log_file, mode=log_file_mode)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    #return fully set up logger object
    return logger

def get_console_handler(object):
    #cycle through handlers, check if it is a console handler. return since only 1 console handler will be used realistically
    for handler in object.handlers:
        if isinstance(handler, logging.StreamHandler):
            if handler.stream in (sys.stdout, sys.stderr):
                return handler
    return None

def archive_logs(object, 
                 archive_file: str = 'archived_logs\\' + '-'.join(map(str, time.localtime()[0:3])) + ' ' + 
                 ''.join(f'{time_element:02s}' for time_element in map(str, time.localtime()[3:6])) + '.log',
                 source_file: str = ''):
    # ^ hence default archive_file path is archived_logs\YY-MM-DD HHmmSS based on time when function is called
    #format input in same style as value returned by inspect.stack()[1][1]
    if '/' in archive_file:
        archive_file = archive_file.replace('/', '\\')
    if '/' in source_file:
        source_file = source_file.replace('/', '\\')
    
    archive_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + archive_file #append archive_file path to caller's parent directory path
    Path(archive_file.rpartition('\\')[0]).mkdir(parents=True, exist_ok=True) #create archive_file's parent folders if missing

    #look for FileHandler instances, paste their output file contents into archive_file
    for handler in object.handlers:
        if isinstance(handler, logging.FileHandler):
            with open(archive_file, 'a') as archive_access:
                log_file = open(handler.baseFilename, 'r')
                archive_access.write(log_file.read())
                log_file = open(handler.baseFilename, 'w')
                return archive_file
    try: #if user wants to archive a log file no longer bound to the logger's handlers, specified in source_file:
        source_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + source_file #find specified source_file starting in caller's parent directory
        if os.path.isfile(source_file) == True:
            log_file = open(source_file, 'r')
        else: 
            raise FileNotFoundError
        with open(archive_file, 'a') as archive_access:
            archive_access.write(log_file.read()) 
            log_file = open(source_file, 'w') #clear source_file after its contents are moved to archive_file. do not os.remove() as permission issues may arise ("file currently in use by a process")
            return
    except FileNotFoundError:
        pass
    
    if source_file == '':
        raise FileNotFoundError('Could not find a FileHandler instance in specified logger, and no source_file was specified')
    else:
        raise FileNotFoundError('Could not find a FileHandler instance in specified logger nor the specified source_file')

#TO DO: comment code, merge archived logs, wipe archive

if __name__ == '__main__':
    test_logger = log_setup('test_logs\\app.log', 'w', logger_name='root')
    test_logger.critical('Critical error test')
    test_logger.warning('Test warning')
    for handler in test_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            test_logger.removeHandler(handler)
            handler.close()
    archive_logs(test_logger, source_file='test_logs/app.log')
