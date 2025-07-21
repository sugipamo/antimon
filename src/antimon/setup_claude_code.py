#!/usr/bin/env python3
"""Setup wizard for Claude Code integration"""

import json
import os
import subprocess
import sys
from pathlib import Path

from .color_utils import ColorFormatter


def find_claude_code_command() -> str | None:
    """
    Find claude-code command in PATH
    
    Returns:
        Path to claude-code command or None if not found
    """
    try:
        result = subprocess.run(
            ["which", "claude-code"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_claude_code_config() -> dict | None:
    """
    Get current Claude Code configuration
    
    Returns:
        Current configuration dict or None if not available
    """
    try:
        result = subprocess.run(
            ["claude-code", "config", "get"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


def set_claude_code_hook(hook_name: str, command: str) -> bool:
    """
    Set a Claude Code hook
    
    Args:
        hook_name: Name of the hook (e.g., "PreToolUse")
        command: Command to run for the hook
        
    Returns:
        True if successful, False otherwise
    """
    try:
        result = subprocess.run(
            ["claude-code", "config", "set", f"hooks.{hook_name}", command],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False


def verify_antimon_in_path() -> str | None:
    """
    Verify antimon is in PATH
    
    Returns:
        Path to antimon command or None if not found
    """
    try:
        result = subprocess.run(
            ["which", "antimon"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def setup_claude_code_integration(no_color: bool = False) -> bool:
    """
    Interactive setup for Claude Code integration
    
    Args:
        no_color: Disable colored output
        
    Returns:
        True if setup was successful, False otherwise
    """
    color = ColorFormatter(use_color=not no_color)
    
    print(f"\n{color.header('🔧 Claude Code Integration Setup')}")
    print("=" * 50)
    
    # Step 1: Check if claude-code is installed
    print(f"\n{color.info('Step 1: Checking for Claude Code...')}")
    claude_code_path = find_claude_code_command()
    
    if not claude_code_path:
        print(f"{color.error('❌ Claude Code not found in PATH')}")
        print("\n💡 To install Claude Code:")
        print("   • Visit: https://claude.ai/code")
        print("   • Or run: npm install -g @anthropic/claude-code")
        return False
    
    print(f"{color.success('✅ Claude Code found:')} {claude_code_path}")
    
    # Step 2: Check if antimon is in PATH
    print(f"\n{color.info('Step 2: Checking antimon installation...')}")
    antimon_path = verify_antimon_in_path()
    
    if not antimon_path:
        print(f"{color.error('❌ antimon not found in PATH')}")
        print("\n💡 Make sure antimon is installed and in your PATH:")
        print("   • Run: pip install antimon")
        print("   • Or: pipx install antimon")
        return False
    
    print(f"{color.success('✅ antimon found:')} {antimon_path}")
    
    # Step 3: Check current configuration
    print(f"\n{color.info('Step 3: Checking current configuration...')}")
    current_config = get_claude_code_config()
    
    if current_config:
        hooks = current_config.get("hooks", {})
        current_hook = hooks.get("PreToolUse")
        
        if current_hook:
            print(f"{color.warning('⚠️  PreToolUse hook already configured:')}")
            print(f"   Current value: {current_hook}")
            
            if current_hook == "antimon":
                print(f"\n{color.success('✅ antimon is already configured!')}")
                print("\n🎉 You're all set! antimon is protecting your Claude Code sessions.")
                return True
            
            response = input(f"\n{color.info('Replace with antimon? [Y/n]:')} ").strip().lower()
            if response == 'n':
                print("\n❌ Setup cancelled.")
                return False
    
    # Step 4: Configure the hook
    print(f"\n{color.info('Step 4: Configuring Claude Code hook...')}")
    
    if set_claude_code_hook("PreToolUse", "antimon"):
        print(f"{color.success('✅ Successfully configured antimon as PreToolUse hook!')}")
        
        # Step 5: Verify configuration
        print(f"\n{color.info('Step 5: Verifying configuration...')}")
        
        # Check the configuration again
        verify_result = subprocess.run(
            ["claude-code", "config", "get", "hooks.PreToolUse"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if verify_result.returncode == 0 and verify_result.stdout.strip() == "antimon":
            print(f"{color.success('✅ Configuration verified!')}")
            
            print(f"\n{color.header('🎉 Setup Complete!')}")
            print("\nantimon is now protecting your Claude Code sessions.")
            print("\n📝 What happens now:")
            print("   • antimon will check all code modifications before they're applied")
            print("   • Dangerous operations will be blocked automatically")
            print("   • You'll see clear explanations when something is blocked")
            
            print("\n💡 Test it out:")
            print("   1. Open a new Claude Code session")
            print("   2. Try to write a file with an API key:")
            print(f'      {color.code("echo \'api_key = \"sk-123\"\' > test.py")}')
            print("   3. antimon should block this operation")
            
            print("\n🔧 To disable temporarily:")
            print(f"   {color.code('claude-code config unset hooks.PreToolUse')}")
            
            print("\n📚 Learn more:")
            print("   • Run: antimon --help")
            print("   • Visit: https://github.com/yourusername/antimon")
            
            return True
        else:
            print(f"{color.error('❌ Configuration verification failed')}")
            print("\n💡 Try setting it manually:")
            print(f"   {color.code('claude-code config set hooks.PreToolUse antimon')}")
            return False
    else:
        print(f"{color.error('❌ Failed to configure hook')}")
        print("\n💡 Try setting it manually:")
        print(f"   {color.code('claude-code config set hooks.PreToolUse antimon')}")
        return False


def check_claude_code_setup() -> tuple[bool, str]:
    """
    Quick check if Claude Code is properly configured with antimon
    
    Returns:
        Tuple of (is_configured, status_message)
    """
    # Check if claude-code exists
    if not find_claude_code_command():
        return False, "Claude Code not installed"
    
    # Check configuration
    try:
        result = subprocess.run(
            ["claude-code", "config", "get", "hooks.PreToolUse"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            hook_value = result.stdout.strip()
            if hook_value == "antimon":
                return True, "antimon is configured as PreToolUse hook"
            elif hook_value:
                return False, f"PreToolUse hook is set to: {hook_value}"
            else:
                return False, "PreToolUse hook not configured"
        else:
            return False, "Could not read Claude Code configuration"
    except Exception:
        return False, "Error checking Claude Code configuration"