#!/usr/bin/env python3
"""Simplified setup wizard for Claude Code integration"""

import json
import subprocess

from .color_utils import ColorFormatter


def find_claude_code_command() -> str | None:
    """
    Find claude command in PATH

    Returns:
        Path to claude command or None if not found
    """
    # Try both 'claude' and 'claude-code' command names
    for cmd in ["claude", "claude-code"]:
        try:
            result = subprocess.run(
                ["which", cmd], capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                # Verify it's actually Claude Code by checking version
                version_result = subprocess.run(
                    [cmd, "--version"], capture_output=True, text=True, check=False
                )
                if version_result.returncode == 0 and "Claude Code" in version_result.stdout:
                    return result.stdout.strip()
        except Exception:
            continue
    return None


def get_claude_code_config() -> dict | None:
    """
    Get current Claude Code configuration from settings files

    Returns:
        Current configuration dict or None if not available
    """
    import os
    
    # Check settings files in order of precedence
    config_paths = [
        os.path.expanduser("~/.claude/settings.local.json"),
        os.path.expanduser("~/.claude/settings.json"),
        os.path.expanduser("~/.claude/settings.json")  # User settings
    ]
    
    for config_path in config_paths:
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception:
            continue
    return None


def set_claude_code_hook(hook_name: str, command: str) -> bool:
    """
    Set a Claude Code hook by editing .claude/settings.local.json

    Args:
        hook_name: Name of the hook (e.g., "PreToolUse")
        command: Command to set for the hook

    Returns:
        True if successful, False otherwise
    """
    import os
    import json
    
    # Use .claude/settings.local.json for local project settings
    config_dir = os.path.expanduser("~/.claude")
    config_path = os.path.join(config_dir, "settings.local.json")
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)
        
        # Read current config
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Add hooks section if it doesn't exist
        if "hooks" not in config:
            config["hooks"] = {}
        
        # Add the specific hook in the correct format
        if hook_name not in config["hooks"]:
            config["hooks"][hook_name] = []
        
        # Set the hook in the correct format
        config["hooks"][hook_name] = [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": command
                    }
                ]
            }
        ]
        
        # Write back to file
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception:
        return False


def setup_claude_code_integration(no_color: bool = False) -> bool:
    """
    Simplified setup for Claude Code integration

    Args:
        no_color: Disable colored output

    Returns:
        True if setup was successful, False otherwise
    """
    color = ColorFormatter(use_color=not no_color)

    print(f"\n{color.header('🔧 Claude Code Integration Setup')}")
    print("=" * 50)

    # Check if claude-code is installed
    print(f"\n{color.info('Checking for Claude Code...')}")
    claude_code_path = find_claude_code_command()

    if not claude_code_path:
        print(f"{color.error('❌ Claude Code not found in PATH')}")
        print("\n💡 To install Claude Code:")
        print(f"   {color.code('Visit: https://claude.ai/download')}")
        print(f"   {color.code('Or run: npm install -g @anthropic/claude-code')}")
        print(f"\n   After installation, run: {color.code('antimon --setup-claude-code')}")
        return False

    print(f"{color.success('✅ Claude Code found')}")

    # Configure the hook
    print(f"\n{color.info('Configuring Claude Code hook...')}")
    
    # Check current hook
    current_config = get_claude_code_config()
    if current_config:
        current_hook = current_config.get("hooks", {}).get("PreToolUse")
        if current_hook == "antimon":
            print(f"{color.success('✅ antimon is already configured!')}")
            return True
        elif current_hook:
            print(f"{color.warning(f'⚠️  Current hook: {current_hook}')}")

    # Set the hook
    if set_claude_code_hook("PreToolUse", "antimon"):
        print(f"{color.success('✅ Successfully configured antimon!')}")
        
        # Show which file was modified
        import os
        config_path = os.path.expanduser("~/.claude/settings.local.json")
        print(f"\n{color.info('Configuration file:')} {config_path}")
        print(f"{color.info('Usage:')} antimon will now protect your Claude Code sessions.")
        return True
    else:
        print(f"{color.error('❌ Failed to configure hook')}")
        return False


def check_claude_code_setup() -> tuple[bool, str]:
    """
    Quick check if Claude Code is properly configured with antimon

    Returns:
        Tuple of (is_configured, status_message)
    """
    # Check if claude exists
    claude_cmd = find_claude_code_command()
    if not claude_cmd:
        return False, "Claude Code not installed"
    
    # Check configuration
    config = get_claude_code_config()
    if not config:
        return False, "Could not read Claude Code configuration"
    
    hooks = config.get("hooks", {})
    pretool_hooks = hooks.get("PreToolUse", [])
    
    # Check if antimon is configured as a hook
    for hook_config in pretool_hooks:
        for hook in hook_config.get("hooks", []):
            if hook.get("command") == "antimon":
                return True, "antimon is configured as PreToolUse hook"
    
    if pretool_hooks:
        return False, "PreToolUse hook configured but not with antimon"
    else:
        return False, "PreToolUse hook not configured"