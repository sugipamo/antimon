# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for core functionality with runtime config
"""

import pytest

from antimon.core import validate_hook_data
from antimon.runtime_config import RuntimeConfig, set_runtime_config


def test_validate_with_ignored_file():
    """Test validation skips ignored files."""
    # Set up runtime config
    config = RuntimeConfig()
    config.ignore_patterns = ["*.test.py", "examples/*"]
    set_runtime_config(config)
    
    # Test with ignored file
    json_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "test_api.test.py",
            "content": "api_key = 'sk-1234567890'"
        }
    }
    
    has_issues, issues, stats = validate_hook_data(json_data)
    
    # Should not detect issues for ignored files
    assert has_issues is False
    assert len(issues) == 0


def test_validate_with_allowed_file():
    """Test validation allows explicitly allowed files."""
    # Set up runtime config
    config = RuntimeConfig()
    config.allowed_files = {"/etc/myapp.conf"}
    set_runtime_config(config)
    
    # Test with allowed sensitive file
    json_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/etc/myapp.conf",
            "content": "config data"
        }
    }
    
    has_issues, issues, stats = validate_hook_data(json_data)
    
    # Should not detect issues for allowed files
    assert has_issues is False
    assert len(issues) == 0


def test_validate_with_disabled_detector():
    """Test validation skips disabled detectors."""
    # Set up runtime config
    config = RuntimeConfig()
    config.disabled_detectors = {"api_key", "llm_api"}
    set_runtime_config(config)
    
    # Test with content that would trigger disabled detectors
    json_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "bot.py",
            "content": "from openai import OpenAI\napi_key = 'sk-1234567890'"
        }
    }
    
    has_issues, issues, stats = validate_hook_data(json_data)
    
    # Should not detect issues from disabled detectors
    assert has_issues is False
    assert len(issues) == 0
    
    # Reset config for other tests
    set_runtime_config(RuntimeConfig())