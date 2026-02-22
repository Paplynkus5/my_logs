Basic reusable Python logging utility I've made to avoid repeating myself in my projects. 

Built using the `logging` module available in pip.


# Available functions


1) **log_setup**: Sets up a basic logger and its console and file handlers. 

	**Takes following variables:** 

	1) **log_file** (string) - relative path and filename to use for the logging file. *Default: '\logs\app.log'*
	2) **log_file_mode** (string) - mode to use when opening the log file. Use `log_file_mode` = 'w' to clear leftover `log_file` contents with the start of each run, 'a' to append to current contents. *Default: 'a' (append)*
	3) **logger_name** (string) - name for the logger object. *Default: 'app'*
	4) **skip_console_handler** (bool) - set as `True` to skip creating the console handler. Useful for scripts that use the console for UI. *Default: `False`*

	Log messages format (as per the example): `(12:34:56.789) WARNING @ file.py, line 2137: Hello World!`; or if a custom logger name is set: `(12:34:56.789) root: WARNING @ file.py, line 2137: Hello World!`

2) **get_console_handler**: Cycles through a logger's handlers and checks if it is a console handler. If true, returns that handler immediately, since only 1 console handler will be used realistically.

	**Takes following variables:** 

	 1) **object** - logger object to analyze.

3) **archive_logs**: Move a given logger's log file to an archive (and create an archive folder if missing). 

	**Takes following variables:** 

	1) **object** - logger object to take its log file path.
	2) **archive_file** (string) - name and path of the archive file that is to be created. *Default: \archived_logs\YY-MM-DD HHmmSS.log (based on time when function is called)*
	3) **source_file** (string) - only to be used to archive a log file that is no longer bound to an accessible logger object. 

4) **wipe_archive**: Wipes a log archive directory.

	**Takes following variables:** 

	1) **archive** - relative path to archive folder. *Default: 'archived_logs'*

5) **merge_archived_logs**: Merges multiple files in a log archive directory into one, preserving all contents.

	**Takes following variables:** 

	1) **archive** - relative path to archive folder. *Default: 'archived_logs'*
	2) **merged_archive_file** (string) - relative path to a new file that should contain all archived logs' contents. *Default: 'archived_logs\merged\YY-MM-DD HHmmSS'*
	3) **super_merge** (bool) - if `True`, logs in archived_logs\merged will also be joined into one file. *Default: `False`*

## Work in progress

1) **rotate_log_archive** - function that archives all log files except a given number of newest ones.
