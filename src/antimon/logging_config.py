# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Logging configuration for antimon
"""

import logging
import sys


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """
    Configure logging for the application

    Args:
        verbose: Enable verbose (DEBUG) logging
        quiet: Suppress all but ERROR level logging
    """
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    # Create formatter with simplified timestamp for better readability
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)

    # Set levels for specific loggers
    logging.getLogger("antimon").setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
