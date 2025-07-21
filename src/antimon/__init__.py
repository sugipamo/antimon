"""
antimon - Security validation tool for AI coding assistants

A Python package that detects potentially dangerous operations and
prohibited patterns in code modifications.
"""

__version__ = "0.2.0"

from .detectors import (
    detect_filenames,
    detect_llm_api,
    detect_api_key,
    detect_docker,
    detect_localhost,
    detect_claude_antipatterns,
    DetectionResult,
)

from .core import validate_hook_data

__all__ = [
    "detect_filenames",
    "detect_llm_api",
    "detect_api_key",
    "detect_docker",
    "detect_localhost",
    "detect_claude_antipatterns",
    "DetectionResult",
    "validate_hook_data",
    "__version__",
]
