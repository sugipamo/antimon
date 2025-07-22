# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for first-run detection and setup guide
"""

import os
from unittest.mock import MagicMock, patch

from antimon.first_run import (
    check_claude_code_setup,
    get_config_dir,
    is_first_run,
    mark_first_run_complete,
    prompt_yes_no,
    run_command,
    run_interactive_setup,
    setup_claude_code_automatically,
    show_first_run_guide,
    show_first_run_guide_interactive,
    suggest_claude_code_setup,
    verify_setup,
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


def test_prompt_yes_no_interactive():
    """Test interactive yes/no prompt."""
    # Test with 'y' input
    with patch("sys.stdin.isatty", return_value=True):
        with patch("builtins.input", return_value="y"):
            assert prompt_yes_no("Test question?") is True

    # Test with 'n' input
    with patch("sys.stdin.isatty", return_value=True):
        with patch("builtins.input", return_value="n"):
            assert prompt_yes_no("Test question?") is False

    # Test with empty input (default)
    with patch("sys.stdin.isatty", return_value=True):
        with patch("builtins.input", return_value=""):
            assert prompt_yes_no("Test question?", default=True) is True
            assert prompt_yes_no("Test question?", default=False) is False

    # Test non-interactive mode
    with patch("sys.stdin.isatty", return_value=False):
        assert prompt_yes_no("Test question?", default=True) is True
        assert prompt_yes_no("Test question?", default=False) is False


def test_run_command():
    """Test running external commands."""
    # Test successful command
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="output", stderr="")
        success, stdout, stderr = run_command(["echo", "test"])
        assert success is True
        assert stdout == "output"
        assert stderr == ""

    # Test failed command
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
        success, stdout, stderr = run_command(["false"])
        assert success is False
        assert stderr == "error"

    # Test command not found
    with patch("subprocess.run", side_effect=FileNotFoundError("command not found")):
        success, stdout, stderr = run_command(["nonexistent"])
        assert success is False
        assert "command not found" in stderr


def test_setup_claude_code_automatically(capsys):
    """Test automatic Claude Code setup."""
    # Test successful setup
    with patch("antimon.first_run.run_command", return_value=(True, "", "")):
        result = setup_claude_code_automatically(no_color=True)
        assert result is True
        captured = capsys.readouterr()
        assert "Setting up Claude Code integration" in captured.out
        assert "Successfully configured Claude Code!" in captured.out

    # Test failed setup
    with patch("antimon.first_run.run_command", return_value=(False, "", "Permission denied")):
        result = setup_claude_code_automatically(no_color=True)
        assert result is False
        captured = capsys.readouterr()
        assert "Failed to configure Claude Code" in captured.out
        assert "Permission denied" in captured.out


def test_verify_setup(capsys):
    """Test setup verification."""
    # Test successful verification
    with patch("shutil.which", return_value="/usr/local/bin/antimon"):
        with patch("antimon.first_run.check_claude_code_setup", return_value="configured"):
            with patch("antimon.first_run.run_command", return_value=(False, "", "Security issue detected")):
                result = verify_setup(no_color=True)
                assert result is True
                captured = capsys.readouterr()
                assert "antimon found at" in captured.out
                assert "Claude Code integration configured" in captured.out
                assert "antimon detection working correctly" in captured.out

    # Test when antimon not in PATH
    with patch("shutil.which", return_value=None):
        result = verify_setup(no_color=True)
        assert result is False
        captured = capsys.readouterr()
        assert "antimon not found in PATH" in captured.out


def test_run_interactive_setup(capsys):
    """Test interactive setup wizard."""
    # Test with Claude Code not configured
    with patch("antimon.first_run.check_claude_code_setup", return_value="not_configured"):
        with patch("antimon.first_run.prompt_yes_no", side_effect=[True, True]):
            with patch("antimon.first_run.setup_claude_code_automatically", return_value=True):
                with patch("antimon.first_run.verify_setup", return_value=True):
                    run_interactive_setup(no_color=True)
                    captured = capsys.readouterr()
                    assert "antimon Setup Wizard" in captured.out
                    assert "Claude Code detected!" in captured.out
                    assert "Setup complete!" in captured.out
                    assert "Everything is working correctly!" in captured.out

    # Test with Claude Code already configured
    with patch("antimon.first_run.check_claude_code_setup", return_value="configured"):
        with patch("antimon.first_run.prompt_yes_no", return_value=False):
            run_interactive_setup(no_color=True)
            captured = capsys.readouterr()
            assert "Claude Code is already configured" in captured.out


def test_show_first_run_guide_interactive(capsys):
    """Test interactive first-run guide."""
    # Test in non-interactive mode (piped)
    with patch("sys.stdin.isatty", return_value=False):
        with patch("antimon.first_run.check_claude_code_setup", return_value="not_configured"):
            show_first_run_guide_interactive(no_color=True)
            captured = capsys.readouterr()
            # Should show regular guide
            assert "Welcome to antimon!" in captured.out
            assert "Quick Start:" in captured.out
            # Should suggest Claude Code setup
            assert "Claude Code detected but antimon not configured!" in captured.out

    # Test in interactive mode with wizard acceptance
    with patch("sys.stdin.isatty", return_value=True):
        with patch("antimon.first_run.prompt_yes_no", return_value=True):
            with patch("antimon.first_run.run_interactive_setup") as mock_setup:
                show_first_run_guide_interactive(no_color=True)
                mock_setup.assert_called_once_with(no_color=True)

    # Test in interactive mode with wizard rejection
    with patch("sys.stdin.isatty", return_value=True):
        with patch("antimon.first_run.prompt_yes_no", return_value=False):
            with patch("antimon.first_run.show_first_run_guide") as mock_guide:
                show_first_run_guide_interactive(no_color=True)
                mock_guide.assert_called_once_with(no_color=True)
