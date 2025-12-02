import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class Logger:
    def __init__(self, file='my_logfile.log', level='debug', RotatingFile=True) -> None:
        """
        level:
            'debug', 'info', 'warning', 'error', 'critical'
        RotatingFile:
            RotatingFile or TimedRotatingFile
        RotatingFile:
            maxBytes: 5MB
            backupCount: 3
        TimedRotatingFile:
            interval: 1 day
            backupCount: 7 (one week)

        """
        # Create a logger
        self.logger = logging.getLogger('my_logger')
        match level:
            case 'debug':
                self.logger.setLevel(logging.DEBUG)
            case 'info':
                self.logger.setLevel(logging.INFO)
            case 'warning':
                self.logger.setLevel(logging.WARNING)
            case 'error':
                self.logger.setLevel(logging.ERROR)
            case 'critical':
                self.logger.setLevel(logging.CRITICAL)

        if RotatingFile:
            # Create a RotatingFileHandler to manage the log file with a maximum size and backup files
            file_handler = RotatingFileHandler(
                file,                    # Log file name
                maxBytes=5*1024*1024,    # Maximum size of the log file (5 MB here)
                backupCount=3            # Number of backup files (3 backup files)
            )
        else:
            # Create a TimedRotatingFileHandler to create a new log file every day
            file_handler = TimedRotatingFileHandler(
                file,                  # Log file name
                when='midnight',       # Rotate log at midnight
                interval=1,            # Rotate every 1 day
                backupCount=7          # Keep 7 backup files (one week of logs)
            )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Create a StreamHandler to also output logs to the terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, text):
        self.logger.debug(text)

    def info(self, text):
        self.logger.info(text)

    def warning(self, text):
        self.logger.warning(text)

    def error(self, text):
        self.logger.error(text)

    def critical(self, text):
        self.logger.critical(text)