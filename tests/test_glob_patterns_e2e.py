# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
End-to-end tests for glob pattern support in --allow-file
"""

import json
import subprocess
import sys


def test_allow_file_glob_patterns():
    """Test --allow-file with various glob patterns."""
    # Test case 1: Simple glob pattern (*.env)
    hook_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "production.env",
            "content": "# Environment config",
        },
    }

    # Should be blocked without --allow-file
    result = subprocess.run(
        [sys.executable, "-m", "antimon"],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2
    assert "environment variables file" in result.stderr.lower()

    # Should pass with --allow-file *.env
    result = subprocess.run(
        [sys.executable, "-m", "antimon", "--allow-file", "*.env"],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0

    # Test case 2: Directory glob pattern (config/*.json)
    hook_data["tool_input"]["file_path"] = "config/database.json"

    # Should pass (no sensitive pattern match)
    result = subprocess.run(
        [sys.executable, "-m", "antimon"],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0

    # Should pass with --allow-file config/*.json
    result = subprocess.run(
        [sys.executable, "-m", "antimon", "--allow-file", "config/*.json"],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0

    # Test case 3: Recursive glob pattern (**/*.pem)
    hook_data["tool_input"]["file_path"] = "deep/nested/dir/server.pem"

    # Should be blocked without --allow-file
    result = subprocess.run(
        [sys.executable, "-m", "antimon"],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2
    assert "cryptographic key" in result.stderr.lower()

    # Should pass with --allow-file **/*.pem
    result = subprocess.run(
        [sys.executable, "-m", "antimon", "--allow-file", "**/*.pem"],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0

    # Test case 4: Multiple patterns
    hook_data["tool_input"]["file_path"] = "deploy_key"

    # Should pass with multiple --allow-file options
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "antimon",
            "--allow-file",
            "*.env",
            "--allow-file",
            "deploy_key",
        ],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0


def test_allow_file_with_api_key_detection():
    """Test that --allow-file only affects filename detection, not API key detection."""
    hook_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "config.env",
            "content": 'API_KEY="sk-1234567890abcdef"',
        },
    }

    # Should still be blocked for API key even with --allow-file *.env
    result = subprocess.run(
        [sys.executable, "-m", "antimon", "--allow-file", "*.env"],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2
    assert "api key" in result.stderr.lower()


if __name__ == "__main__":
    test_allow_file_glob_patterns()
    test_allow_file_with_api_key_detection()
    print("All e2e tests passed!")
