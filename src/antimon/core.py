# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Core validation logic for antimon
"""

import json
import logging
import sys

from .color_utils import ColorFormatter
from .detectors import (
    HookData,
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
from .last_error import save_last_error
from .logger import get_logger
from .runtime_config import get_runtime_config

logger = get_logger()


def validate_hook_data(json_data: HookData) -> tuple[bool, list[str], dict[str, int]]:
    """
    Validate hook data for security issues

    Args:
        json_data: Hook data from AI assistant

    Returns:
        Tuple of (has_issues, list_of_messages, detector_stats)
    """
    # Get runtime configuration
    config = get_runtime_config()

    # Define code-editing tools that need validation
    code_editing_tools = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

    # Define tools that need special validation
    special_validation_tools = {"Read", "Bash"}

    # Define safe tools that don't need validation
    safe_tools = {
        "LS", "Glob", "Grep", "NotebookRead",
        "WebFetch", "WebSearch", "TodoWrite", "exit_plan_mode"
    }

    tool_name = json_data.get("tool_name", "")

    # Check if file is ignored by runtime config
    # Note: We moved this check to individual detectors to allow
    # filename detection to be skipped while other detectors still run

    # Skip truly safe tools
    if tool_name in safe_tools:
        logger.debug(f"Skipping safe non-code-editing tool: {tool_name}")
        return False, [], {}
    elif tool_name not in code_editing_tools and tool_name not in special_validation_tools:
        if tool_name:
            logger.debug(f"Skipping unknown tool: {tool_name}")
        else:
            logger.debug("No tool name provided")
        return False, [], {}

    # Select appropriate detectors based on tool type
    if tool_name in code_editing_tools:
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

        # Check if detector is enabled
        if not config.is_detector_enabled(detector.__name__):
            logger.debug(f"Skipping disabled detector: {detector.__name__}")
            continue

        logger.debug(f"Running detector: {detector.__name__}")
        try:
            result = detector(json_data)
            if result.detected:
                logger.debug(
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
            issues.append(f"Internal error in {detector.__name__} detector: {e!s}")
            detector_stats["errors"] += 1
            detailed_results.append({
                "detector": detector_name,
                "status": "ERROR",
                "message": str(e),
                "file_path": json_data.get("tool_input", {}).get("file_path", "N/A")
            })

    # Log structured results in verbose mode
    if logger.is_enabled_for(logging.DEBUG):
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
            error_msg = f"❌ JSON parsing error: {e}\n\n💡 How to fix:\n"
            error_msg += "   Ensure your input is valid JSON. Example of valid format:\n"
            error_msg += '   {\n'
            error_msg += '     "hook_event_name": "PreToolUse",\n'
            error_msg += '     "tool_name": "Write",\n'
            error_msg += '     "tool_input": {\n'
            error_msg += '       "file_path": "example.py",\n'
            error_msg += '       "content": "print(\'Hello\')"}\n'
            error_msg += '   }\n'
            error_msg += "\n   Common issues:\n"
            error_msg += "   • Missing quotes around strings\n"
            error_msg += "   • Trailing commas after last item\n"
            error_msg += "   • Unescaped quotes in strings (use \\\") \n"
            error_msg += "   • Missing brackets or braces"
            logger.error(error_msg)
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
    code_editing_tools = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

    # Validate required fields for code-editing tools
    if tool_name in code_editing_tools:
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
    if tool_name == "Read" and "file_path" not in tool_input:
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
    if tool_name == "Bash" and "command" not in tool_input:
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
                           tool_name: str, color: ColorFormatter, verbose: bool, quiet: bool, no_color: bool = False, dry_run: bool = False) -> None:
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
        no_color: Disable colored output
        dry_run: If True, show issues but don't block
    """
    logger.info(f"Security validation failed with {len(issues)} issue(s)")

    # Create error context handler
    error_context = ErrorContext(no_color=no_color)

    # Always show security issues, even in quiet mode
    if dry_run:
        print(f"\n{color.warning('🔍 DRY RUN - Security issues that would be detected:')}", file=sys.stderr)
    else:
        print(f"\n{color.error('⚠️  Security issues detected:')}", file=sys.stderr)

    # Structured output for issues
    if verbose and not quiet:
        print("\n📊 Detection Results:", file=sys.stderr)
        print(f"   File: {json_data.get('tool_input', {}).get('file_path', 'N/A')}", file=sys.stderr)
        print(f"   Tool: {tool_name}", file=sys.stderr)
        print(f"   Summary: {stats['failed']} failed, {stats['passed']} passed, {stats['errors']} errors\n", file=sys.stderr)
        print("   Issues found:", file=sys.stderr)
        for i, issue in enumerate(issues, 1):
            print(f"   [{i}] {issue}", file=sys.stderr)
            # Add context for each issue
            context = error_context.get_context_for_error(issue, json_data)
            if context:
                print(f"\n{context}", file=sys.stderr)
    else:
        for issue in issues:
            print(f"  • {color.format_security_issue(issue)}", file=sys.stderr)

        # Show context for the first issue in non-verbose mode
        if issues and not quiet:
            print("", file=sys.stderr)  # Empty line
            context = error_context.get_context_for_error(issues[0], json_data)
            if context:
                print(context, file=sys.stderr)

    if not quiet:
        if dry_run:
            print("\n💡 DRY RUN Summary:", file=sys.stderr)
            print("   • This is a preview of what would be blocked", file=sys.stderr)
            print("   • No actual blocking occurred", file=sys.stderr)
            print("   • To actually block these operations, run without --dry-run", file=sys.stderr)
            print("   • To allow specific files, use --allow-file", file=sys.stderr)
            print("   • To disable specific detectors, use --disable-detector\n", file=sys.stderr)
        else:
            print("\n💡 How to proceed:", file=sys.stderr)
            print("   1. Review the detected issues above", file=sys.stderr)
            print("   2. Run 'antimon --explain-last-error' for detailed explanations", file=sys.stderr)
            print("   3. If false positive, consider:", file=sys.stderr)
            print("      • Using environment variables instead of hardcoded values", file=sys.stderr)
            print("      • Moving sensitive data to separate config files", file=sys.stderr)
            print("      • Using --allow-file or --ignore-pattern options", file=sys.stderr)
            print("   4. For legitimate use cases, you can:", file=sys.stderr)
            print("      • Temporarily disable the hook in Claude Code settings", file=sys.stderr)
            print("      • Report false positives at: https://github.com/antimon-security/antimon/issues\n", file=sys.stderr)


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
    code_editing_tools = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    special_validation_tools = {"Read", "Bash"}
    safe_tools = {
        "LS", "Glob", "Grep", "NotebookRead",
        "WebFetch", "WebSearch", "TodoWrite", "exit_plan_mode"
    }

    tool_name = json_data.get("tool_name", "")

    # Validate required fields
    validation_result = _validate_required_fields(json_data, tool_name, color, quiet)
    if validation_result != 0:
        return validation_result

    # Provide feedback for non-code-editing tools
    if tool_name not in code_editing_tools and tool_name not in special_validation_tools:
        if tool_name in safe_tools:
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

    # Get runtime config at the beginning
    config = get_runtime_config()

    # Validate code-editing tools
    has_issues, issues, stats = validate_hook_data(json_data)

    # In verbose mode, add pattern visualization
    if verbose and has_issues:
        enhanced_issues = []
        for issue in issues:
            # Add visual separator for each issue
            enhanced_issue = "─" * 60 + "\n" + issue
            enhanced_issues.append(enhanced_issue)
        issues = enhanced_issues
    elif not verbose and has_issues:
        # In non-verbose mode, simplify error messages
        simplified_issues = []
        for issue in issues:
            # Keep only essential information
            lines = issue.split('\n')
            essential_lines = []
            for line in lines:
                line_stripped = line.strip()
                # Keep main message, risk, suggestion, and allow-file hint
                if (not line_stripped.startswith('Pattern matched:') and
                    not line_stripped.startswith('Type:') and
                    not line_stripped.startswith('Found:')):
                    essential_lines.append(line)
            simplified_issues.append('\n'.join(essential_lines))
        issues = simplified_issues

    if has_issues:
        # Get runtime config to check for dry run mode
        config = get_runtime_config()

        # Save the error for later explanation (even in dry run)
        save_last_error(issues, json_data)
        _display_security_issues(issues, stats, json_data, tool_name, color, verbose, quiet, no_color, dry_run=config.dry_run)

        # In dry run mode, return success (0) instead of error (2)
        if config.dry_run:
            return 0
        else:
            return 2

    logger.info("Security validation passed")
    if config.show_stats or verbose:
        if not quiet:
            # Show detailed summary
            print("\n📊 Detection Summary:", file=sys.stderr)
            print(f"   • Total detectors run: {stats['total']}", file=sys.stderr)
            print(f"   • Passed: {stats['passed']}", file=sys.stderr)
            print(f"   • Failed: {stats['failed']}", file=sys.stderr)
            if stats['errors'] > 0:
                print(f"   • Errors: {stats['errors']}", file=sys.stderr)
    elif not quiet:
        # Simple success message in normal mode
        print("✅ Check passed", file=sys.stderr)
    return 0


def check_file_directly(file_path: str, verbose: bool = False, quiet: bool = False, no_color: bool = False) -> int:
    """
    Check a file directly without JSON input.

    Args:
        file_path: Path to the file to check
        verbose: Enable verbose output
        quiet: Suppress all output except errors
        no_color: Disable colored output

    Returns:
        Exit code (0=success, 1=error, 2=security issues)
    """
    import os

    # Initialize color formatter
    color = ColorFormatter(use_color=not no_color)

    # Check if file exists
    if not os.path.exists(file_path):
        if not quiet:
            print(f"\n{color.error('❌ Error:')} File not found: {file_path}", file=sys.stderr)
        return 1

    # Read file content
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        if not quiet:
            print(f"\n{color.error('❌ Error reading file:')} {e}", file=sys.stderr)
        return 1

    # Create JSON data for validation
    json_data: HookData = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": os.path.abspath(file_path),
            "content": content
        }
    }

    # Get runtime config at the beginning
    config = get_runtime_config()

    # Validate the file
    has_issues, issues, stats = validate_hook_data(json_data)

    if has_issues:
        # Get runtime config to check for dry run mode
        config = get_runtime_config()

        # Save the error for later explanation
        save_last_error(issues, json_data)
        _display_security_issues(issues, stats, json_data, "Write", color, verbose, quiet, no_color, dry_run=config.dry_run)

        # In dry run mode, return success (0) instead of error (2)
        if config.dry_run:
            return 0
        else:
            return 2

    if config.show_stats or verbose:
        if not quiet:
            print(f"\n✅ File '{file_path}' passed all security checks", file=sys.stderr)
            print("\n📊 Detection Summary:", file=sys.stderr)
            print(f"   • Total detectors run: {stats['total']}", file=sys.stderr)
            print(f"   • Passed: {stats['passed']}", file=sys.stderr)
            print(f"   • Failed: {stats['failed']}", file=sys.stderr)
            if stats['errors'] > 0:
                print(f"   • Errors: {stats['errors']}", file=sys.stderr)
    elif not quiet:
        print(f"✅ No security issues found in '{file_path}'", file=sys.stderr)

    return 0


def check_content_directly(content: str, file_name: str = "stdin", verbose: bool = False, quiet: bool = False, no_color: bool = False) -> int:
    """
    Check content directly without JSON input.

    Args:
        content: Content to check
        file_name: Optional file name for context
        verbose: Enable verbose output
        quiet: Suppress all output except errors
        no_color: Disable colored output

    Returns:
        Exit code (0=success, 2=security issues)
    """
    # Initialize color formatter
    color = ColorFormatter(use_color=not no_color)

    # Create JSON data for validation
    json_data: HookData = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": file_name,
            "content": content
        }
    }

    # Get runtime config at the beginning
    config = get_runtime_config()

    # Validate the content
    has_issues, issues, stats = validate_hook_data(json_data)

    if has_issues:
        # Get runtime config to check for dry run mode
        config = get_runtime_config()

        # Save the error for later explanation
        save_last_error(issues, json_data)
        _display_security_issues(issues, stats, json_data, "Write", color, verbose, quiet, no_color, dry_run=config.dry_run)

        # In dry run mode, return success (0) instead of error (2)
        if config.dry_run:
            return 0
        else:
            return 2

    if config.show_stats or verbose:
        if not quiet:
            print("\n✅ Content passed all security checks", file=sys.stderr)
            print("\n📊 Detection Summary:", file=sys.stderr)
            print(f"   • Total detectors run: {stats['total']}", file=sys.stderr)
            print(f"   • Passed: {stats['passed']}", file=sys.stderr)
            print(f"   • Failed: {stats['failed']}", file=sys.stderr)
            if stats['errors'] > 0:
                print(f"   • Errors: {stats['errors']}", file=sys.stderr)
    elif not quiet:
        print("✅ No security issues found in provided content", file=sys.stderr)

    return 0
