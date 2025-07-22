# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Last error tracking for antimon
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .color_utils import Colors, apply_color


def get_error_file() -> Path:
    """Get the path to the last error file."""
    from .first_run import get_config_dir

    config_dir = get_config_dir()
    return config_dir / "last_error.json"


def save_last_error(issues: list[str], hook_data: dict[str, Any]) -> None:
    """Save the last error for later explanation."""
    error_file = get_error_file()
    error_file.parent.mkdir(parents=True, exist_ok=True)

    error_record = {
        "timestamp": datetime.now().isoformat(),
        "issues": issues,
        "hook_data": hook_data,
        "tool_name": hook_data.get("tool_name", ""),
        "file_path": hook_data.get("tool_input", {}).get("file_path", ""),
    }

    try:
        with open(error_file, "w") as f:
            json.dump(error_record, f, indent=2)
    except Exception:
        # Silently fail - don't interrupt the main flow
        pass


def load_last_error() -> dict[str, Any] | None:
    """Load the last error if available."""
    error_file = get_error_file()

    if not error_file.exists():
        return None

    try:
        with open(error_file) as f:
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


def _provide_detailed_explanations(
    issues: list[str], hook_data: dict, no_color: bool
) -> None:
    """Provide detailed explanations for each issue type."""
    print(apply_color("📚 Why these are blocked:", Colors.OKBLUE, no_color))
    print()

    # Track which explanations we've shown to avoid duplicates
    explained_types = set()

    for issue in issues:
        if "API key" in issue and "api_key" not in explained_types:
            explained_types.add("api_key")
            print("• " + apply_color("API Key Detection:", Colors.BOLD, no_color))
            print("  " + apply_color("What we look for:", Colors.UNDERLINE, no_color))
            print("    - Patterns: api_key='...', secret_key=\"...\", bearer tokens")
            print("    - Common formats: sk-..., AIza..., xoxb-...")
            print("  " + apply_color("Why it's dangerous:", Colors.UNDERLINE, no_color))
            print("    - Exposed in version control history forever")
            print("    - Visible in logs, error messages, and stack traces")
            print("    - Can be scraped by automated tools")
            print(
                "  " + apply_color("How detection works:", Colors.UNDERLINE, no_color)
            )
            print("    - Regular expressions match common key patterns")
            print("    - Case-insensitive matching for flexibility")
            print()

        elif "sensitive file" in issue and "sensitive_file" not in explained_types:
            explained_types.add("sensitive_file")
            print(
                "• " + apply_color("Sensitive File Detection:", Colors.BOLD, no_color)
            )
            print("  " + apply_color("What we look for:", Colors.UNDERLINE, no_color))
            print("    - System files: /etc/passwd, /etc/shadow")
            print("    - SSH keys: ~/.ssh/id_rsa, ~/.ssh/id_ed25519")
            print("    - Environment files: .env, .env.local")
            print("    - Certificates: .pem, .key, .pfx, .p12")
            print("  " + apply_color("Why it's dangerous:", Colors.UNDERLINE, no_color))
            print("    - Contains authentication credentials")
            print("    - Can compromise entire systems")
            print("    - Often have strict permissions for a reason")
            print(
                "  " + apply_color("How detection works:", Colors.UNDERLINE, no_color)
            )
            print("    - Path pattern matching against known sensitive locations")
            print("    - File extension checking for key/cert files")
            print()

        elif (
            "LLM API" in issue or "external AI" in issue
        ) and "llm_api" not in explained_types:
            explained_types.add("llm_api")
            print(
                "• " + apply_color("External LLM API Detection:", Colors.BOLD, no_color)
            )
            print("  " + apply_color("What we look for:", Colors.UNDERLINE, no_color))
            print("    - Import statements: from openai import ...")
            print("    - API endpoints: api.openai.com, gemini.google.com")
            print("    - SDK usage: OpenAI(), Anthropic(), etc.")
            print("  " + apply_color("Why it's dangerous:", Colors.UNDERLINE, no_color))
            print("    - Your code/data leaves your control")
            print("    - Unexpected costs from API usage")
            print("    - Requires managing API keys")
            print(
                "  " + apply_color("How detection works:", Colors.UNDERLINE, no_color)
            )
            print("    - Import statement pattern matching")
            print("    - URL and domain detection")
            print()

        elif "Docker" in issue and "docker" not in explained_types:
            explained_types.add("docker")
            print(
                "• " + apply_color("Docker Operation Detection:", Colors.BOLD, no_color)
            )
            print("  " + apply_color("What we look for:", Colors.UNDERLINE, no_color))
            print("    - Commands: docker run, docker exec, docker build")
            print("    - Files: Dockerfile, docker-compose.yml")
            print("  " + apply_color("Why it's dangerous:", Colors.UNDERLINE, no_color))
            print("    - Potential container escapes")
            print("    - Resource consumption issues")
            print("    - Security misconfigurations")
            print(
                "  " + apply_color("How detection works:", Colors.UNDERLINE, no_color)
            )
            print("    - Command pattern matching")
            print("    - Dockerfile keyword detection")
            print()

        elif "localhost" in issue and "localhost" not in explained_types:
            explained_types.add("localhost")
            print(
                "• "
                + apply_color("Localhost Connection Detection:", Colors.BOLD, no_color)
            )
            print("  " + apply_color("What we look for:", Colors.UNDERLINE, no_color))
            print("    - URLs: localhost:PORT, 127.0.0.1:PORT")
            print("    - Common ports: 3000, 8000, 8080, 5432, 3306")
            print("  " + apply_color("Why it's dangerous:", Colors.UNDERLINE, no_color))
            print("    - Environment-specific configurations")
            print("    - May expose local services")
            print("    - Breaks in production environments")
            print(
                "  " + apply_color("How detection works:", Colors.UNDERLINE, no_color)
            )
            print("    - URL pattern matching with port numbers")
            print("    - Common development port detection")
            print()


def _suggest_solutions(issues: list[str], hook_data: dict, no_color: bool) -> None:
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
    print(
        apply_color("🚨 If you need to bypass temporarily:", Colors.WARNING, no_color)
    )
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
