"""
Command-line interface for antimon
"""

import sys
import argparse
from typing import Optional, List

from . import __version__
from .core import process_stdin


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main CLI entry point

    Args:
        argv: Command line arguments (defaults to sys.argv)

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        prog="antimon", description="Security validation tool for AI coding assistants"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--config", type=str, help="Path to configuration file (not yet implemented)"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args(argv)

    if args.config:
        print("Configuration file support coming in v0.3.0", file=sys.stderr)

    return process_stdin()


if __name__ == "__main__":
    sys.exit(main())
