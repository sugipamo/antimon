# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for first-run detection and setup guide
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from antimon.first_run import (
    get_config_dir,
    is_first_run,
    mark_first_run_complete,
    show_first_run_guide,
    check_claude_code_setup,
    suggest_claude_code_setup,
)


def test_get_config_dir_linux():
    """Test getting config directory on Linux."""
    with patch.dict(os.environ, {"XDG_CONFIG_HOME": "/custom/config"}, clear=True):
        with patch("sys.platform", "linux"):
            config_dir = get_config_dir()
            assert str(config_dir) == "/custom/config/antimon"


def test_get_config_dir_windows():
    """Test getting config directory on Windows."""
    with patch.dict(os.environ, {"APPDATA": "C:\\Users\\Test\\AppData\\Roaming"}, clear=True):
        with patch("sys.platform", "win32"):
            config_dir = get_config_dir()
            # Path uses forward slashes even on Windows with pathlib
            assert str(config_dir).replace("\\", "/") == "C:/Users/Test/AppData/Roaming/antimon"


def test_first_run_detection(tmp_path):
    """Test first run detection and marking."""
    # Mock the config directory
    with patch("antimon.first_run.get_config_dir", return_value=tmp_path / "antimon"):
        # Should be first run initially
        assert is_first_run() is True
        
        # Mark as complete
        mark_first_run_complete()
        
        # Should no longer be first run
        assert is_first_run() is False
        
        # Marker file should exist
        marker_file = tmp_path / "antimon" / ".first_run_complete"
        assert marker_file.exists()


def test_show_first_run_guide(capsys):
    """Test showing the first-run guide."""
    show_first_run_guide(no_color=True)
    
    captured = capsys.readouterr()
    assert "Welcome to antimon!" in captured.out
    assert "Quick Start:" in captured.out
    assert "antimon --test" in captured.out
    assert "claude-code config set" in captured.out
    assert "Learn More:" in captured.out


def test_check_claude_code_setup():
    """Test checking Claude Code setup."""
    # Test when claude-code returns antimon
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="antimon")
        assert check_claude_code_setup() == "configured"
    
    # Test when claude-code returns something else
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="other-hook")
        assert check_claude_code_setup() == "not_configured"
    
    # Test when claude-code is not found
    with patch("subprocess.run", side_effect=FileNotFoundError):
        assert check_claude_code_setup() is None


def test_suggest_claude_code_setup(capsys):
    """Test suggesting Claude Code setup."""
    # Test when not configured
    with patch("antimon.first_run.check_claude_code_setup", return_value="not_configured"):
        suggest_claude_code_setup(no_color=True)
        captured = capsys.readouterr()
        assert "Claude Code detected but antimon not configured!" in captured.out
        assert "claude-code config set hooks.PreToolUse antimon" in captured.out
    
    # Test when configured
    with patch("antimon.first_run.check_claude_code_setup", return_value="configured"):
        suggest_claude_code_setup(no_color=True)
        captured = capsys.readouterr()
        assert captured.out == ""  # Should not print anything
    
    # Test when claude-code not found
    with patch("antimon.first_run.check_claude_code_setup", return_value=None):
        suggest_claude_code_setup(no_color=True)
        captured = capsys.readouterr()
        assert captured.out == ""  # Should not print anything