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
    # Define code-editing tools that need validation
    CODE_EDITING_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    
    # Define known safe tools that don't need validation
    SAFE_TOOLS = {
        "Read", "Bash", "LS", "Glob", "Grep", "NotebookRead",
        "WebFetch", "WebSearch", "TodoWrite", "exit_plan_mode"
    }
    
    tool_name = json_data.get("tool_name", "")
    
    # Skip non-code-editing operations
    if tool_name not in CODE_EDITING_TOOLS:
        if tool_name in SAFE_TOOLS:
            logger.debug(f"Skipping safe non-code-editing tool: {tool_name}")
        elif tool_name:
            logger.debug(f"Skipping unknown tool: {tool_name}")
        else:
            logger.debug("No tool name provided")
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
            issues.append(f"Internal error in {detector.__name__} detector: {str(e)}")

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
        print(f"\n❌ JSON parsing error: {e}", file=sys.stderr)
        print("\n💡 How to fix:", file=sys.stderr)
        print("   Ensure your input is valid JSON. Example of valid format:", file=sys.stderr)
        print('   {', file=sys.stderr)
        print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
        print('     "tool_name": "Write",', file=sys.stderr)
        print('     "tool_input": {', file=sys.stderr)
        print('       "file_path": "example.py",', file=sys.stderr)
        print('       "content": "print(\'Hello\')"}', file=sys.stderr)
        print('   }', file=sys.stderr)
        print("\n   Common issues:", file=sys.stderr)
        print("   • Missing quotes around strings", file=sys.stderr)
        print("   • Trailing commas after last item", file=sys.stderr)
        print("   • Unescaped quotes in strings (use \\\") ", file=sys.stderr)
        print("   • Missing brackets or braces\n", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected error reading input: {e}", exc_info=True)
        print(f"\n❌ Error reading input: {e}", file=sys.stderr)
        print("\n💡 How to fix:", file=sys.stderr)
        print("   • Ensure data is being piped to stdin", file=sys.stderr)
        print("   • Example: echo '{...}' | antimon", file=sys.stderr)
        print("   • Or: cat hook_data.json | antimon\n", file=sys.stderr)
        return 1

    # Define tool categories for user feedback
    CODE_EDITING_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    SAFE_TOOLS = {
        "Read", "Bash", "LS", "Glob", "Grep", "NotebookRead",
        "WebFetch", "WebSearch", "TodoWrite", "exit_plan_mode"
    }
    
    tool_name = json_data.get("tool_name", "")
    
    # Provide feedback for non-code-editing tools
    if tool_name not in CODE_EDITING_TOOLS:
        if tool_name in SAFE_TOOLS:
            logger.info(f"Safe tool {tool_name} - no security validation needed")
            if not verbose:
                print(f"ℹ️  Tool '{tool_name}' is considered safe - no security validation performed", file=sys.stderr)
        elif tool_name:
            logger.info(f"Unknown tool {tool_name} - skipping validation")
            if not verbose:
                print(f"ℹ️  Unknown tool '{tool_name}' - no security validation performed", file=sys.stderr)
        else:
            logger.info("No tool name provided - skipping validation")
            if not verbose:
                print("ℹ️  No tool specified - no security validation performed", file=sys.stderr)
        return 0
    
    # Validate code-editing tools
    has_issues, issues = validate_hook_data(json_data)

    if has_issues:
        logger.info(f"Security validation failed with {len(issues)} issue(s)")
        print("\n⚠️  Security issues detected:", file=sys.stderr)
        for issue in issues:
            print(f"  • {issue}", file=sys.stderr)
        print("\n💡 How to proceed:", file=sys.stderr)
        print("   1. Review the detected issues above", file=sys.stderr)
        print("   2. If false positive, consider:", file=sys.stderr)
        print("      • Using environment variables instead of hardcoded values", file=sys.stderr)
        print("      • Moving sensitive data to separate config files", file=sys.stderr)
        print("      • Adding patterns to whitelist (config support coming in v0.3.0)", file=sys.stderr)
        print("   3. For legitimate use cases, you can:", file=sys.stderr)
        print("      • Temporarily disable the hook in Claude Code settings", file=sys.stderr)
        print("      • Report false positives at: https://github.com/yourusername/antimon/issues\n", file=sys.stderr)
        return 2

    logger.info("Security validation passed")
    if not verbose:
        # In non-verbose mode, print success message
        print("✅ No security issues detected", file=sys.stderr)
    return 0
