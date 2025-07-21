# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Status command implementation for antimon
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from .runtime_config import get_runtime_config
from .color_utils import apply_color, Colors


def show_status(no_color: bool = False) -> None:
    """
    Display the current status of antimon configuration
    
    Args:
        no_color: Disable colored output
    """
    config = get_runtime_config()
    
    # Title
    print()
    print(apply_color("antimon status", Colors.BOLD, no_color=no_color))
    print(apply_color("=" * 40, Colors.WHITE, no_color=no_color))
    print()
    
    # 1. Detectors
    print(apply_color("🔍 Detectors", Colors.CYAN, no_color=no_color))
    print()
    
    all_detectors = [
        ("filenames", "Dangerous filename detection"),
        ("llm_api", "External LLM API usage detection"),
        ("api_key", "Hardcoded API key detection"),
        ("docker", "Docker operation detection"),
        ("localhost", "Localhost connection detection"),
        ("claude_antipatterns", "Claude anti-pattern detection"),
        ("bash", "Dangerous bash command detection"),
        ("read", "Sensitive file read detection"),
    ]
    
    for detector_name, description in all_detectors:
        if config.is_detector_enabled(detector_name):
            status = apply_color("✓ enabled", Colors.GREEN, no_color=no_color)
        else:
            status = apply_color("✗ disabled", Colors.WHITE, no_color=no_color)
        print(f"  {status}  {detector_name:<20} - {description}")
    
    print()
    
    # 2. Allowed Files
    print(apply_color("📄 Allowed Files", Colors.CYAN, no_color=no_color))
    print()
    
    if config.allowed_files:
        for pattern in sorted(config.allowed_files):
            print(f"  • {pattern}")
    else:
        print(apply_color("  (none)", Colors.WHITE, no_color=no_color))
    
    print()
    
    # 3. Ignored Patterns
    print(apply_color("🚫 Ignored Patterns", Colors.CYAN, no_color=no_color))
    print()
    
    if config.ignore_patterns:
        for pattern in sorted(config.ignore_patterns):
            print(f"  • {pattern}")
    else:
        print(apply_color("  (none)", Colors.WHITE, no_color=no_color))
    
    print()
    
    # 4. Configuration Sources
    print(apply_color("⚙️  Configuration Sources", Colors.CYAN, no_color=no_color))
    print()
    
    # Check for environment variables
    env_vars = [
        ("ANTIMON_IGNORE_PATTERNS", "Ignored patterns"),
        ("ANTIMON_ALLOW_FILES", "Allowed files"),
        ("ANTIMON_DISABLE_DETECTORS", "Disabled detectors"),
    ]
    
    env_found = False
    for var_name, description in env_vars:
        if var_value := os.environ.get(var_name):
            env_found = True
            print(f"  • {var_name}: {var_value}")
    
    if not env_found:
        print(apply_color("  • No environment variables set", Colors.WHITE, no_color=no_color))
    
    # Check for config file (future feature)
    print(apply_color("  • Config file: Not supported yet (coming in v0.3.0)", Colors.WHITE, no_color=no_color))
    
    print()
    
    # 5. Claude Code Integration
    print(apply_color("🤖 Claude Code Integration", Colors.CYAN, no_color=no_color))
    print()
    
    # Try to detect Claude Code configuration
    claude_config_paths = [
        Path.home() / ".config" / "claude-code" / "settings.json",
        Path.home() / "Library" / "Application Support" / "claude-code" / "settings.json",
    ]
    
    claude_configured = False
    for config_path in claude_config_paths:
        if config_path.exists():
            try:
                import json
                with open(config_path, 'r') as f:
                    settings = json.load(f)
                    if settings.get("hooks", {}).get("PreToolUse") == "antimon":
                        claude_configured = True
                        print(apply_color(f"  ✓ Configured in: {config_path}", Colors.GREEN, no_color=no_color))
                        break
            except Exception:
                pass
    
    if not claude_configured:
        print(apply_color("  ✗ Not configured", Colors.YELLOW, no_color=no_color))
        print(apply_color("  → Run 'antimon --setup' to configure", Colors.WHITE, no_color=no_color))
    
    print()
    
    # 6. Quick Tips
    print(apply_color("💡 Quick Tips", Colors.CYAN, no_color=no_color))
    print()
    print("  • Use --allow-file to permit specific files")
    print("  • Use --disable-detector to turn off specific checks")
    print("  • Use --explain-last-error after a block for details")
    print("  • Run --test to verify antimon is working correctly")
    print()