# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
antimon - Security validation tool for AI coding assistants

A Python package that detects potentially dangerous operations and
prohibited patterns in code modifications.
"""

__version__ = "0.2.4"

from .core import validate_hook_data
from .detectors import (
    DetectionResult,
    detect_api_key,
    detect_bash_dangerous_commands,
    detect_claude_antipatterns,
    detect_docker,
    detect_filenames,
    detect_llm_api,
    detect_localhost,
    detect_read_sensitive_files,
)

__all__ = [
    "DetectionResult",
    "__version__",
    "detect_api_key",
    "detect_bash_dangerous_commands",
    "detect_claude_antipatterns",
    "detect_docker",
    "detect_filenames",
    "detect_llm_api",
    "detect_localhost",
    "detect_read_sensitive_files",
    "validate_hook_data",
]
