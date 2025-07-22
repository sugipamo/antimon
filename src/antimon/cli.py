# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Command-line interface for antimon
"""

import argparse
import sys

from . import __version__
from .core import (
    check_content_directly,
    check_file_directly,
    check_files_batch,
    process_stdin,
)
from .demo import run_demo
from .error_context import show_error_help
from .first_run import (
    is_first_run,
    mark_first_run_complete,
    run_interactive_setup,
    show_first_run_guide,
    show_first_run_guide_interactive,
    suggest_claude_code_setup,
)
from .last_error import explain_last_error
from .logging_config import setup_logging
from .pattern_test import run_pattern_test
from .runtime_config import RuntimeConfig, set_runtime_config
from .self_test import run_self_test
from .setup_claude_code import setup_claude_code_integration
from .status import show_status
from .watch import watch_directory


def main(argv: list[str] | None = None) -> int:
    """
    Main CLI entry point

    Args:
        argv: Command line arguments (defaults to sys.argv)

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        prog="antimon",
        description="Security validation tool for AI coding assistants that detects potentially dangerous operations and prohibited patterns in code modifications.",
        epilog="""
Examples:
  # Validate JSON input from stdin
  echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "hello.py", "content": "print(\\"Hello\\")"}}' | antimon

  # Use with a file
  cat hook_data.json | antimon

  # Enable verbose logging
  cat hook_data.json | antimon --verbose

  # Use as a Claude Code hook (add to settings.json)
  {"hooks": {"PreToolUse": "antimon"}}

Exit codes:
  0 - No security issues detected (or non-code-editing operation)
  1 - JSON parsing error or internal error
  2 - Security issues detected

For more information: https://github.com/antimon-security/antimon
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file (coming in v0.3.0). Will allow custom patterns and detector settings.",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output with detailed logging of each detector's execution",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress all output except errors. Only display security issues when detected.",
    )

    parser.add_argument(
        "--brief",
        "-b",
        action="store_true",
        help="Show concise security reports without detailed explanations. Useful for CI/CD pipelines.",
    )

    parser.add_argument(
        "--autofix",
        action="store_true",
        help="Show auto-fix suggestions for detected security issues. Provides code snippets to fix common problems.",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run a self-test to verify antimon is working correctly. Useful after installation.",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output. Useful for CI/CD pipelines or when terminal doesn't support colors.",
    )

    parser.add_argument(
        "--quickstart",
        action="store_true",
        help="Show the quick start guide and examples. Useful for new users.",
    )

    parser.add_argument(
        "--help-errors",
        action="store_true",
        help="Show help for dealing with antimon errors and blocks.",
    )

    parser.add_argument(
        "--ignore-pattern",
        action="append",
        help="Add file pattern to ignore (can be used multiple times). Example: --ignore-pattern '*.test.py' --ignore-pattern 'examples/*'",
    )

    parser.add_argument(
        "--allow-file",
        action="append",
        help="Allow specific file path or glob pattern (can be used multiple times). "
        "Examples: --allow-file /home/user/.config/app.conf, --allow-file '*.env', "
        "--allow-file 'config/*.json', --allow-file '**/*.secret'",
    )

    parser.add_argument(
        "--disable-detector",
        action="append",
        choices=[
            "filenames",
            "llm_api",
            "api_key",
            "docker",
            "localhost",
            "claude_antipatterns",
            "bash",
            "read",
        ],
        help="Disable specific detector (can be used multiple times). Example: --disable-detector api_key --disable-detector localhost",
    )

    parser.add_argument(
        "--explain-last-error",
        action="store_true",
        help="Show detailed explanation of the last error that occurred. Run this after antimon blocks an operation.",
    )

    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run the interactive setup wizard to configure antimon with your tools.",
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run interactive demo to see antimon's detection capabilities in action.",
    )

    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="When used with --demo, runs a non-interactive automated demonstration.",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current configuration, enabled detectors, and exclusion patterns.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be detected without blocking. Shows all detections that would occur.",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show detailed statistics after checks (detector counts, pass/fail rates).",
    )

    parser.add_argument(
        "--check-file",
        type=str,
        help="Check a specific file directly without JSON input. Example: antimon --check-file config.py",
    )

    parser.add_argument(
        "--check-content",
        type=str,
        help="Check content directly without JSON input. Example: antimon --check-content 'api_key = \"sk-123\"'",
    )

    parser.add_argument(
        "--check-files",
        type=str,
        help="Check multiple files using glob pattern. Example: antimon --check-files 'src/**/*.py'",
    )

    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format for results (default: text). JSON format is useful for CI/CD integration.",
    )

    parser.add_argument(
        "--setup-claude-code",
        action="store_true",
        help="Interactive setup wizard to configure antimon with Claude Code. Automatically configures the PreToolUse hook.",
    )

    parser.add_argument(
        "--watch",
        type=str,
        metavar="DIRECTORY",
        help="Watch a directory for file changes and re-check modified files automatically. Example: antimon --watch src/",
    )

    parser.add_argument(
        "--test-pattern",
        type=str,
        metavar="PATTERN",
        help="Test a pattern against antimon detectors to see if it would be blocked. Example: antimon --test-pattern 'api_key = \"sk-123\"'",
    )

    parser.add_argument(
        "--pattern-examples",
        action="store_true",
        help="Show example patterns that would trigger each detector. Useful for understanding what antimon blocks.",
    )

    parser.add_argument(
        "--detector",
        type=str,
        choices=["api_key", "llm_api", "docker", "localhost", "filenames"],
        help="When used with --test-pattern, test against a specific detector only.",
    )

    args = parser.parse_args(argv)

    # Check if this is the first run (before running test)
    first_run = is_first_run()

    # Create and set runtime configuration
    runtime_config = RuntimeConfig.from_args(args)
    set_runtime_config(runtime_config)

    # Show runtime config in verbose mode
    if args.verbose and not args.quiet:
        config_summary = runtime_config.get_summary()
        if config_summary:
            print("\n📋 Runtime Configuration:", file=sys.stderr)
            for line in config_summary:
                print(f"   • {line}", file=sys.stderr)
            print("", file=sys.stderr)  # Empty line

    # Show quickstart guide if requested
    if args.quickstart:
        show_first_run_guide(no_color=args.no_color, is_quickstart=True)
        suggest_claude_code_setup(no_color=args.no_color)
        if first_run:
            mark_first_run_complete()
        return 0

    # Show error help if requested
    if args.help_errors:
        show_error_help(no_color=args.no_color)
        if first_run:
            mark_first_run_complete()
        return 0

    # Explain last error if requested
    if args.explain_last_error:
        explain_last_error(no_color=args.no_color)
        if first_run:
            mark_first_run_complete()
        return 0

    # Run setup wizard if requested
    if args.setup:
        run_interactive_setup(no_color=args.no_color)
        if first_run:
            mark_first_run_complete()
        return 0

    # Run demo if requested
    if args.demo:
        if first_run:
            mark_first_run_complete()
        run_demo(non_interactive=args.non_interactive)
        return 0

    # Show status if requested
    if args.status:
        if first_run:
            mark_first_run_complete()
        show_status(no_color=args.no_color)
        return 0

    # Run self-test if requested
    if args.test:
        if first_run:
            mark_first_run_complete()
        return run_self_test(verbose=args.verbose)

    # Show first-run guide if needed
    if first_run and not args.quiet:
        show_first_run_guide_interactive(no_color=args.no_color)
        mark_first_run_complete()

    # Check for conflicting options
    if args.verbose and args.quiet:
        print("\n⚠️  Cannot use --verbose and --quiet together", file=sys.stderr)
        return 1

    # Setup logging
    setup_logging(verbose=args.verbose, quiet=args.quiet)

    if args.config and not args.quiet:
        print("\n⚠️  Configuration file support is not yet available", file=sys.stderr)
        print(
            "   This feature is planned for v0.3.0 and will include:", file=sys.stderr
        )
        print("   • Custom detection patterns", file=sys.stderr)
        print("   • Project-specific whitelists", file=sys.stderr)
        print("   • Detector sensitivity tuning", file=sys.stderr)
        print("   • Team-wide configuration sharing", file=sys.stderr)
        print("\n📌 For now, you can use:", file=sys.stderr)
        print("   • --allow-file: Allow specific files or patterns", file=sys.stderr)
        print("   • --disable-detector: Disable specific detectors", file=sys.stderr)
        print("   • --ignore-pattern: Ignore files matching patterns", file=sys.stderr)
        print(
            "\n💡 Example: antimon --allow-file '*.env' --disable-detector api_key\n",
            file=sys.stderr,
        )

    # Handle direct file checking
    if args.check_file:
        if first_run:
            mark_first_run_complete()
        return check_file_directly(
            args.check_file,
            verbose=args.verbose,
            quiet=args.quiet,
            no_color=args.no_color,
            output_format=args.output_format,
        )

    # Handle direct content checking
    if args.check_content:
        if first_run:
            mark_first_run_complete()
        return check_content_directly(
            args.check_content,
            verbose=args.verbose,
            quiet=args.quiet,
            no_color=args.no_color,
            output_format=args.output_format,
        )

    # Handle batch file checking
    if args.check_files:
        if first_run:
            mark_first_run_complete()
        return check_files_batch(
            args.check_files,
            verbose=args.verbose,
            quiet=args.quiet,
            no_color=args.no_color,
            output_format=args.output_format,
        )

    # Handle Claude Code setup
    if args.setup_claude_code:
        if first_run:
            mark_first_run_complete()
        success = setup_claude_code_integration(no_color=args.no_color)
        return 0 if success else 1

    # Handle watch mode
    if args.watch:
        if first_run:
            mark_first_run_complete()
        return watch_directory(
            args.watch,
            verbose=args.verbose,
            quiet=args.quiet,
            no_color=args.no_color,
            output_format=args.output_format,
        )

    # Handle pattern testing
    if args.test_pattern or args.pattern_examples:
        if first_run:
            mark_first_run_complete()
        return run_pattern_test(
            pattern=args.test_pattern,
            detector_type=args.detector,
            show_examples=args.pattern_examples,
            verbose=args.verbose,
            no_color=args.no_color,
        )

    return process_stdin(
        verbose=args.verbose,
        quiet=args.quiet,
        no_color=args.no_color,
        output_format=args.output_format,
    )


if __name__ == "__main__":
    sys.exit(main())
