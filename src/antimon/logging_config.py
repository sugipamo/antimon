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
        level = logging.WARNING  # Changed from INFO to WARNING for normal mode

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Important: Clear all existing handlers to prevent duplicates
    # This includes handlers set by logger.py
    root_logger.handlers.clear()
    
    # Also clear handlers from antimon logger specifically
    antimon_logger = logging.getLogger("antimon")
    antimon_logger.handlers.clear()
    antimon_logger.setLevel(level)
    
    # Don't add any handlers here - let logger.py handle formatting and output
    # This prevents duplicate messages in verbose mode


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
