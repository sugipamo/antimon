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

    args = parser.parse_args(argv)

    # Setup logging
    setup_logging(verbose=args.verbose)

    if args.config:
        print("\n⚠️  Configuration file support coming in v0.3.0", file=sys.stderr)
        print("   This will allow you to:", file=sys.stderr)
        print("   • Define custom detection patterns", file=sys.stderr)
        print("   • Whitelist specific files or patterns", file=sys.stderr)
        print("   • Customize detector sensitivity", file=sys.stderr)
        print("   • Add project-specific rules\n", file=sys.stderr)

    return process_stdin(verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
