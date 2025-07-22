# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for core functionality with runtime config
"""


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
    """Test validation allows explicitly allowed files but still checks content."""
    # Set up runtime config
    config = RuntimeConfig()
    config.allowed_files = {"/etc/myapp.conf"}
    set_runtime_config(config)

    # Test with allowed sensitive file but with API key in content
    json_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/etc/myapp.conf",
            "content": "api_key = 'sk-1234567890'"
        }
    }

    has_issues, issues, stats = validate_hook_data(json_data)

    # Should detect API key issue even for allowed files
    assert has_issues is True
    assert len(issues) == 1
    assert "API key" in issues[0]


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


def test_validate_allowed_file_skips_filename_detection_only():
    """Test that allowed files skip filename detection but not content detection."""
    # Set up runtime config
    config = RuntimeConfig()
    config.allowed_files = {"/etc/passwd"}
    set_runtime_config(config)

    # Test with allowed sensitive file path
    json_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/etc/passwd",
            "content": "safe content"
        }
    }

    has_issues, issues, stats = validate_hook_data(json_data)

    # Should not detect filename issue for allowed file
    assert has_issues is False
    assert len(issues) == 0

    # Now test same file with API key
    json_data["tool_input"]["content"] = "openai_api_key = 'sk-test123'"
    has_issues, issues, stats = validate_hook_data(json_data)

    # Should still detect API key even though file is allowed
    assert has_issues is True
    assert len(issues) == 1
    assert "API key" in issues[0]

    # Reset config for other tests
    set_runtime_config(RuntimeConfig())
