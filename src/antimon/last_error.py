# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Last error tracking for antimon
"""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

from .color_utils import apply_color, Colors


def get_error_file() -> Path:
    """Get the path to the last error file."""
    from .first_run import get_config_dir
    config_dir = get_config_dir()
    return config_dir / "last_error.json"


def save_last_error(issues: List[str], hook_data: Dict) -> None:
    """Save the last error for later explanation."""
    error_file = get_error_file()
    error_file.parent.mkdir(parents=True, exist_ok=True)
    
    error_record = {
        "timestamp": datetime.now().isoformat(),
        "issues": issues,
        "hook_data": hook_data,
        "tool_name": hook_data.get("tool_name", ""),
        "file_path": hook_data.get("tool_input", {}).get("file_path", "")
    }
    
    try:
        with open(error_file, "w") as f:
            json.dump(error_record, f, indent=2)
    except Exception as e:
        # Silently fail - don't interrupt the main flow
        pass


def load_last_error() -> Optional[Dict]:
    """Load the last error if available."""
    error_file = get_error_file()
    
    if not error_file.exists():
        return None
    
    try:
        with open(error_file, "r") as f:
            return json.load(f)
    except Exception:
        return None


def explain_last_error(no_color: bool = False) -> None:
    """Explain the last error in detail."""
    error_record = load_last_error()
    
    if not error_record:
        print(apply_color("ℹ️  No recent errors found.", Colors.WARNING, no_color))
        print("\nThis command shows detailed explanations for the last antimon block.")
        print("Run it after antimon blocks an operation to understand why.")
        return
    
    print()
    print(apply_color("📋 Last Error Details", Colors.HEADER, no_color))
    print(apply_color("=" * 50, Colors.HEADER, no_color))
    print()
    
    # Show when the error occurred
    timestamp = error_record.get("timestamp", "Unknown")
    print(f"⏰ Occurred at: {timestamp}")
    print()
    
    # Show the tool and file
    tool_name = error_record.get("tool_name", "Unknown")
    file_path = error_record.get("file_path", "N/A")
    print(f"🔧 Tool: {tool_name}")
    print(f"📄 File: {file_path}")
    print()
    
    # Show the issues
    issues = error_record.get("issues", [])
    print(apply_color("❌ Issues detected:", Colors.FAIL, no_color))
    for issue in issues:
        print(f"   • {issue}")
    print()
    
    # Provide detailed explanations for each issue type
    hook_data = error_record.get("hook_data", {})
    _provide_detailed_explanations(issues, hook_data, no_color)
    
    # Show how to bypass if needed
    print(apply_color("🔧 How to handle this:", Colors.OKBLUE, no_color))
    print()
    _suggest_solutions(issues, hook_data, no_color)


def _provide_detailed_explanations(issues: List[str], hook_data: Dict, no_color: bool) -> None:
    """Provide detailed explanations for each issue type."""
    print(apply_color("📚 Why these are blocked:", Colors.OKBLUE, no_color))
    print()
    
    for issue in issues:
        if "API key" in issue:
            print("• " + apply_color("API Keys:", Colors.BOLD, no_color))
            print("  Hardcoded API keys in code are a security risk.")
            print("  They can be exposed in version control, logs, or error messages.")
            print("  Best practice: Use environment variables or secure vaults.")
            print()
        
        elif "sensitive file" in issue:
            print("• " + apply_color("Sensitive Files:", Colors.BOLD, no_color))
            print("  System files like /etc/passwd contain critical security information.")
            print("  AI tools should not modify these files to prevent system compromise.")
            print("  Best practice: Use application-specific config files instead.")
            print()
        
        elif "LLM API" in issue or "external AI" in issue:
            print("• " + apply_color("External AI APIs:", Colors.BOLD, no_color))
            print("  Using external AI services can leak your code and data.")
            print("  It also creates dependencies on third-party services.")
            print("  Best practice: Use local models or the AI assistant's built-in capabilities.")
            print()
        
        elif "Docker" in issue:
            print("• " + apply_color("Docker Operations:", Colors.BOLD, no_color))
            print("  Docker commands can expose your system to container escapes.")
            print("  They can also consume significant system resources.")
            print("  Best practice: Use docker-compose or development containers.")
            print()
        
        elif "localhost" in issue:
            print("• " + apply_color("Localhost Connections:", Colors.BOLD, no_color))
            print("  Hardcoded localhost URLs can break in different environments.")
            print("  They may also expose local services unintentionally.")
            print("  Best practice: Use environment-specific configuration.")
            print()


def _suggest_solutions(issues: List[str], hook_data: Dict, no_color: bool) -> None:
    """Suggest specific solutions for the detected issues."""
    suggested_solutions = set()
    
    for issue in issues:
        if "API key" in issue:
            suggested_solutions.add("api_key")
        elif "sensitive file" in issue:
            suggested_solutions.add("sensitive_file")
        elif "LLM API" in issue:
            suggested_solutions.add("llm_api")
    
    if "api_key" in suggested_solutions:
        print("1. " + apply_color("For API Keys:", Colors.BOLD, no_color))
        print("   # Instead of:")
        print("   api_key = 'sk-1234567890abcdef'")
        print()
        print("   # Use:")
        print("   import os")
        print("   api_key = os.environ.get('API_KEY')")
        print()
    
    if "sensitive_file" in suggested_solutions:
        file_path = hook_data.get("tool_input", {}).get("file_path", "")
        print("2. " + apply_color("For Sensitive Files:", Colors.BOLD, no_color))
        print(f"   # Instead of modifying: {file_path}")
        print("   # Create a project-specific config:")
        print("   ~/.config/myapp/config.yaml")
        print("   ./config/settings.json")
        print()
    
    if "llm_api" in suggested_solutions:
        print("3. " + apply_color("For LLM APIs:", Colors.BOLD, no_color))
        print("   # Instead of: from openai import OpenAI")
        print("   # Consider:")
        print("   - Using Claude's built-in capabilities")
        print("   - Local models with llama.cpp or ollama")
        print("   - Mock responses for testing")
        print()
    
    # Always show bypass option
    print(apply_color("🚨 If you need to bypass temporarily:", Colors.WARNING, no_color))
    print("   # Disable antimon:")
    print("   claude-code config unset hooks.PreToolUse")
    print()
    print("   # Re-enable after:")
    print("   claude-code config set hooks.PreToolUse antimon")
    print()
    
    # Show how to whitelist
    print(apply_color("📝 To allow specific files:", Colors.OKGREEN, no_color))
    print("   # Use runtime options:")
    file_path = hook_data.get("tool_input", {}).get("file_path", "")
    if file_path:
        print(f"   echo '{{...}}' | antimon --allow-file '{file_path}'")
    else:
        print("   echo '{...}' | antimon --allow-file /path/to/file")
    print()
    print("   # Or use environment variables:")
    print("   export ANTIMON_ALLOW_FILES='/path/to/file1,/path/to/file2'")
    print()