# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
First-run detection and setup guide for antimon
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from .color_utils import Colors, apply_color
from .constants import GITHUB_REPO_URL


def safe_input(prompt):
    """Safe input function for user prompts."""
    # Python 3.11+ only, input is always safe
    return input(prompt)


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


def show_first_run_guide(no_color: bool = False, is_quickstart: bool = False) -> None:
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
    print(
        '   $ echo \'{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "/etc/passwd", "content": "test"}}\' | antimon'
    )
    print()

    print(apply_color("📚 Learn More:", Colors.OKBLUE, no_color))
    print(f"• Documentation: {GITHUB_REPO_URL}")
    print("• Run 'antimon --help' for all options")
    print("• Use 'antimon --test' to verify your installation")
    print()

    print(apply_color("💡 Tip:", Colors.WARNING, no_color), end=" ")
    print("antimon runs automatically when Claude Code tries to modify files.")
    print("   It will block potentially dangerous operations before they happen.")
    print()

    if not is_quickstart:
        print(
            apply_color(
                "This message will only appear once. Happy coding! 🚀",
                Colors.OKGREEN,
                no_color,
            )
        )
    else:
        print(apply_color("Happy coding! 🚀", Colors.OKGREEN, no_color))
    print()


def check_claude_code_setup() -> str | None:
    """Check if Claude Code is set up with antimon."""
    try:
        result = subprocess.run(
            ["claude-code", "config", "get", "hooks.PreToolUse"],
            capture_output=True,
            text=True,
            timeout=2,
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
        print(
            apply_color(
                "💡 Claude Code detected but antimon not configured!",
                Colors.WARNING,
                no_color,
            )
        )
        print("   Run this command to set it up:")
        print(
            apply_color(
                "   $ claude-code config set hooks.PreToolUse antimon",
                Colors.BOLD,
                no_color,
            )
        )
        print()


def prompt_yes_no(question: str, default: bool = True, no_color: bool = False) -> bool:
    """Prompt user for yes/no answer."""
    # Check if stdin is interactive
    if not sys.stdin.isatty():
        # Non-interactive mode, return default
        return default

    default_str = "Y/n" if default else "y/N"
    prompt = f"{question} [{default_str}]: "

    try:
        while True:
            response = (
                safe_input(apply_color(prompt, Colors.OKBLUE, no_color)).strip().lower()
            )
            if not response:
                return default
            if response in ["y", "yes"]:
                return True
            if response in ["n", "no"]:
                return False
            print(apply_color("Please answer 'y' or 'n'.", Colors.WARNING, no_color))
    except (EOFError, KeyboardInterrupt):
        print()  # New line after ^C
        return default


def run_command(cmd: list, timeout: int = 10) -> tuple[bool, str, str]:
    """Run a command and return success status, stdout, and stderr."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except (
        subprocess.SubprocessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ) as e:
        return False, "", str(e)


def setup_claude_code_automatically(no_color: bool = False) -> bool:
    """Automatically set up Claude Code integration."""
    print(
        apply_color("⚙️  Setting up Claude Code integration...", Colors.HEADER, no_color)
    )

    success, stdout, stderr = run_command(
        ["claude-code", "config", "set", "hooks.PreToolUse", "antimon"]
    )

    if success:
        print(
            apply_color(
                "✅ Successfully configured Claude Code!", Colors.OKGREEN, no_color
            )
        )
        return True
    else:
        print(apply_color("❌ Failed to configure Claude Code:", Colors.FAIL, no_color))
        if stderr:
            print(f"   {stderr}")
        return False


def verify_setup(no_color: bool = False) -> bool:
    """Verify that antimon is set up correctly."""
    print()
    print(apply_color("🔍 Verifying setup...", Colors.HEADER, no_color))

    # Check if antimon is in PATH
    antimon_path = shutil.which("antimon")
    if not antimon_path:
        print(apply_color("❌ antimon not found in PATH", Colors.FAIL, no_color))
        return False
    print(apply_color(f"✅ antimon found at: {antimon_path}", Colors.OKGREEN, no_color))

    # Check Claude Code setup if available
    claude_status = check_claude_code_setup()
    if claude_status == "configured":
        print(
            apply_color(
                "✅ Claude Code integration configured", Colors.OKGREEN, no_color
            )
        )
    elif claude_status == "not_configured":
        print(
            apply_color(
                "⚠️  Claude Code found but not configured", Colors.WARNING, no_color
            )
        )
    else:
        print(
            apply_color(
                "ℹ️  Claude Code not detected (optional)", Colors.OKBLUE, no_color
            )
        )

    # Test antimon functionality
    test_data = '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "/etc/passwd", "content": "test"}}'
    success, stdout, stderr = run_command(
        ["sh", "-c", f"echo '{test_data}' | antimon"], timeout=5
    )

    if not success and "Security issue detected" in stderr:
        print(
            apply_color(
                "✅ antimon detection working correctly", Colors.OKGREEN, no_color
            )
        )
        return True
    else:
        print(apply_color("❌ antimon detection test failed", Colors.FAIL, no_color))
        return False


def run_interactive_setup(no_color: bool = False) -> None:
    """Run an interactive setup wizard for antimon."""
    print()
    print(apply_color("🧙 antimon Setup Wizard", Colors.HEADER, no_color))
    print(apply_color("=" * 50, Colors.HEADER, no_color))
    print()
    print("This wizard will help you set up antimon for your environment.")
    print()

    # Check for Claude Code
    claude_status = check_claude_code_setup()

    if claude_status == "not_configured":
        print(apply_color("📍 Claude Code detected!", Colors.OKGREEN, no_color))
        if prompt_yes_no(
            "Would you like to configure antimon with Claude Code automatically?",
            default=True,
            no_color=no_color,
        ):
            if setup_claude_code_automatically(no_color=no_color):
                print()
                print(apply_color("🎉 Setup complete!", Colors.OKGREEN, no_color))
            else:
                print()
                print("You can manually configure it later with:")
                print(
                    apply_color(
                        "  $ claude-code config set hooks.PreToolUse antimon",
                        Colors.BOLD,
                        no_color,
                    )
                )
    elif claude_status == "configured":
        print(
            apply_color(
                "✅ Claude Code is already configured with antimon!",
                Colors.OKGREEN,
                no_color,
            )
        )
    else:
        print(apply_color("ℹ️  Claude Code not detected.", Colors.OKBLUE, no_color))
        print("   You can install Claude Code from the official website")
        print("   Or use antimon with other tools via JSON input.")

    print()

    # Offer to run verification
    if prompt_yes_no(
        "Would you like to verify your antimon installation?",
        default=True,
        no_color=no_color,
    ):
        if verify_setup(no_color=no_color):
            print()
            print(
                apply_color(
                    "✨ Everything is working correctly!", Colors.OKGREEN, no_color
                )
            )
        else:
            print()
            print(
                apply_color("⚠️  Some issues were detected.", Colors.WARNING, no_color)
            )
            print("   Please check the messages above and refer to the documentation.")

    print()
    print(apply_color("📚 Next steps:", Colors.OKBLUE, no_color))
    print("• Run 'antimon --test' to see example detections")
    print("• Run 'antimon --help' to see all available options")
    print(f"• Visit {GITHUB_REPO_URL} for documentation")
    print()
    print(apply_color("Happy coding with antimon! 🚀", Colors.OKGREEN, no_color))


def show_claude_code_status(no_color: bool = False) -> None:
    """Show Claude Code integration status on first run."""
    status = check_claude_code_setup()

    if status == "configured":
        print(
            apply_color(
                "\n✅ Claude Code integration is already configured!",
                Colors.OKGREEN,
                no_color,
            )
        )
        print("   antimon will automatically validate your code operations.")
    elif status == "not_configured":
        print(
            apply_color(
                "\n🔔 Claude Code detected but antimon is not configured as a hook.",
                Colors.WARNING,
                no_color,
            )
        )
        print("   To enable automatic security validation, run:")
        print(apply_color("   antimon --setup-claude-code", Colors.HEADER, no_color))
    else:
        print(apply_color("\nℹ️  Claude Code not detected.", Colors.OKBLUE, no_color))
        print(
            "   If you install Claude Code later, run 'antimon --setup-claude-code' to configure it."
        )


def show_first_run_guide_interactive(no_color: bool = False) -> None:
    """Display the first-run guide with interactive setup option."""
    # If not in a terminal (e.g., piped), show the regular guide
    if not sys.stdin.isatty():
        show_first_run_guide(no_color=no_color)
        suggest_claude_code_setup(no_color=no_color)
        return

    print()
    print(apply_color("🎉 Welcome to antimon!", Colors.HEADER, no_color))
    print(apply_color("=" * 50, Colors.HEADER, no_color))
    print()
    print("antimon is a security validation tool for AI coding assistants.")
    print("It helps prevent potentially dangerous operations in your code.")

    # Show Claude Code integration status
    show_claude_code_status(no_color=no_color)
    print()

    if prompt_yes_no(
        "Would you like to run the interactive setup wizard?",
        default=True,
        no_color=no_color,
    ):
        run_interactive_setup(no_color=no_color)
    else:
        # Show the original non-interactive guide
        show_first_run_guide(no_color=no_color)
