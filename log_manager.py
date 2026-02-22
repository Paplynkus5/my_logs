import logging
import sys
import os
import inspect
import time
from pathlib import Path



def log_setup(log_file: str = 'logs\\app.log', log_file_mode: str = 'a', logger_name: str = 'app', skip_console_handler: bool = False):
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
    if skip_console_handler == True:
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
    raise LookupError #if no console handler found



def archive_logs(object, 
                 archive_file: str = 'archived_logs\\' + 
                     '-'.join(f'{time_element:02d}' for time_element in time.localtime()[0:3]) + ' ' 
                    + ''.join(f'{time_element:02d}' for time_element in time.localtime()[3:6]) + '.log',
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
                log_file = open(handler.baseFilename, 'w') #clear source_file after its contents are moved to archive_file. do not os.remove() as permission issues may arise ("file currently in use by a process")
                log_file.close()
                return archive_file
    try: #if user wants to archive a log file no longer bound to the logger's handlers, specified in source_file:
        source_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + source_file #find specified source_file in caller's parent directory
        if os.path.isfile(source_file) == True:
            log_file = open(source_file, 'r')
        else: 
            raise FileNotFoundError
        
        with open(archive_file, 'a') as archive_access:
            archive_access.write(log_file.read()) 
            log_file = open(source_file, 'w') #clear source_file after its contents are moved to archive_file. do not os.remove() as permission issues may arise ("file currently in use by a process")
            log_file.close()
            return
    except FileNotFoundError:
        pass
    
    if source_file == '':
        raise FileNotFoundError('Could not find a FileHandler instance in specified logger, and no source_file was specified')
    else:
        raise FileNotFoundError('Could not find a FileHandler instance in specified logger nor the specified source_file')



def wipe_archive(archive: str = 'archived_logs'):
    archive = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + archive #find specified archive in caller's parent directory
    for file in os.listdir(archive):
        if file.rpartition('.')[2] == 'log':
            os.remove(archive + '\\' + file)



def merge_archived_logs(archive: str = 'archived_logs', 
                        merged_archive_file: str = 'archived_logs\\merged\\' + 
                            '-'.join(f'{time_element:02d}' for time_element in time.localtime()[0:3]) + ' ' 
                            + ''.join(f'{time_element:02d}' for time_element in time.localtime()[3:6]) + '.log', 
                        super_merge: bool = False):
                        # ^ hence default merged_archive_file path is archived_logs\merged\YY-MM-DD HHmmSS based on time when function is called
                        # ^ if super_merge = true, logs in archived_logs\merged will also be joined into one file
    
    archive = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + archive #find specified archive in caller's parent directory
    merged_archive_file = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + merged_archive_file #append merged_archive_file path to caller's parent directory path
    Path(merged_archive_file.rpartition('\\')[0]).mkdir(parents=True, exist_ok=True) #create merged_archive_file's parent folders if missing
    
    if super_merge == True:
        for file in os.listdir(merged_archive_file.rpartition('\\')[0]):
            if file != merged_archive_file.rpartition('\\')[2]: #prevents execution if given file is the one we are merging to
                file_path = merged_archive_file.rpartition('\\')[0] + '\\' + file 
                #paste all merged log files' contents into merged_archive_file after a separator, and remove said files
                with open(merged_archive_file, 'a') as maf_access:
                    file_access = open(file_path, 'r')
                    maf_access.write(f'\n----- Merged as {file} -----\n')
                    maf_access.write(file_access.read())
                    file_access.close()
                    os.remove(file_path)

    #paste all archived log files' contents into merged_archive_file after a separator, and remove said files
    for file in os.listdir(archive):
        file_path = archive + '\\' + file
        if os.path.isfile(file_path):
            with open(merged_archive_file, 'a') as maf_access:
                file_access = open(file_path, 'r')
                maf_access.write(f'----- Archived as {file} -----\n')
                maf_access.write(file_access.read())
                file_access.close()
                os.remove(file_path)



def rotate_log_archive(object, count: int, archive: str = 'archived_logs', merge: bool = False, callout: bool = False):
    archive = inspect.stack()[1][1].rpartition('\\')[0] + '\\' + archive #find specified archive in caller's parent directory

    
    file_list = os.listdir(archive)
    while len(file_list) > count:
        if merge == True:
            pass
        else:
            os.remove(archive + '\\' + file_list[0])
    archive_logs(object)



if __name__ == '__main__':
    test_logger = log_setup('test_logs\\app.log', 'a', logger_name='root')
    test_logger.critical('Critical error test')
    test_logger.warning('Test warning')
    #wipe_archive()
    #for handler in test_logger.handlers:
    #    if isinstance(handler, logging.FileHandler):
    #        test_logger.removeHandler(handler)
    #        handler.close()
    archive_logs(test_logger, source_file='test_logs/app.log')
    rotate_log_archive(test_logger, 0)
    #merge_archived_logs(super_merge=True)