'''
Logger Module

This module provides functions for logging messages to a file.
'''

# Modules
from modules.file_paths import OUTPUT_PATH, DEBUG_PATH

def debug(message, severity = "INFO"):
    """
    Logs messages with optional severity levels, default file path is 'logs\\debug.txt'

    Args:
        message (str): The message to be logged.
        severity (str, optional): The severity level of the log message. Defaults to "INFO".

    Returns:
        timestamp: current system time from datetime
    """

    # Local import for system time information
    from datetime import datetime as dt

    # Get the current timestamp
    timestamp = dt.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # Create the log entry
    debug_entry = f"{timestamp} [{severity}] {message}"

    # Write the log entry to the log file
    with open(DEBUG_PATH, 'a') as debug_file:
        debug_file.write(debug_entry + '\n')

    return timestamp

def clear_logs():
    """
    Helper function: Clears all logs from 'logs\\output.txt' and 'logs\\debug.txt'
    """

    try:
        # Open the files in write mode to clear the content
        with open(OUTPUT_PATH, "w") as _, open(DEBUG_PATH, "w") as _:
            pass  # The files are opened and immediately closed, which clears their content
    except Exception as error:
        print(f"Error clearing logs: {error}")

def log_entry(entry, boolean, timestamp):
    """
    Helper function: Logs user entry information to 'logs\\output.txt' with a timestamp

    Args:
        entry (dict): User input data as a dictionary.
        boolean (Bool): A value for True, False, or None.
        timestamp (string): The current formatted system time.
    """

    # Check if match was found - 'T' for True, 'F' for False, else, no match info needed
    if boolean == True:
        log(f"{timestamp} | Match Found: 'T' | User entry info: {entry}")
    elif boolean == False:
        log(f"{timestamp} | Match Found: 'F' | User entry info: {entry}")
    else:
        log(f"{timestamp} | User entry info: {entry}")

def log(*args, file_path = OUTPUT_PATH, sep = ' ', end = '\n'):
    """
    Logs messages to a file, similar to the built-in print function.

    Args:
        *args: Variable number of positional arguments representing the log messages.
        file_path (str, optional): The path of the log file. Defaults to 'logs\\output.txt'.
        sep (str, optional): The separator between arguments. Defaults to ' '.
        end (str, optional): The character to append at the end of each line. Defaults to '\n'.
    """

    try:
        # Convert all arguments to strings
        formatted_args = [str(arg) for arg in args]
        # Join the formatted arguments with the specified separator
        formatted_message = sep.join(formatted_args)
        # Open log file in append mode
        with open(file_path, 'a') as file:
            # Print the formatted message to the file
            print(formatted_message, end = end, file = file)
    except FileNotFoundError as error:
        # If file is not found, log an error using the debug function
        debug(f"File not found! Is 'output.txt' in the correct directory? Code: {error}", "ERROR")
    except IOError as error:
        # If there's an IO error, log an error using the debug function
        debug(f"Bad file read/write. Code: {error}", "ERROR")