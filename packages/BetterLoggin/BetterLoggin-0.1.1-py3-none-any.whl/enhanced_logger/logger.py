import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler, SMTPHandler, TimedRotatingFileHandler
from colorama import Fore, Style, init
import json
import socket

# Initialize Colorama for colored console outputs
init(autoreset=True)

class CustomFormatter(logging.Formatter):
    """Custom Formatter to add colors and enhance log format."""
    FORMATS = {
        logging.DEBUG: Fore.CYAN + "[DEBUG]" + Style.RESET_ALL + " %(asctime)s - %(message)s",
        logging.INFO: Fore.GREEN + "[INFO]" + Style.RESET_ALL + " %(asctime)s - %(message)s",
        logging.WARNING: Fore.YELLOW + "[WARNING]" + Style.RESET_ALL + " %(asctime)s - %(message)s",
        logging.ERROR: Fore.RED + "[ERROR]" + Style.RESET_ALL + " %(asctime)s - %(message)s",
        logging.CRITICAL: Fore.MAGENTA + "[CRITICAL]" + Style.RESET_ALL + " %(asctime)s - %(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


class JsonFormatter(logging.Formatter):
    """Custom JSON Formatter for structured logging."""
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created)),
            "name": record.name,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "process": record.process,
            "threadName": record.threadName,
            "hostname": socket.gethostname()
        }
        return json.dumps(log_record)


def get_logger(name: str, log_file: str = "app.log", level: int = logging.DEBUG, use_json: bool = False) -> logging.Logger:
    """
    Creates a customized logger that logs to both console and a file, with colored outputs and optional JSON formatting.
    
    Parameters:
    - name: str: The name of the logger.
    - log_file: str: The file to write logs to.
    - level: int: The minimum log level.
    - use_json: bool: If True, logs will be written in JSON format.
    
    Returns:
    - Logger: A customized logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        # Create a rotating file handler
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
        file_handler.setLevel(level)
        if use_json:
            file_formatter = JsonFormatter()
        else:
            file_formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Create a timed rotating file handler for daily logs
        timed_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
        timed_handler.setLevel(level)
        timed_handler.setFormatter(file_formatter)
        logger.addHandler(timed_handler)

        # Create a console handler with color support
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)
        
        # Optional: Add SMTP handler for critical errors
        smtp_handler = SMTPHandler(
            mailhost=("smtp.example.com", 587),
            fromaddr="error-logger@example.com",
            toaddrs=["admin@example.com"],
            subject="Critical Error Logged",
            credentials=("user", "password"),
            secure=()
        )
        smtp_handler.setLevel(logging.CRITICAL)
        smtp_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s"))
        logger.addHandler(smtp_handler)
        
        # Optional: Add error file handler for error logs only
        error_file_handler = RotatingFileHandler("errors.log", maxBytes=2 * 1024 * 1024, backupCount=3)
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(file_formatter)
        logger.addHandler(error_file_handler)

    return logger

# Example usage
if __name__ == "__main__":
    # Get the enhanced logger
    logger = get_logger("AdvancedEnhancedLogger", use_json=True)
    
    # Sample log messages
    logger.debug("This is a debug message, useful for tracing.")
    logger.info("This is an info message, providing general information.")
    logger.warning("This is a warning, something might be wrong.")
    logger.error("This is an error, something is definitely wrong!")
    logger.critical("This is a critical issue, immediate attention needed!")
