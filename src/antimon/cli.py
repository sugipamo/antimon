# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Command-line interface for antimon
"""

import argparse
import sys

from . import __version__
from .core import process_stdin
from .logging_config import setup_logging
from .self_test import run_self_test
from .first_run import (
    is_first_run,
    mark_first_run_complete,
    show_first_run_guide,
    suggest_claude_code_setup,
    show_first_run_guide_interactive,
    run_interactive_setup,
)
from .error_context import show_error_help
from .runtime_config import RuntimeConfig, set_runtime_config
from .last_error import explain_last_error
from .demo import run_demo


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

For more information: https://github.com/yourusername/antimon
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
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
        choices=["filenames", "llm_api", "api_key", "docker", "localhost", "claude_antipatterns", "bash", "read"],
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
        show_first_run_guide(no_color=args.no_color)
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
        run_demo()
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
        print("\n⚠️  Configuration file support coming in v0.3.0", file=sys.stderr)
        print("   This will allow you to:", file=sys.stderr)
        print("   • Define custom detection patterns", file=sys.stderr)
        print("   • Whitelist specific files or patterns", file=sys.stderr)
        print("   • Customize detector sensitivity", file=sys.stderr)
        print("   • Add project-specific rules\n", file=sys.stderr)

    return process_stdin(verbose=args.verbose, quiet=args.quiet, no_color=args.no_color)


if __name__ == "__main__":
    sys.exit(main())
