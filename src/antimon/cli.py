# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Command-line interface for antimon
"""

import argparse
import os
import sys

from . import __version__
from .core import process_stdin
from .setup_claude_code import setup_claude_code_integration
from .color_utils import ColorFormatter
from .config import create_sample_config, load_config
from .pattern_detector import PatternDetector
from .ai_detector import AIDetector
from .help_commands import show_api_setup_help


def list_detectors(no_color: bool = False) -> None:
    """List all available security detectors"""
    color = ColorFormatter(use_color=not no_color)
    
    print(f"\n{color.header('🛡️  Available Security Detectors')}")
    print("=" * 50)
    
    # Load configuration to show actual configured detectors
    try:
        config = load_config()
        
        # List pattern-based detectors
        if config.patterns:
            print(f"\n{color.info('Pattern-based Detectors:')}")
            for pattern_name, pattern_config in config.patterns.items():
                status = color.success("enabled") if pattern_config.enabled else color.warning("disabled")
                print(f"\n  • {color.info(pattern_name)} ({status})")
                if pattern_config.description:
                    print(f"    {pattern_config.description}")
        
        # List AI-powered detectors
        if config.ai_detectors:
            print(f"\n{color.info('AI-powered Detectors:')}")
            for ai_name, ai_config in config.ai_detectors.items():
                status = color.success("enabled") if ai_config.enabled else color.warning("disabled")
                print(f"\n  • {color.info(ai_name)} ({status})")
                if ai_config.description:
                    print(f"    {ai_config.description}")
                print(f"    Model: {ai_config.model}")
        
        if not config.patterns and not config.ai_detectors:
            print(f"\n{color.warning('No detectors configured.')}")
            print(f"Create a configuration file with: {color.code('antimon config')}")
        
    except Exception as e:
        print(f"\n{color.error('Error loading configuration:')} {e}")
        print(f"Create a configuration file with: {color.code('antimon config')}")
    
    print(f"\n{color.info('Usage:')}")
    print("  Detectors are configured in antimon.toml")
    print("  Use 'antimon config' to create a sample configuration")
    print("  Use 'antimon list --patterns' to see pattern details")


def list_patterns(no_color: bool = False) -> None:
    """List configured patterns from config file"""
    color = ColorFormatter(use_color=not no_color)
    
    try:
        detector = PatternDetector()
        enabled_patterns = detector.get_enabled_patterns()
        all_patterns = list(detector.config.patterns.keys())
        
        print(f"\n{color.header('📋 Configured Patterns')}")
        print("=" * 50)
        
        if not all_patterns:
            print(f"\n{color.warning('No patterns configured. Create a config file with:')}")
            print(f"  {color.code('antimon --create-config')}")
            return
        
        for pattern_name in all_patterns:
            pattern_config = detector.get_pattern_info(pattern_name)
            status = color.success("✅ enabled") if pattern_name in enabled_patterns else color.warning("❌ disabled")
            
            print(f"\n{color.info(f'• {pattern_name}')} ({status})")
            if pattern_config.description:
                print(f"  {pattern_config.description}")
            
            # Show pattern counts
            content_count = len(pattern_config.content_patterns)
            file_count = len(pattern_config.file_patterns)
            import_count = len(pattern_config.import_patterns)
            
            if content_count:
                print(f"  Content patterns: {content_count}")
            if file_count:
                print(f"  File patterns: {file_count}")
            if import_count:
                print(f"  Import patterns: {import_count}")
        
        print(f"\n{color.info('Total:')} {len(enabled_patterns)}/{len(all_patterns)} patterns enabled")
        
    except Exception as e:
        print(f"{color.error('Error loading patterns:')} {e}")


def test_ai_detector(detector_name: str, no_color: bool = False) -> int:
    """Test an AI detector with sample content"""
    color = ColorFormatter(use_color=not no_color)
    
    # Load config
    config = load_config()
    
    if detector_name not in config.ai_detectors:
        print(f"{color.error('❌ AI detector not found:')} {detector_name}")
        print(f"\n{color.info('Available AI detectors:')}")
        for name in config.ai_detectors:
            print(f"  • {name}")
        return 1
    
    detector_config = config.ai_detectors[detector_name]
    
    if not detector_config.enabled:
        print(f"{color.warning('⚠️  Detector is disabled in config')}")
        print(f"Enable it by setting: ai_detectors.{detector_name}.enabled = true")
        return 1
    
    # Sample code for testing
    sample_code = '''
# Sample code for testing
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)
    
api_key = "sk-1234567890abcdef"
'''
    
    print(f"\n{color.header(f'🧪 Testing AI Detector: {detector_name}')}")
    print("=" * 50)
    print(f"\n{color.info('Configuration:')}")
    print(f"  Model: {detector_config.model}")
    print(f"  Temperature: {detector_config.temperature}")
    print(f"  Max tokens: {detector_config.max_tokens}")
    print(f"\n{color.info('Prompt:')}")
    print(f"  {detector_config.prompt}")
    print(f"\n{color.info('Testing with sample code...')}")
    
    # Create detector
    api_key = os.environ.get(detector_config.api_key_env)
    if not api_key:
        print(f"\n{color.error(f'❌ API key not found in environment: {detector_config.api_key_env}')}")
        print(f"Set it with: export {detector_config.api_key_env}='your-api-key'")
        return 1
    
    detector = AIDetector(api_key=api_key, api_base=detector_config.api_base)
    
    # Run detection
    result = detector.detect(
        content=sample_code,
        prompt=detector_config.prompt,
        model=detector_config.model,
        temperature=detector_config.temperature,
        max_tokens=detector_config.max_tokens
    )
    
    print(f"\n{color.header('Results:')}")
    if result.detected:
        print(f"{color.error(f'⚠️  Issue detected: {result.message}')}")
        print(f"Severity: {result.severity}")
    else:
        if result.severity == "error":
            print(f"{color.error(f'❌ {result.message}')}")
        else:
            print(f"{color.success('✅ No issues detected')}")
            print(f"Message: {result.message}")
    
    return 0 if result.severity != "error" else 1


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        prog="antimon",
        description="Security validation tool for AI coding assistants.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )

    # init command (replaces --setup-claude-code)
    init_parser = subparsers.add_parser(
        "init",
        help="Setup wizard to configure antimon with Claude Code",
        description="Initialize antimon integration with Claude Code"
    )

    # list command (replaces --list-detectors and --list-patterns)
    list_parser = subparsers.add_parser(
        "list",
        help="List available security detectors or configured patterns",
        description="List available security detectors or configured patterns"
    )
    list_parser.add_argument(
        "--patterns",
        action="store_true",
        help="List configured patterns instead of detectors"
    )

    # config command (replaces --create-config)
    config_parser = subparsers.add_parser(
        "config",
        help="Create sample configuration file",
        description="Create a sample antimon.toml configuration file"
    )
    config_parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default="./antimon.toml",
        help="Path for the configuration file (default: ./antimon.toml)"
    )

    # test command (replaces --test-ai-detector)
    test_parser = subparsers.add_parser(
        "test",
        help="Test an AI detector with sample content",
        description="Test an AI detector to verify configuration"
    )
    test_parser.add_argument(
        "detector",
        type=str,
        help="Name of the AI detector to test"
    )

    # help command for specific topics
    help_parser = subparsers.add_parser(
        "help",
        help="Show help for specific topics",
        description="Get detailed help for various antimon features"
    )
    help_parser.add_argument(
        "topic",
        type=str,
        choices=["api-setup"],
        help="Help topic to display"
    )

    return parser


def handle_command(args: argparse.Namespace) -> int:
    """Route to appropriate command handler"""
    if args.command == "init":
        success = setup_claude_code_integration(no_color=args.no_color)
        return 0 if success else 1

    elif args.command == "list":
        if args.patterns:
            list_patterns(no_color=args.no_color)
        else:
            list_detectors(no_color=args.no_color)
        return 0

    elif args.command == "config":
        color = ColorFormatter(use_color=not args.no_color)
        try:
            create_sample_config(args.path)
            print(f"{color.success('✅ Configuration file created:')} {args.path}")
            print(f"{color.info('Edit the file to customize detection patterns.')}")
            return 0
        except FileExistsError:
            print(f"{color.error('❌ Configuration file already exists:')} {args.path}")
            return 1
        except PermissionError:
            print(f"{color.error('❌ Permission denied:')} {args.path}")
            return 1
        except OSError as e:
            print(f"{color.error('❌ Failed to create config file:')} {e}")
            return 1

    elif args.command == "test":
        return test_ai_detector(args.detector, no_color=args.no_color)
    
    elif args.command == "help":
        if args.topic == "api-setup":
            show_api_setup_help(no_color=args.no_color)
            return 0

    return 1


def main(argv: list[str] | None = None) -> int:
    """
    Main CLI entry point

    Args:
        argv: Command line arguments (defaults to sys.argv)

    Returns:
        Exit code
    """
    parser = create_argument_parser()
    args = parser.parse_args(argv)

    # Handle subcommands
    if args.command:
        return handle_command(args)

    # If stdin is available (hook data), process it
    if not sys.stdin.isatty():
        return process_stdin(
            verbose=False,
            quiet=False,  # Show detailed errors for better UX
            no_color=args.no_color,
            output_format="text"
        )

    # If no specific command and no stdin, show help
    parser.print_help()
    return 1