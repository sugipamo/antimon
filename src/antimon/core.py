# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Core validation logic for antimon
"""

import json
import sys
from typing import Any

from .detectors import (
    detect_api_key,
    detect_claude_antipatterns,
    detect_docker,
    detect_filenames,
    detect_llm_api,
    detect_localhost,
)
from .logging_config import get_logger

logger = get_logger(__name__)


def validate_hook_data(json_data: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate hook data for security issues

    Args:
        json_data: Hook data from AI assistant

    Returns:
        Tuple of (has_issues, list_of_messages)
    """
    # Skip non-code-editing operations
    tool_name = json_data.get("tool_name", "")
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        logger.debug(f"Skipping non-code-editing tool: {tool_name}")
        return False, []

    detectors = [
        detect_filenames,
        detect_llm_api,
        detect_api_key,
        detect_docker,
        detect_localhost,
        detect_claude_antipatterns,
    ]

    issues = []

    for detector in detectors:
        logger.debug(f"Running detector: {detector.__name__}")
        try:
            result = detector(json_data)
            if result.detected:
                logger.warning(
                    f"Detector {detector.__name__} found issue: {result.message}"
                )
                issues.append(result.message)
        except Exception as e:
            logger.error(f"Error in detector {detector.__name__}: {e}", exc_info=True)
            issues.append(f"Internal error in {detector.__name__} detector")

    return len(issues) > 0, issues


def process_stdin(verbose: bool = False) -> int:
    """
    Process JSON input from stdin and validate

    Returns:
        Exit code (0=success, 1=parse error, 2=security issues)
    """
    try:
        logger.debug("Reading input from stdin")
        input_data = sys.stdin.read()
        json_data = json.loads(input_data)
        logger.debug(
            f"Parsed JSON data with tool: {json_data.get('tool_name', 'unknown')}"
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        print(f"JSON parsing error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected error reading input: {e}", exc_info=True)
        print(f"Error reading input: {e}", file=sys.stderr)
        return 1

    has_issues, issues = validate_hook_data(json_data)

    if has_issues:
        logger.info(f"Security validation failed with {len(issues)} issue(s)")
        print("Security issues detected:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 2

    logger.info("Security validation passed")
    if not verbose:
        # In non-verbose mode, print success message
        print("No security issues detected", file=sys.stderr)
    return 0
