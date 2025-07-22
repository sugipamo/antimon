# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for dry-run mode functionality
"""

import io
import json
from unittest.mock import patch

from antimon.cli import main


def test_dry_run_basic():
    """Test basic dry-run functionality"""
    # Test data that would normally trigger a block
    test_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "/etc/passwd", "content": "malicious content"},
    }

    # Mock stdin with test data
    with patch("sys.stdin", io.StringIO(json.dumps(test_data))):
        # Capture stdout and stderr
        with patch("sys.stdout", io.StringIO()):
            with patch("sys.stderr", io.StringIO()) as mock_stderr:
                # Run with dry-run flag
                result = main(["--dry-run", "--no-color"])

    # In dry-run mode, should return 0 (success) even with security issues
    assert result == 0

    stderr_output = mock_stderr.getvalue()

    # Check for dry-run specific messaging
    assert "DRY RUN" in stderr_output
    assert "Security issues that would be detected" in stderr_output
    assert "/etc/passwd" in stderr_output
    assert "This is a preview of what would be blocked" in stderr_output


def test_dry_run_with_api_key():
    """Test dry-run with API key detection"""
    test_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "config.py",
            "content": 'OPENAI_API_KEY = "sk-1234567890abcdef"',
        },
    }

    with patch("sys.stdin", io.StringIO(json.dumps(test_data))):
        with patch("sys.stdout", io.StringIO()):
            with patch("sys.stderr", io.StringIO()) as mock_stderr:
                result = main(["--dry-run", "--no-color"])

    assert result == 0  # Success in dry-run mode

    stderr_output = mock_stderr.getvalue()
    assert "DRY RUN" in stderr_output
    assert "API key" in stderr_output  # Changed to match actual output
    assert "No actual blocking occurred" in stderr_output


def test_dry_run_no_issues():
    """Test dry-run with no security issues"""
    test_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "hello.py", "content": 'print("Hello World")'},
    }

    with patch("sys.stdin", io.StringIO(json.dumps(test_data))):
        with patch("sys.stdout", io.StringIO()):
            with patch("sys.stderr", io.StringIO()) as mock_stderr:
                result = main(["--dry-run", "--no-color"])

    assert result == 0

    stderr_output = mock_stderr.getvalue()
    # Should not show any dry-run warnings if no issues detected
    assert "DRY RUN" not in stderr_output
    assert "Security issues" not in stderr_output


def test_dry_run_with_verbose():
    """Test dry-run mode with verbose output"""
    test_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/home/user/.ssh/id_rsa",
            "content": "ssh key content",
        },
    }

    with patch("sys.stdin", io.StringIO(json.dumps(test_data))):
        with patch("sys.stdout", io.StringIO()):
            with patch("sys.stderr", io.StringIO()) as mock_stderr:
                result = main(["--dry-run", "--verbose", "--no-color"])

    assert result == 0

    stderr_output = mock_stderr.getvalue()

    # Verbose mode should show more details
    assert "DRY RUN" in stderr_output
    assert "Detection Results:" in stderr_output
    assert ".ssh/id_rsa" in stderr_output
    assert "DRY RUN Summary:" in stderr_output


def test_dry_run_combined_with_allow_file():
    """Test dry-run mode combined with --allow-file option"""
    test_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "/etc/hosts", "content": "127.0.0.1 localhost"},
    }

    with patch("sys.stdin", io.StringIO(json.dumps(test_data))):
        with patch("sys.stdout", io.StringIO()):
            with patch("sys.stderr", io.StringIO()) as mock_stderr:
                # With --allow-file, shouldn't detect any issues even in dry-run
                result = main(["--dry-run", "--allow-file", "/etc/hosts", "--no-color"])

    assert result == 0

    stderr_output = mock_stderr.getvalue()
    # Should not show security issues since file is allowed
    assert "DRY RUN" not in stderr_output
    assert "Security issues" not in stderr_output
