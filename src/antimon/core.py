# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Core validation logic for antimon
"""

import glob
import json
import logging
import os
import sys
import time

from .color_utils import ColorFormatter
from .config import load_config
from .constants import ISSUE_TRACKER_URL
from .detectors import HookData
from .error_context import ErrorContext
from .last_error import save_last_error
from .logger import get_logger
from .runtime_config import get_runtime_config
from .pattern_detector import PatternDetector
from .ai_detector import AIDetector

logger = get_logger()


def validate_hook_data(
    json_data: HookData,
    quiet: bool = False, 
    no_color: bool = False
) -> tuple[bool, list[str], dict[str, int | float]]:
    """
    Validate hook data for security issues

    Args:
        json_data: Hook data from AI assistant
        quiet: Suppress warning messages
        no_color: Disable colored output

    Returns:
        Tuple of (has_issues, list_of_messages, detector_stats)
    """
    start_time = time.time()
    # Get runtime configuration
    config = get_runtime_config()

    # Define code-editing tools that need validation
    code_editing_tools = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

    # Define tools that need special validation
    special_validation_tools = {"Read", "Bash"}

    # Define safe tools that don't need validation
    safe_tools = {
        "LS",
        "Glob",
        "Grep",
        "NotebookRead",
        "WebFetch",
        "WebSearch",
        "TodoWrite",
        "exit_plan_mode",
    }

    tool_name = json_data.get("tool_name", "")

    # Check if file is ignored by runtime config
    # Note: We moved this check to individual detectors to allow
    # filename detection to be skipped while other detectors still run

    # Skip truly safe tools
    if tool_name in safe_tools:
        logger.debug(f"Skipping safe non-code-editing tool: {tool_name}")
        return False, [], {}
    elif (
        tool_name not in code_editing_tools
        and tool_name not in special_validation_tools
    ):
        if tool_name:
            logger.debug(f"Skipping unknown tool: {tool_name}")
        else:
            logger.debug("No tool name provided")
        return False, [], {}

    issues = []
    detector_stats = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "total_time": 0.0,
        "detector_times": {},
        "patterns_checked": 0,
        "content_size": 0,
    }
    detailed_results = []  # For structured logging

    # Get content size if available
    tool_input = json_data.get("tool_input", {})
    if isinstance(tool_input, dict):
        content = tool_input.get("content", "")
        if content:
            detector_stats["content_size"] = len(content)

    # Run pattern-based detectors from config file
    try:
        pattern_detector = PatternDetector()
        pattern_results = pattern_detector.detect_patterns(json_data)
        
        for result in pattern_results:
            if result.detected:
                issues.append(result.message)
                detector_stats["failed"] += 1
                detailed_results.append({
                    "detector": f"Pattern: {result.details.get('pattern_name', 'unknown')}",
                    "status": "FAILED",
                    "message": result.message,
                    "file_path": json_data.get("tool_input", {}).get("file_path", "N/A"),
                })
            detector_stats["patterns_checked"] += 1
    except Exception as e:
        logger.error(f"Error in pattern detector: {e}", exc_info=True)
        detector_stats["errors"] += 1

    # Run AI-powered detectors from config file
    try:
        ai_config = load_config()
        for ai_name, ai_detector_config in ai_config.ai_detectors.items():
            if not ai_detector_config.enabled:
                continue
                
            detector_stats["total"] += 1
            
            try:
                # Create AI detector
                api_key = os.environ.get(ai_detector_config.api_key_env)
                if not api_key:
                    # Always show warning for missing API key (even in quiet mode)
                    from .color_utils import ColorFormatter
                    color = ColorFormatter(use_color=not no_color)
                    print(f"{color.warning('⚠️  AI Detector Warning:')} {ai_name} is enabled but {ai_detector_config.api_key_env} is not set", file=sys.stderr)
                    print(f"{color.info('💡 To enable AI detection:')} Run 'antimon help api-setup' for setup instructions", file=sys.stderr)
                    logger.debug(f"Skipping AI detector {ai_name}: API key not found")
                    continue
                
                ai_detector = AIDetector(api_key=api_key, api_base=ai_detector_config.api_base)
                
                # Run detection
                result = ai_detector.detect_from_hook_data(
                    json_data,
                    ai_detector_config.prompt,
                    ai_detector_config.model
                )
                
                if result.detected:
                    issues.append(f"[AI/{ai_name}] {result.message}")
                    detector_stats["failed"] += 1
                    detailed_results.append({
                        "detector": f"AI: {ai_name}",
                        "status": "FAILED",
                        "message": result.message,
                        "file_path": json_data.get("tool_input", {}).get("file_path", "N/A"),
                    })
                else:
                    detector_stats["passed"] += 1
                    
            except Exception as e:
                logger.error(f"Error in AI detector {ai_name}: {e}", exc_info=True)
                detector_stats["errors"] += 1
                
    except Exception as e:
        logger.error(f"Error loading AI detectors: {e}", exc_info=True)

    # Log structured results in verbose mode
    if logger.is_enabled_for(logging.DEBUG):
        for result in detailed_results:
            logger.debug(
                f"[{result['status']}] {result['detector']} - "
                f"File: {result['file_path']} - "
                f"{'Message: ' + result['message'] if result['message'] else 'No issues'}"
            )

    # Calculate total time
    detector_stats["total_time"] = time.time() - start_time

    return len(issues) > 0, issues, detector_stats


def _parse_json_input(
    color: ColorFormatter, quiet: bool
) -> tuple[HookData | None, int]:
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
        logger.debug(f"JSON parsing error: {e}")
        if not quiet:
            logger.error(f"\n{color.error('❌ JSON parsing error:')} {e}")
            logger.print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
            logger.print(
                "   Ensure your input is valid JSON. Example of valid format:",
                file=sys.stderr,
            )
            logger.print("   {", file=sys.stderr)
            logger.print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
            logger.print('     "tool_name": "Write",', file=sys.stderr)
            logger.print('     "tool_input": {', file=sys.stderr)
            logger.print('       "file_path": "example.py",', file=sys.stderr)
            logger.print('       "content": "print(\'Hello\')"', file=sys.stderr)
            logger.print("     }", file=sys.stderr)
            logger.print("   }", file=sys.stderr)
            logger.print("\n   Common issues:", file=sys.stderr)
            logger.print("   • Missing quotes around strings", file=sys.stderr)
            logger.print("   • Trailing commas after last item", file=sys.stderr)
            logger.print('   • Unescaped quotes in strings (use \\") ', file=sys.stderr)
            logger.print("   • Missing brackets or braces\n", file=sys.stderr)
        else:
            # Show minimal error even in quiet mode
            print(f"❌ JSON Parse Error: {e}", file=sys.stderr)
        return None, 1
    except Exception as e:
        logger.debug(f"Unexpected error reading input: {e}")
        if not quiet:
            logger.error(f"\n{color.error('❌ Error reading input:')} {e}")
            logger.print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
            logger.print("   • Ensure data is being piped to stdin", file=sys.stderr)
            logger.print("   • Example: echo '{...}' | antimon", file=sys.stderr)
            logger.print("   • Or: cat hook_data.json | antimon\n", file=sys.stderr)
        else:
            # Show minimal error even in quiet mode
            print(f"❌ Error reading input: {e}", file=sys.stderr)
        return None, 1


def _validate_required_fields(
    json_data: HookData, tool_name: str, color: ColorFormatter, quiet: bool
) -> int:
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
                    logger.error(
                        f"\n{color.error('❌ Validation error:')} Missing required field 'content' for {tool_name} tool"
                    )
                    logger.print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
                    logger.print(
                        "   The Write tool requires both 'file_path' and 'content' fields:",
                        file=sys.stderr,
                    )
                    logger.print("   {", file=sys.stderr)
                    logger.print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
                    logger.print('     "tool_name": "Write",', file=sys.stderr)
                    logger.print('     "tool_input": {', file=sys.stderr)
                    logger.print('       "file_path": "example.py",', file=sys.stderr)
                    logger.print('       "content": "file contents here"', file=sys.stderr)
                    logger.print("     }", file=sys.stderr)
                    logger.print("   }\n", file=sys.stderr)
                return 1
        elif tool_name in {"Edit", "MultiEdit"}:
            # Edit tools need either 'new_string' or both 'old_string' and 'new_string'
            if "new_string" not in tool_input:
                logger.error(
                    f"Missing required field 'new_string' for {tool_name} tool"
                )
                if not quiet:
                    logger.error(
                        f"\n❌ Validation error: Missing required field 'new_string' for {tool_name} tool"
                    )
                    logger.print("\n💡 How to fix:", file=sys.stderr)
                    logger.print(
                        f"   The {tool_name} tool requires 'old_string' and 'new_string' fields:",
                        file=sys.stderr,
                    )
                    logger.print("   {", file=sys.stderr)
                    logger.print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
                    logger.print(f'     "tool_name": "{tool_name}",', file=sys.stderr)
                    logger.print('     "tool_input": {', file=sys.stderr)
                    logger.print('       "file_path": "example.py",', file=sys.stderr)
                    logger.print('       "old_string": "text to replace",', file=sys.stderr)
                    logger.print('       "new_string": "replacement text"', file=sys.stderr)
                    logger.print("     }", file=sys.stderr)
                    logger.print("   }\n", file=sys.stderr)
                return 1

    # Validate required fields for Read tool
    if tool_name == "Read" and "file_path" not in tool_input:
        logger.error(f"Missing required field 'file_path' for {tool_name} tool")
        if not quiet:
            logger.error(
                f"\n{color.error('❌ Validation error:')} Missing required field 'file_path' for {tool_name} tool"
            )
            logger.print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
            logger.print("   The Read tool requires a 'file_path' field:", file=sys.stderr)
            logger.print("   {", file=sys.stderr)
            logger.print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
            logger.print('     "tool_name": "Read",', file=sys.stderr)
            logger.print('     "tool_input": {', file=sys.stderr)
            logger.print('       "file_path": "/path/to/file"', file=sys.stderr)
            logger.print("     }", file=sys.stderr)
            logger.print("   }\n", file=sys.stderr)
        return 1

    # Validate required fields for Bash tool
    if tool_name == "Bash" and "command" not in tool_input:
        logger.error(f"Missing required field 'command' for {tool_name} tool")
        if not quiet:
            logger.error(
                f"\n{color.error('❌ Validation error:')} Missing required field 'command' for {tool_name} tool"
            )
            logger.print(f"\n{color.info('💡 How to fix:')}", file=sys.stderr)
            logger.print("   The Bash tool requires a 'command' field:", file=sys.stderr)
            logger.print("   {", file=sys.stderr)
            logger.print('     "hook_event_name": "PreToolUse",', file=sys.stderr)
            logger.print('     "tool_name": "Bash",', file=sys.stderr)
            logger.print('     "tool_input": {', file=sys.stderr)
            logger.print('       "command": "ls -la"', file=sys.stderr)
            logger.print("     }", file=sys.stderr)
            logger.print("   }\n", file=sys.stderr)
        return 1

    return 0


def _display_security_issues(
    issues: list[str],
    stats: dict[str, int],
    json_data: HookData,
    tool_name: str,
    color: ColorFormatter,
    verbose: bool,
    quiet: bool,
    no_color: bool = False,
    dry_run: bool = False,
) -> None:
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

    config = get_runtime_config()
    brief = config.brief

    # Create error context handler
    error_context = ErrorContext(no_color=no_color)

    # Always show security issues, even in quiet mode
    if dry_run:
        logger.warning(
            f"\n{color.warning('🔍 DRY RUN - Security issues that would be detected:')}"
        )
    else:
        logger.error(f"\n{color.error('⚠️  Security issues detected:')}")

    # Structured output for issues
    if brief:
        # Brief mode: show only essential information
        for issue in issues:
            logger.print(f"  • {issue}", file=sys.stderr)
        logger.print("", file=sys.stderr)
        logger.print("💡 Run 'antimon --explain-last-error' for details", file=sys.stderr)
        # Show exit code documentation
        exit_code = 0 if dry_run else 2
        logger.print(
            f"\nExit code: {exit_code} ({'Preview only' if dry_run else 'Security issue detected'})",
            file=sys.stderr,
        )
    elif verbose and not quiet:
        logger.print("\n📊 Detection Results:", file=sys.stderr)
        logger.print(
            f"   File: {json_data.get('tool_input', {}).get('file_path', 'N/A')}",
            file=sys.stderr,
        )
        logger.print(f"   Tool: {tool_name}", file=sys.stderr)
        logger.print(
            f"   Summary: {stats['failed']} failed, {stats['passed']} passed, {stats['errors']} errors\n",
            file=sys.stderr,
        )
        logger.print("   Issues found:", file=sys.stderr)
        for i, issue in enumerate(issues, 1):
            logger.print(f"   [{i}] {issue}", file=sys.stderr)
            # Add context for each issue
            context = error_context.get_context_for_error(issue, json_data)
            if context:
                logger.print(f"\n{context}", file=sys.stderr)
    else:
        for issue in issues:
            logger.print(f"  • {color.format_security_issue(issue)}", file=sys.stderr)

        # Show context for the first issue in non-verbose mode
        if issues and not quiet:
            logger.print("", file=sys.stderr)  # Empty line
            context = error_context.get_context_for_error(issues[0], json_data)
            if context:
                logger.print(context, file=sys.stderr)

    if not quiet and not brief:
        if dry_run:
            logger.print("\n💡 DRY RUN Summary:", file=sys.stderr)
            logger.print("   • This is a preview of what would be blocked", file=sys.stderr)
            logger.print("   • No actual blocking occurred", file=sys.stderr)
            logger.print(
                "   • To actually block these operations, run without --dry-run",
                file=sys.stderr,
            )
            logger.print("   • To allow specific files, use --allow-file", file=sys.stderr)
            logger.print(
                "   • To disable specific detectors, use --disable-detector\n",
                file=sys.stderr,
            )
        else:
            logger.print("\n💡 How to proceed:", file=sys.stderr)
            logger.print("   1. Review the detected issues above", file=sys.stderr)
            logger.print(
                "   2. Run 'antimon --explain-last-error' for detailed explanations",
                file=sys.stderr,
            )
            logger.print("   3. If false positive, consider:", file=sys.stderr)
            logger.print(
                "      • Using environment variables instead of hardcoded values",
                file=sys.stderr,
            )
            logger.print(
                "      • Moving sensitive data to separate config files",
                file=sys.stderr,
            )
            logger.print(
                "      • Using --allow-file or --ignore-pattern options",
                file=sys.stderr,
            )
            logger.print("   4. For legitimate use cases, you can:", file=sys.stderr)
            logger.print(
                "      • Temporarily disable the hook in Claude Code settings",
                file=sys.stderr,
            )
            logger.print(
                f"      • Report false positives at: {ISSUE_TRACKER_URL}\n",
                file=sys.stderr,
            )



    # Always show error recovery hint for non-brief mode (Exit Code Documentation + Error Recovery Hints)
    if not quiet and not brief and not dry_run:
        logger.print("Exit code: 2 (Security issues detected)", file=sys.stderr)
        logger.print(
            "💡 For more information, run: antimon --explain-last-error\n",
            file=sys.stderr,
        )


def process_stdin(
    verbose: bool = False,
    quiet: bool = False,
    no_color: bool = False,
    output_format: str = "text",
) -> int:
    """
    Process JSON input from stdin and validate

    Args:
        verbose: Enable verbose output
        quiet: Suppress all output except errors
        no_color: Disable colored output

    Returns:
        Exit code (0=success, 1=parse error, 2=security issues)
    """
    import sys
    
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
        "LS",
        "Glob",
        "Grep",
        "NotebookRead",
        "WebFetch",
        "WebSearch",
        "TodoWrite",
        "exit_plan_mode",
    }

    tool_name = json_data.get("tool_name", "")

    # Validate required fields
    validation_result = _validate_required_fields(json_data, tool_name, color, quiet)
    if validation_result != 0:
        return validation_result

    # Provide feedback for non-code-editing tools
    if (
        tool_name not in code_editing_tools
        and tool_name not in special_validation_tools
    ):
        if tool_name in safe_tools:
            logger.info(f"Safe tool {tool_name} - no security validation needed")
            if verbose and not quiet:
                logger.info(
                    f"ℹ️  Tool '{tool_name}' is considered safe - no security validation performed"
                )
        elif tool_name:
            logger.info(f"Unknown tool {tool_name} - skipping validation")
            if verbose and not quiet:
                logger.info(
                    f"ℹ️  Unknown tool '{tool_name}' - no security validation performed"
                )
        else:
            logger.info("No tool name provided - skipping validation")
            if verbose and not quiet:
                logger.info(
                    "ℹ️  No tool specified - no security validation performed"
                )
        return 0

    # Get runtime config at the beginning
    config = get_runtime_config()

    # Validate code-editing tools
    has_issues, issues, stats = validate_hook_data(json_data, quiet=quiet, no_color=no_color)

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
            lines = issue.split("\n")
            essential_lines = []
            for line in lines:
                line_stripped = line.strip()
                # Keep main message, risk, suggestion, and allow-file hint
                if (
                    not line_stripped.startswith("Pattern matched:")
                    and not line_stripped.startswith("Type:")
                    and not line_stripped.startswith("Found:")
                ):
                    essential_lines.append(line)
            simplified_issues.append("\n".join(essential_lines))
        issues = simplified_issues

    if has_issues:
        # Get runtime config to check for dry run mode
        config = get_runtime_config()

        # Save the error for later explanation (even in dry run)
        save_last_error(issues, json_data)
        _display_security_issues(
            issues,
            stats,
            json_data,
            tool_name,
            color,
            verbose,
            quiet,
            no_color,
            dry_run=config.dry_run,
        )

        # In dry run mode, return success (0) instead of error (2)
        if config.dry_run:
            return 0
        else:
            return 2

    logger.info("Security validation passed")
    if config.show_stats or verbose:
        if not quiet:
            # Show detailed summary
            logger.print("\n📊 Detection Summary:", file=sys.stderr)
            logger.print(f"   • Total detectors run: {stats['total']}", file=sys.stderr)
            logger.print(f"   • Passed: {stats['passed']}", file=sys.stderr)
            logger.print(f"   • Failed: {stats['failed']}", file=sys.stderr)
            if stats["errors"] > 0:
                logger.print(f"   • Errors: {stats['errors']}", file=sys.stderr)

            # Show timing information if --stats is used
            if config.show_stats and "total_time" in stats:
                logger.print("\n⏱️  Performance Metrics:", file=sys.stderr)
                logger.print(f"   • Total time: {stats['total_time']:.3f}s", file=sys.stderr)
                if "content_size" in stats and stats["content_size"] > 0:
                    logger.print(
                        f"   • Content size: {stats['content_size']:,} bytes",
                        file=sys.stderr,
                    )
                if "patterns_checked" in stats:
                    logger.print(
                        f"   • Patterns checked: {stats['patterns_checked']}",
                        file=sys.stderr,
                    )

                # Show individual detector times
                if stats.get("detector_times"):
                    logger.print("\n⚡ Detector Performance:", file=sys.stderr)
                    sorted_times = sorted(
                        stats["detector_times"].items(),
                        key=lambda x: x[1],
                        reverse=True,
                    )
                    for detector_name, detector_time in sorted_times:
                        logger.print(
                            f"   • {detector_name}: {detector_time:.3f}s",
                            file=sys.stderr,
                        )
    elif not quiet:
        # Enhanced success message showing what was checked
        operation_info = []
        if tool_name:
            operation_info.append(f"Tool: {tool_name}")
        if json_data and "tool_input" in json_data:
            tool_input = json_data["tool_input"]
            if isinstance(tool_input, dict):
                if "file_path" in tool_input:
                    operation_info.append(f"File: {tool_input['file_path']}")
                if "content" in tool_input and isinstance(tool_input["content"], str):
                    content_size = len(tool_input["content"])
                    operation_info.append(f"Content: {content_size:,} bytes")

        logger.info(
            f"\n✅ {color.success('Success:')} No security issues found"
        )
        if operation_info:
            for info in operation_info:
                logger.print(f"   • {info}", file=sys.stderr)
        logger.print(
            f"   • Checks performed: {stats['total']} security detectors",
            file=sys.stderr,
        )
    return 0


def check_files_batch(
    file_pattern: str,
    verbose: bool = False,
    quiet: bool = False,
    no_color: bool = False,
    output_format: str = "text",
) -> int:
    """
    Check multiple files matching a glob pattern.

    Args:
        file_pattern: Glob pattern to match files (e.g., 'src/**/*.py')
        verbose: Enable verbose output
        quiet: Suppress all output except errors
        no_color: Disable colored output

    Returns:
        Exit code (0=success, 1=error, 2=security issues)
    """
    # Initialize color formatter
    color = ColorFormatter(use_color=not no_color)

    # Find all files matching the pattern
    files = glob.glob(file_pattern, recursive=True)

    if not files:
        if not quiet:
            logger.warning(
                f"\n{color.warning('⚠️  Warning:')} No files found matching pattern: {file_pattern}"
            )
        return 0

    # Filter out directories
    files = [f for f in files if os.path.isfile(f)]

    if not files:
        if not quiet:
            logger.warning(
                f"\n{color.warning('⚠️  Warning:')} No files found matching pattern: {file_pattern}"
            )
        return 0

    if not quiet:
        logger.print(
            f"\n🔍 Checking {len(files)} file{'s' if len(files) != 1 else ''} matching pattern: {file_pattern}",
            file=sys.stderr,
        )

    # Track overall results
    total_issues = 0
    files_with_issues = []
    total_start_time = time.time()

    # Check each file
    for i, file_path in enumerate(files, 1):
        if not quiet:
            logger.print(f"\n[{i}/{len(files)}] Checking: {file_path}", file=sys.stderr)

        # Check the file
        # For batch mode, always suppress individual file messages except errors
        result = check_file_directly(
            file_path, verbose=verbose, quiet=not quiet, no_color=no_color
        )

        if result == 2:  # Security issues found
            total_issues += 1
            files_with_issues.append(file_path)
        elif result == 1:  # Error
            if not quiet:
                logger.error(f"   {color.error('⚠️  Error checking file')}")

    # Show summary
    total_time = time.time() - total_start_time

    if output_format == "json":
        # JSON output
        result = {
            "pattern": file_pattern,
            "files_checked": len(files),
            "files_with_issues": len(files_with_issues),
            "total_time": total_time,
            "issues": files_with_issues,
            "success": len(files_with_issues) == 0,
        }
        logger.print(json.dumps(result, indent=2), file=sys.stdout)
    elif not quiet:
        # Text output
        logger.print(f"\n{'='*60}", file=sys.stderr)
        logger.print("📊 Batch Check Summary", file=sys.stderr)
        logger.print(f"{'='*60}", file=sys.stderr)
        logger.print(f"   • Files checked: {len(files)}", file=sys.stderr)
        logger.print(f"   • Files with issues: {len(files_with_issues)}", file=sys.stderr)
        logger.print(f"   • Total time: {total_time:.2f}s", file=sys.stderr)

        if files_with_issues:
            logger.error(f"\n{color.error('❌ Files with security issues:')}")
            for file_path in files_with_issues:
                logger.print(f"   • {file_path}", file=sys.stderr)
        else:
            logger.info(
                f"\n{color.success('✅ All files passed security checks!')}"
            )

    # Return appropriate exit code
    return 2 if total_issues > 0 else 0


def check_file_directly(
    file_path: str,
    verbose: bool = False,
    quiet: bool = False,
    no_color: bool = False,
    output_format: str = "text",
) -> int:
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
    # Initialize color formatter
    color = ColorFormatter(use_color=not no_color)

    # Check if file exists
    if not os.path.exists(file_path):
        if not quiet:
            logger.error(
                f"\n{color.error('❌ Error:')} File not found: {file_path}"
            )
        return 1

    # Read file content
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        if not quiet:
            logger.error(f"\n{color.error('❌ Error reading file:')} {e}")
        return 1

    # Create JSON data for validation
    json_data: HookData = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": os.path.abspath(file_path), "content": content},
    }

    # Get runtime config at the beginning
    config = get_runtime_config()

    # Validate the file
    has_issues, issues, stats = validate_hook_data(json_data, quiet=quiet, no_color=no_color)

    if has_issues:
        # Get runtime config to check for dry run mode
        config = get_runtime_config()

        # Save the error for later explanation
        save_last_error(issues, json_data)
        _display_security_issues(
            issues,
            stats,
            json_data,
            "Write",
            color,
            verbose,
            quiet,
            no_color,
            dry_run=config.dry_run,
        )

        # In dry run mode, return success (0) instead of error (2)
        if config.dry_run:
            return 0
        else:
            return 2

    if config.show_stats or verbose:
        if not quiet:
            logger.info(
                f"\n✅ File '{file_path}' passed all security checks"
            )
            logger.print("\n📊 Detection Summary:", file=sys.stderr)
            logger.print(f"   • Total detectors run: {stats['total']}", file=sys.stderr)
            logger.print(f"   • Passed: {stats['passed']}", file=sys.stderr)
            logger.print(f"   • Failed: {stats['failed']}", file=sys.stderr)
            if stats["errors"] > 0:
                logger.print(f"   • Errors: {stats['errors']}", file=sys.stderr)

            # Show timing information if --stats is used
            if config.show_stats and "total_time" in stats:
                logger.print("\n⏱️  Performance Metrics:", file=sys.stderr)
                logger.print(f"   • Total time: {stats['total_time']:.3f}s", file=sys.stderr)
                logger.print(f"   • File: {file_path}", file=sys.stderr)
                if "content_size" in stats and stats["content_size"] > 0:
                    logger.print(
                        f"   • Content size: {stats['content_size']:,} bytes",
                        file=sys.stderr,
                    )
                if "patterns_checked" in stats:
                    logger.print(
                        f"   • Patterns checked: {stats['patterns_checked']}",
                        file=sys.stderr,
                    )

                # Show individual detector times
                if stats.get("detector_times"):
                    logger.print("\n⚡ Detector Performance:", file=sys.stderr)
                    sorted_times = sorted(
                        stats["detector_times"].items(),
                        key=lambda x: x[1],
                        reverse=True,
                    )
                    for detector_name, detector_time in sorted_times:
                        logger.print(
                            f"   • {detector_name}: {detector_time:.3f}s",
                            file=sys.stderr,
                        )
    elif not quiet:
        # Get file info for better user feedback
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        logger.info(
            f"\n✅ {color.success('Success:')} No security issues found"
        )
        logger.print(f"   • File: {file_path}", file=sys.stderr)
        logger.print(
            f"   • Size: {file_size_kb:.1f} KB ({file_size:,} bytes)", file=sys.stderr
        )
        logger.print(
            f"   • Checks performed: {stats['total']} security detectors",
            file=sys.stderr,
        )

    return 0


def check_content_directly(
    content: str,
    file_name: str = "stdin",
    verbose: bool = False,
    quiet: bool = False,
    no_color: bool = False,
    output_format: str = "text",
) -> int:
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
        "tool_input": {"file_path": file_name, "content": content},
    }

    # Get runtime config at the beginning
    config = get_runtime_config()

    # Validate the content
    has_issues, issues, stats = validate_hook_data(json_data, quiet=quiet, no_color=no_color)

    if has_issues:
        # Get runtime config to check for dry run mode
        config = get_runtime_config()

        # Save the error for later explanation
        save_last_error(issues, json_data)
        _display_security_issues(
            issues,
            stats,
            json_data,
            "Write",
            color,
            verbose,
            quiet,
            no_color,
            dry_run=config.dry_run,
        )

        # In dry run mode, return success (0) instead of error (2)
        if config.dry_run:
            return 0
        else:
            return 2

    if config.show_stats or verbose:
        if not quiet:
            logger.info("\n✅ Content passed all security checks")
            logger.print("\n📊 Detection Summary:", file=sys.stderr)
            logger.print(f"   • Total detectors run: {stats['total']}", file=sys.stderr)
            logger.print(f"   • Passed: {stats['passed']}", file=sys.stderr)
            logger.print(f"   • Failed: {stats['failed']}", file=sys.stderr)
            if stats["errors"] > 0:
                logger.print(f"   • Errors: {stats['errors']}", file=sys.stderr)

            # Show timing information if --stats is used
            if config.show_stats and "total_time" in stats:
                logger.print("\n⏱️  Performance Metrics:", file=sys.stderr)
                logger.print(f"   • Total time: {stats['total_time']:.3f}s", file=sys.stderr)
                if "content_size" in stats and stats["content_size"] > 0:
                    logger.print(
                        f"   • Content size: {stats['content_size']:,} bytes",
                        file=sys.stderr,
                    )
                if "patterns_checked" in stats:
                    logger.print(
                        f"   • Patterns checked: {stats['patterns_checked']}",
                        file=sys.stderr,
                    )

                # Show individual detector times
                if stats.get("detector_times"):
                    logger.print("\n⚡ Detector Performance:", file=sys.stderr)
                    sorted_times = sorted(
                        stats["detector_times"].items(),
                        key=lambda x: x[1],
                        reverse=True,
                    )
                    for detector_name, detector_time in sorted_times:
                        logger.print(
                            f"   • {detector_name}: {detector_time:.3f}s",
                            file=sys.stderr,
                        )
    elif not quiet:
        # Get content info for better user feedback
        content_lines = content.count("\n") + 1 if content else 0
        content_size = len(content.encode("utf-8"))
        content_size_kb = content_size / 1024
        logger.info(
            f"\n✅ {color.success('Success:')} No security issues found"
        )
        logger.print(
            f"   • Content size: {content_size_kb:.1f} KB ({content_size:,} bytes)",
            file=sys.stderr,
        )
        logger.print(f"   • Lines: {content_lines:,}", file=sys.stderr)
        logger.print(
            f"   • Checks performed: {stats['total']} security detectors",
            file=sys.stderr,
        )

    return 0
