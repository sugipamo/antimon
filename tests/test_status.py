# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for the status command
"""

import io
from unittest.mock import patch

from antimon.cli import main
from antimon.runtime_config import RuntimeConfig, set_runtime_config


def test_status_command_basic():
    """Test basic status command functionality"""
    # Capture stdout
    captured_output = io.StringIO()

    with patch("sys.stdout", captured_output), patch("sys.stderr", io.StringIO()):
        result = main(["--status", "--no-color"])

    assert result == 0
    output = captured_output.getvalue()

    # Check for expected sections
    assert "antimon status" in output
    assert "🔍 Detectors" in output
    assert "📄 Allowed Files" in output
    assert "🚫 Ignored Patterns" in output
    assert "⚙️  Configuration Sources" in output
    assert "🤖 Claude Code Integration" in output
    assert "💡 Quick Tips" in output


def test_status_with_runtime_config():
    """Test status command with runtime configuration"""
    # Capture stdout
    captured_output = io.StringIO()

    with patch("sys.stdout", captured_output), patch("sys.stderr", io.StringIO()):
        # Pass configuration via command line arguments
        result = main(
            [
                "--status",
                "--no-color",
                "--allow-file",
                "test.env",
                "--allow-file",
                "*.secret",
                "--ignore-pattern",
                "*.test.py",
                "--disable-detector",
                "docker",
                "--disable-detector",
                "localhost",
            ]
        )

    assert result == 0
    output = captured_output.getvalue()

    # Check allowed files
    assert "test.env" in output
    assert "*.secret" in output

    # Check ignored patterns
    assert "*.test.py" in output

    # Check disabled detectors
    assert "✗ disabled  docker" in output
    assert "✗ disabled  localhost" in output
    assert "✓ enabled  filenames" in output  # Should still be enabled


def test_status_with_environment_variables():
    """Test status command with environment variables"""
    # Set environment variables
    env_patch = {
        "ANTIMON_ALLOW_FILES": "config.yaml,secrets.json",
        "ANTIMON_IGNORE_PATTERNS": "test_*,*_test.py",
        "ANTIMON_DISABLE_DETECTORS": "api_key,llm_api",
    }

    # Reset runtime config to ensure env vars are loaded
    set_runtime_config(None)

    # Capture stdout
    captured_output = io.StringIO()

    with patch.dict("os.environ", env_patch), patch("sys.stdout", captured_output):
        with patch("sys.stderr", io.StringIO()):
            result = main(["--status", "--no-color"])

    assert result == 0
    output = captured_output.getvalue()

    # Check that env vars are shown
    assert "ANTIMON_ALLOW_FILES: config.yaml,secrets.json" in output
    assert "ANTIMON_IGNORE_PATTERNS: test_*,*_test.py" in output
    assert "ANTIMON_DISABLE_DETECTORS: api_key,llm_api" in output


def test_status_detector_display():
    """Test that all detectors are displayed correctly"""
    # Reset runtime config
    set_runtime_config(RuntimeConfig())

    # Capture stdout
    captured_output = io.StringIO()

    with patch("sys.stdout", captured_output), patch("sys.stderr", io.StringIO()):
        result = main(["--status", "--no-color"])

    assert result == 0
    output = captured_output.getvalue()

    # Check all detectors are shown
    expected_detectors = [
        "filenames",
        "llm_api",
        "api_key",
        "docker",
        "localhost",
        "claude_antipatterns",
        "bash",
        "read",
    ]

    for detector in expected_detectors:
        assert detector in output
        assert f"✓ enabled  {detector}" in output
