# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
antimon - Security validation tool for AI coding assistants

A Python package that detects potentially dangerous operations and
prohibited patterns in code modifications.
"""

__version__ = "0.2.8"

from .core import validate_hook_data, check_file_directly, check_content_directly
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
from .runtime_config import RuntimeConfig, get_runtime_config, set_runtime_config
from .error_context import ErrorContext
from .first_run import is_first_run, mark_first_run_complete
from .last_error import save_last_error, load_last_error, explain_last_error

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
    "check_file_directly",
    "check_content_directly",
    "RuntimeConfig",
    "get_runtime_config",
    "set_runtime_config",
    "ErrorContext",
    "is_first_run",
    "mark_first_run_complete",
    "save_last_error",
    "load_last_error",
    "explain_last_error",
]
