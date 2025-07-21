"""
Core validation logic for antimon
"""

from typing import Dict, Any, List, Tuple
import sys
import json

from .detectors import (
    detect_filenames,
    detect_llm_api,
    detect_api_key,
    detect_docker,
    detect_localhost,
    detect_claude_antipatterns,
)


def validate_hook_data(json_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
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
        result = detector(json_data)
        if result.detected:
            issues.append(result.message)

    return len(issues) > 0, issues


def process_stdin() -> int:
    """
    Process JSON input from stdin and validate

    Returns:
        Exit code (0=success, 1=parse error, 2=security issues)
    """
    try:
        input_data = sys.stdin.read()
        json_data = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}", file=sys.stderr)
        return 1

    has_issues, issues = validate_hook_data(json_data)

    if has_issues:
        print("Security issues detected:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 2

    return 0
