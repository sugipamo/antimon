# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
antimon - Security validation tool for AI coding assistants

A Python package that detects potentially dangerous operations and
prohibited patterns in code modifications.
"""

__version__ = "0.2.12"

from .core import check_content_directly, check_file_directly, validate_hook_data
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
from .error_context import ErrorContext
from .first_run import is_first_run, mark_first_run_complete
from .last_error import explain_last_error, load_last_error, save_last_error
from .runtime_config import RuntimeConfig, get_runtime_config, set_runtime_config

__all__ = [
    "DetectionResult",
    "ErrorContext",
    "RuntimeConfig",
    "__version__",
    "check_content_directly",
    "check_file_directly",
    "detect_api_key",
    "detect_bash_dangerous_commands",
    "detect_claude_antipatterns",
    "detect_docker",
    "detect_filenames",
    "detect_llm_api",
    "detect_localhost",
    "detect_read_sensitive_files",
    "explain_last_error",
    "get_runtime_config",
    "is_first_run",
    "load_last_error",
    "mark_first_run_complete",
    "save_last_error",
    "set_runtime_config",
    "validate_hook_data",
]
