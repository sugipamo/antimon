# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
First-run detection and setup guide for antimon
"""

import os
import sys
from pathlib import Path
from typing import Optional

from .color_utils import apply_color, Colors


def get_config_dir() -> Path:
    """Get the configuration directory for antimon."""
    if sys.platform == "win32":
        config_dir = Path(os.environ.get("APPDATA", "~")) / "antimon"
    else:
        config_dir = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")) / "antimon"
    
    return config_dir.expanduser()


def is_first_run() -> bool:
    """Check if this is the first run of antimon."""
    config_dir = get_config_dir()
    marker_file = config_dir / ".first_run_complete"
    return not marker_file.exists()


def mark_first_run_complete() -> None:
    """Mark that the first run has been completed."""
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    marker_file = config_dir / ".first_run_complete"
    marker_file.touch()


def show_first_run_guide(no_color: bool = False) -> None:
    """Display the first-run guide for new users."""
    print()
    print(apply_color("🎉 Welcome to antimon!", Colors.HEADER, no_color))
    print(apply_color("=" * 50, Colors.HEADER, no_color))
    print()
    print("antimon is a security validation tool for AI coding assistants.")
    print("It helps prevent potentially dangerous operations in your code.")
    print()
    
    print(apply_color("📋 Quick Start:", Colors.OKBLUE, no_color))
    print()
    print("1. " + apply_color("Test antimon is working:", Colors.BOLD, no_color))
    print("   $ antimon --test")
    print()
    print("2. " + apply_color("Set up with Claude Code:", Colors.BOLD, no_color))
    print("   $ claude-code config set hooks.PreToolUse antimon")
    print()
    print("3. " + apply_color("Or try it manually:", Colors.BOLD, no_color))
    print('   $ echo \'{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "/etc/passwd", "content": "test"}}\' | antimon')
    print()
    
    print(apply_color("📚 Learn More:", Colors.OKBLUE, no_color))
    print("• Documentation: https://github.com/yourusername/antimon")
    print("• Run 'antimon --help' for all options")
    print("• Use 'antimon --test' to verify your installation")
    print()
    
    print(apply_color("💡 Tip:", Colors.WARNING, no_color), end=" ")
    print("antimon runs automatically when Claude Code tries to modify files.")
    print("   It will block potentially dangerous operations before they happen.")
    print()
    
    print(apply_color("This message will only appear once. Happy coding! 🚀", Colors.OKGREEN, no_color))
    print()


def check_claude_code_setup() -> Optional[str]:
    """Check if Claude Code is set up with antimon."""
    try:
        import subprocess
        result = subprocess.run(
            ["claude-code", "config", "get", "hooks.PreToolUse"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and "antimon" in result.stdout:
            return "configured"
        elif result.returncode == 0:
            return "not_configured"
    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def suggest_claude_code_setup(no_color: bool = False) -> None:
    """Suggest Claude Code setup if not configured."""
    setup_status = check_claude_code_setup()
    
    if setup_status == "not_configured":
        print()
        print(apply_color("💡 Claude Code detected but antimon not configured!", Colors.WARNING, no_color))
        print("   Run this command to set it up:")
        print(apply_color("   $ claude-code config set hooks.PreToolUse antimon", Colors.BOLD, no_color))
        print()