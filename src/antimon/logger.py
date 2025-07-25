# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Centralized logging system for antimon
"""

import logging
import sys
from enum import Enum

from .color_utils import Colors, apply_color, supports_color


class LogLevel(Enum):
    """Log levels for antimon"""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages"""

    def __init__(self, no_color: bool = False):
        super().__init__()
        self.no_color = no_color

        # Define color mapping for different log levels
        self.level_colors = {
            logging.DEBUG: Colors.WHITE,
            logging.INFO: Colors.CYAN,
            logging.WARNING: Colors.YELLOW,
            logging.ERROR: Colors.RED,
            logging.CRITICAL: Colors.MAGENTA,
        }

        # Define format strings for different message types
        self.formats = {
            "default": "%(message)s",
            "verbose": "[%(levelname)s] %(message)s",
            "debug": "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with appropriate colors"""
        # Get the base format
        if record.levelno == logging.DEBUG:
            fmt = self.formats["debug"]
        elif hasattr(record, "verbose") and record.verbose:
            fmt = self.formats["verbose"]
        else:
            fmt = self.formats["default"]

        # Create a formatter with the selected format
        formatter = logging.Formatter(fmt)
        formatted = formatter.format(record)

        # Apply color if not disabled
        if not self.no_color and supports_color():
            color = self.level_colors.get(record.levelno, Colors.RESET)
            formatted = apply_color(formatted, color, no_color=self.no_color)

        return formatted


class AntimonLogger:
    """Centralized logger for antimon"""

    def __init__(self, name: str = "antimon", no_color: bool = False):
        self.logger = logging.getLogger(name)
        self.no_color = no_color
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up logging handlers"""
        # Remove existing handlers
        self.logger.handlers.clear()

        # Create console handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(ColoredFormatter(no_color=self.no_color))

        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    def set_level(self, level: LogLevel):
        """Set the logging level"""
        self.logger.setLevel(level.value)

    def is_enabled_for(self, level: int) -> bool:
        """Check if logging is enabled for the given level"""
        return self.logger.isEnabledFor(level)

    def debug(self, message: str, **kwargs):
        """Log a debug message"""
        self.logger.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs):
        """Log an info message"""
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """Log a warning message"""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        """Log an error message"""
        self.logger.error(message, extra=kwargs)

    def critical(self, message: str, **kwargs):
        """Log a critical message"""
        self.logger.critical(message, extra=kwargs)

    def detection(self, detector: str, message: str, severity: str = "error"):
        """Log a detection event"""
        level = LogLevel.ERROR if severity == "error" else LogLevel.WARNING
        self.logger.log(
            level.value,
            f"Security issue detected: {message}",
            extra={"detector": detector, "detection": True},
        )

    def success(self, message: str):
        """Log a success message (shown as info with green color if available)"""
        # Create a custom record with success flag
        record = self.logger.makeRecord(
            self.logger.name, logging.INFO, "(unknown file)", 0, message, (), None
        )
        record.success = True
        self.logger.handle(record)
    
    def print(self, message: str = "", end: str = "\n", file=None):
        """Print-compatible method for backward compatibility.
        
        This method mimics the behavior of the built-in print() function
        to ensure seamless migration from print statements.
        
        Args:
            message: The message to print
            end: String appended after the message (default: newline)
            file: File object to write to (default: sys.stderr)
        """
        if file is None:
            file = sys.stderr
            
        # For stdout, use a different handler temporarily
        if file == sys.stdout:
            # Create a temporary stdout handler
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(ColoredFormatter(no_color=self.no_color))
            self.logger.addHandler(stdout_handler)
            
            # Log the message
            if end == "\n":
                self.logger.info(message)
            else:
                # For non-newline endings, we need to handle it specially
                self.logger.info(message + end.rstrip("\n"))
                
            # Remove the temporary handler
            self.logger.removeHandler(stdout_handler)
        else:
            # Default to stderr
            if end == "\n":
                self.logger.info(message)
            else:
                self.logger.info(message + end.rstrip("\n"))


# Global logger instance
_logger: AntimonLogger | None = None


def get_logger() -> AntimonLogger:
    """Get the global logger instance"""
    global _logger
    if _logger is None:
        _logger = AntimonLogger()
    return _logger


def setup_logger(
    verbose: bool = False, quiet: bool = False, no_color: bool = False
) -> AntimonLogger:
    """Set up the global logger with the specified configuration"""
    global _logger
    _logger = AntimonLogger(no_color=no_color)

    if quiet:
        _logger.set_level(LogLevel.ERROR)
    elif verbose:
        _logger.set_level(LogLevel.DEBUG)
    else:
        _logger.set_level(LogLevel.INFO)

    return _logger


# Convenience functions that mimic print() for easy migration
def log_print(message: str = "", end: str = "\n", file=None):
    """Print replacement that uses the logging system.
    
    This function can be used as a drop-in replacement for print()
    statements throughout the codebase.
    
    Args:
        message: The message to print
        end: String appended after the message (default: newline)
        file: File object to write to (default: sys.stderr)
    """
    logger = get_logger()
    logger.print(message, end=end, file=file)


def log_debug(message: str):
    """Log a debug message."""
    logger = get_logger()
    logger.debug(message)


def log_info(message: str):
    """Log an info message."""
    logger = get_logger()
    logger.info(message)


def log_warning(message: str):
    """Log a warning message."""
    logger = get_logger()
    logger.warning(message)


def log_error(message: str):
    """Log an error message."""
    logger = get_logger()
    logger.error(message)
