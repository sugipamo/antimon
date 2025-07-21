# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Core validation logic for antimon
"""

import json
import logging
import sys
from typing import Any

from .detectors import HookData

from .detectors import (
    detect_api_key,
    detect_bash_dangerous_commands,
    detect_claude_antipatterns,
    detect_docker,
    detect_filenames,
    detect_llm_api,
    detect_localhost,
    detect_read_sensitive_files,
)
from .logging_config import get_logger
from .color_utils import ColorFormatter

logger = get_logger(__name__)


def validate_hook_data(json_data: HookData) -> tuple[bool, list[str], dict[str, int]]:
    """
    Validate hook data for security issues

    Args:
        json_data: Hook data from AI assistant

    Returns:
        Tuple of (has_issues, list_of_messages, detector_stats)
    """
    # Define code-editing tools that need validation
    CODE_EDITING_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    
    # Define tools that need special validation
    SPECIAL_VALIDATION_TOOLS = {"Read", "Bash"}
    
    # Define safe tools that don't need validation
    SAFE_TOOLS = {
        "LS", "Glob", "Grep", "NotebookRead",
        "WebFetch", "WebSearch", "TodoWrite", "exit_plan_mode"
    }
    
    tool_name = json_data.get("tool_name", "")
    
    # Skip truly safe tools
    if tool_name in SAFE_TOOLS:
        logger.debug(f"Skipping safe non-code-editing tool: {tool_name}")
        return False, [], {}
    elif tool_name not in CODE_EDITING_TOOLS and tool_name not in SPECIAL_VALIDATION_TOOLS:
        if tool_name:
            logger.debug(f"Skipping unknown tool: {tool_name}")
        else:
            logger.debug("No tool name provided")
        return False, [], {}

    # Select appropriate detectors based on tool type
    if tool_name in CODE_EDITING_TOOLS:
        detectors = [
            detect_filenames,
            detect_llm_api,
            detect_api_key,
            detect_docker,
            detect_localhost,
            detect_claude_antipatterns,
        ]
    elif tool_name == "Read":
        detectors = [detect_read_sensitive_files]
    elif tool_name == "Bash":
        detectors = [detect_bash_dangerous_commands]
    else:
        # Fallback to all detectors
        detectors = [
            detect_filenames,
            detect_llm_api,
            detect_api_key,
            detect_docker,
            detect_localhost,
            detect_claude_antipatterns,
            detect_read_sensitive_files,
            detect_bash_dangerous_commands,
        ]

    issues = []
    detector_stats = {
        "total": len(detectors),
        "passed": 0,
        "failed": 0,
        "errors": 0
    }
    detailed_results = []  # For structured logging

    for detector in detectors:
        detector_name = detector.__name__.replace("detect_", "").replace("_", " ").title()
        logger.debug(f"Running detector: {detector.__name__}")
        try:
            result = detector(json_data)
            if result.detected:
                logger.warning(
                    f"Detector {detector.__name__} found issue: {result.message}"
                )
                issues.append(result.message)
                detector_stats["failed"] += 1
                detailed_results.append({
                    "detector": detector_name,
                    "status": "FAILED",
                    "message": result.message,
                    "file_path": json_data.get("tool_input", {}).get("file_path", "N/A")
                })
            else:
                detector_stats["passed"] += 1
                detailed_results.append({
                    "detector": detector_name,
                    "status": "PASSED",
                    "message": None,
                    "file_path": json_data.get("tool_input", {}).get("file_path", "N/A")
                })
        except Exception as e:
            logger.error(f"Error in detector {detector.__name__}: {e}", exc_info=True)
            issues.append(f"Internal error in {detector.__name__} detector: {str(e)}")
            detector_stats["errors"] += 1
            detailed_results.append({
                "detector": detector_name,
                "status": "ERROR",
                "message": str(e),
                "file_path": json_data.get("tool_input", {}).get("file_path", "N/A")
            })

    # Log structured results in verbose mode
    if logger.isEnabledFor(logging.DEBUG):
        for result in detailed_results:
            logger.debug(
                f"[{result['status']}] {result['detector']} - "
                f"File: {result['file_path']} - "
                f"{'Message: ' + result['message'] if result['message'] else 'No issues'}"
            )
    
    return len(issues) > 0, issues, detector_stats


def _parse_json_input(color: ColorFormatter, quiet: bool) -> tuple[HookData | None, int]:
    """
    Parse JSON input from stdin.
    
    Args:
        color: Color formatter instance
        quiet: Suppress all output except errors
        
    Returns:
        Tuple of (parsed_json_data, exit_code). If error, json_data is None.
    """
    try:
        logger.debug("Reading input from stdin")
        input_data = sys.stdin.read()
        json_data = json.loads(input_data)
        logger.debug(
            f"Parsed JSON data with tool: {json_data.get('tool_name', 'unknown')}"
        )
        return json_data, 0
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        if not quiet:
            print(f"\n{color.error('❌ JSON parsing error:')} {e}", file=sys.stderr)
            print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
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
        return None, 1
    except Exception as e:
        logger.error(f"Unexpected error reading input: {e}", exc_info=True)
        if not quiet:
            print(f"\n{color.error('❌ Error reading input:')} {e}", file=sys.stderr)
            print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
            print("   • Ensure data is being piped to stdin", file=sys.stderr)
            print("   • Example: echo '{...}' | antimon", file=sys.stderr)
            print("   • Or: cat hook_data.json | antimon\n", file=sys.stderr)
        return None, 1


def _validate_required_fields(json_data: HookData, tool_name: str, color: ColorFormatter, quiet: bool) -> int:
    """
    Validate required fields for different tool types.
    
    Args:
        json_data: Parsed JSON data
        tool_name: Name of the tool being used
        color: Color formatter instance
        quiet: Suppress all output except errors
        
    Returns:
        Exit code (0=valid, 1=missing required fields)
    """
    tool_input = json_data.get("tool_input", {})
    CODE_EDITING_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    
    # Validate required fields for code-editing tools
    if tool_name in CODE_EDITING_TOOLS:
        # Check for required fields based on tool type
        if tool_name == "Write":
            if "content" not in tool_input:
                logger.error(f"Missing required field 'content' for {tool_name} tool")
                if not quiet:
                    print(f"\n{color.error('❌ Validation error:')} Missing required field 'content' for {tool_name} tool", file=sys.stderr)
                    print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
                    print("   The Write tool requires both 'file_path' and 'content' fields:", file=sys.stderr)
                    print('   {', file=sys.stderr)
                    print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
                    print('     "tool_name": "Write",', file=sys.stderr)
                    print('     "tool_input": {', file=sys.stderr)
                    print('       "file_path": "example.py",', file=sys.stderr)
                    print('       "content": "file contents here"', file=sys.stderr)
                    print('     }', file=sys.stderr)
                    print('   }\n', file=sys.stderr)
                return 1
        elif tool_name in {"Edit", "MultiEdit"}:
            # Edit tools need either 'new_string' or both 'old_string' and 'new_string'
            if "new_string" not in tool_input:
                logger.error(f"Missing required field 'new_string' for {tool_name} tool")
                if not quiet:
                    print(f"\n❌ Validation error: Missing required field 'new_string' for {tool_name} tool", file=sys.stderr)
                    print("\n💡 How to fix:", file=sys.stderr)
                    print(f"   The {tool_name} tool requires 'old_string' and 'new_string' fields:", file=sys.stderr)
                    print('   {', file=sys.stderr)
                    print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
                    print(f'     "tool_name": "{tool_name}",', file=sys.stderr)
                    print('     "tool_input": {', file=sys.stderr)
                    print('       "file_path": "example.py",', file=sys.stderr)
                    print('       "old_string": "text to replace",', file=sys.stderr)
                    print('       "new_string": "replacement text"', file=sys.stderr)
                    print('     }', file=sys.stderr)
                    print('   }\n', file=sys.stderr)
                return 1
    
    # Validate required fields for Read tool
    if tool_name == "Read":
        if "file_path" not in tool_input:
            logger.error(f"Missing required field 'file_path' for {tool_name} tool")
            if not quiet:
                print(f"\n{color.error('❌ Validation error:')} Missing required field 'file_path' for {tool_name} tool", file=sys.stderr)
                print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
                print("   The Read tool requires a 'file_path' field:", file=sys.stderr)
                print('   {', file=sys.stderr)
                print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
                print('     "tool_name": "Read",', file=sys.stderr)
                print('     "tool_input": {', file=sys.stderr)
                print('       "file_path": "/path/to/file"', file=sys.stderr)
                print('     }', file=sys.stderr)
                print('   }\n', file=sys.stderr)
            return 1
    
    # Validate required fields for Bash tool
    if tool_name == "Bash":
        if "command" not in tool_input:
            logger.error(f"Missing required field 'command' for {tool_name} tool")
            if not quiet:
                print(f"\n{color.error('❌ Validation error:')} Missing required field 'command' for {tool_name} tool", file=sys.stderr)
                print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
                print("   The Bash tool requires a 'command' field:", file=sys.stderr)
                print('   {', file=sys.stderr)
                print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
                print('     "tool_name": "Bash",', file=sys.stderr)
                print('     "tool_input": {', file=sys.stderr)
                print('       "command": "ls -la"', file=sys.stderr)
                print('     }', file=sys.stderr)
                print('   }\n', file=sys.stderr)
            return 1
    
    return 0


def _display_security_issues(issues: list[str], stats: dict[str, int], json_data: HookData, 
                           tool_name: str, color: ColorFormatter, verbose: bool, quiet: bool) -> None:
    """
    Display security issues found during validation.
    
    Args:
        issues: List of security issues found
        stats: Detection statistics
        json_data: Original JSON data
        tool_name: Name of the tool being used
        color: Color formatter instance
        verbose: Enable verbose output
        quiet: Suppress all output except errors
    """
    logger.info(f"Security validation failed with {len(issues)} issue(s)")
    # Always show security issues, even in quiet mode
    print(f"\n{color.error('⚠️  Security issues detected:')}", file=sys.stderr)
    
    # Structured output for issues
    if verbose and not quiet:
        print(f"\n📊 Detection Results:", file=sys.stderr)
        print(f"   File: {json_data.get('tool_input', {}).get('file_path', 'N/A')}", file=sys.stderr)
        print(f"   Tool: {tool_name}", file=sys.stderr)
        print(f"   Summary: {stats['failed']} failed, {stats['passed']} passed, {stats['errors']} errors\n", file=sys.stderr)
        print("   Issues found:", file=sys.stderr)
        for i, issue in enumerate(issues, 1):
            print(f"   [{i}] {issue}", file=sys.stderr)
    else:
        for issue in issues:
            print(f"  • {color.format_security_issue(issue)}", file=sys.stderr)
    
    if not quiet:
        print("\n💡 How to proceed:", file=sys.stderr)
        print("   1. Review the detected issues above", file=sys.stderr)
        print("   2. If false positive, consider:", file=sys.stderr)
        print("      • Using environment variables instead of hardcoded values", file=sys.stderr)
        print("      • Moving sensitive data to separate config files", file=sys.stderr)
        print("      • Adding patterns to whitelist (config support coming in v0.3.0)", file=sys.stderr)
        print("   3. For legitimate use cases, you can:", file=sys.stderr)
        print("      • Temporarily disable the hook in Claude Code settings", file=sys.stderr)
        print("      • Report false positives at: https://github.com/yourusername/antimon/issues\n", file=sys.stderr)


def process_stdin(verbose: bool = False, quiet: bool = False, no_color: bool = False) -> int:
    """
    Process JSON input from stdin and validate

    Args:
        verbose: Enable verbose output
        quiet: Suppress all output except errors
        no_color: Disable colored output

    Returns:
        Exit code (0=success, 1=parse error, 2=security issues)
    """
    # Initialize color formatter
    color = ColorFormatter(use_color=not no_color)
    
    # Parse JSON input
    json_data, exit_code = _parse_json_input(color, quiet)
    if exit_code != 0:
        return exit_code

    # Define tool categories for user feedback
    CODE_EDITING_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    SPECIAL_VALIDATION_TOOLS = {"Read", "Bash"}
    SAFE_TOOLS = {
        "LS", "Glob", "Grep", "NotebookRead",
        "WebFetch", "WebSearch", "TodoWrite", "exit_plan_mode"
    }
    
    tool_name = json_data.get("tool_name", "")
    
    # Validate required fields
    validation_result = _validate_required_fields(json_data, tool_name, color, quiet)
    if validation_result != 0:
        return validation_result
    
    # Provide feedback for non-code-editing tools
    if tool_name not in CODE_EDITING_TOOLS and tool_name not in SPECIAL_VALIDATION_TOOLS:
        if tool_name in SAFE_TOOLS:
            logger.info(f"Safe tool {tool_name} - no security validation needed")
            if verbose and not quiet:
                print(f"ℹ️  Tool '{tool_name}' is considered safe - no security validation performed", file=sys.stderr)
        elif tool_name:
            logger.info(f"Unknown tool {tool_name} - skipping validation")
            if verbose and not quiet:
                print(f"ℹ️  Unknown tool '{tool_name}' - no security validation performed", file=sys.stderr)
        else:
            logger.info("No tool name provided - skipping validation")
            if verbose and not quiet:
                print("ℹ️  No tool specified - no security validation performed", file=sys.stderr)
        return 0
    
    # Validate code-editing tools
    has_issues, issues, stats = validate_hook_data(json_data)
    
    # In non-verbose mode, simplify error messages
    if not verbose and has_issues:
        simplified_issues = []
        for issue in issues:
            # Remove pattern details from messages unless in verbose mode
            lines = issue.split('\n')
            simplified_lines = []
            for line in lines:
                if not line.strip().startswith('Pattern matched:'):
                    simplified_lines.append(line)
            simplified_issues.append('\n'.join(simplified_lines))
        issues = simplified_issues

    if has_issues:
        _display_security_issues(issues, stats, json_data, tool_name, color, verbose, quiet)
        return 2

    logger.info("Security validation passed")
    if verbose and not quiet:
        # Only in verbose mode, show detailed summary
        print(f"\n📊 Detection Summary:", file=sys.stderr)
        print(f"   • Total detectors run: {stats['total']}", file=sys.stderr)
        print(f"   • Passed: {stats['passed']}", file=sys.stderr)
        print(f"   • Failed: {stats['failed']}", file=sys.stderr)
        if stats['errors'] > 0:
            print(f"   • Errors: {stats['errors']}", file=sys.stderr)
    # No output in normal mode when no issues are detected (matches README example)
    return 0
