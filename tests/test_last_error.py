# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for last error tracking
"""

from unittest.mock import patch

from antimon.last_error import (
    explain_last_error,
    load_last_error,
    save_last_error,
)


def test_save_and_load_last_error(tmp_path):
    """Test saving and loading last error."""
    # Mock the config directory
    with patch("antimon.first_run.get_config_dir", return_value=tmp_path / "antimon"):
        issues = ["API key found in content", "Sensitive file access detected"]
        hook_data = {
            "tool_name": "Write",
            "tool_input": {"file_path": "config.py", "content": "api_key = 'sk-123'"},
        }

        # Save error
        save_last_error(issues, hook_data)

        # Load error
        loaded = load_last_error()

        assert loaded is not None
        assert loaded["issues"] == issues
        assert loaded["tool_name"] == "Write"
        assert loaded["file_path"] == "config.py"
        assert "timestamp" in loaded


def test_load_last_error_no_file(tmp_path):
    """Test loading when no error file exists."""
    with patch("antimon.first_run.get_config_dir", return_value=tmp_path / "antimon"):
        loaded = load_last_error()
        assert loaded is None


def test_explain_last_error_no_error(tmp_path, capsys):
    """Test explaining when no error exists."""
    with patch("antimon.first_run.get_config_dir", return_value=tmp_path / "antimon"):
        explain_last_error(no_color=True)

        captured = capsys.readouterr()
        assert "No recent errors found" in captured.out
        assert "Run it after antimon blocks an operation" in captured.out


def test_explain_last_error_with_error(tmp_path, capsys):
    """Test explaining a saved error."""
    with patch("antimon.first_run.get_config_dir", return_value=tmp_path / "antimon"):
        # Save an error first
        issues = ["API key found in content", "External LLM API usage detected"]
        hook_data = {
            "tool_name": "Write",
            "tool_input": {"file_path": "bot.py", "content": "openai_key = 'sk-123'"},
        }
        save_last_error(issues, hook_data)

        # Explain it
        explain_last_error(no_color=True)

        captured = capsys.readouterr()
        assert "📋 Last Error Details" in captured.out
        assert "🔧 Tool: Write" in captured.out
        assert "📄 File: bot.py" in captured.out
        assert "❌ Issues detected:" in captured.out
        assert "API key found in content" in captured.out
        assert "External LLM API usage detected" in captured.out

        # Check for explanations - more specific patterns for new format
        assert "API Key Detection:" in captured.out
        assert "dangerous" in captured.out.lower()
        assert (
            "LLM API Detection:" in captured.out
            or "External LLM API Detection:" in captured.out
        )
        assert "leave" in captured.out.lower() or "control" in captured.out.lower()

        # Check for solutions
        assert "For API Keys:" in captured.out
        assert "api_key = os.environ.get('API_KEY')" in captured.out
        assert "For LLM APIs:" in captured.out
        assert "Using Claude's built-in capabilities" in captured.out

        # Check bypass instructions
        assert "If you need to bypass temporarily:" in captured.out
        assert "claude-code config unset hooks.PreToolUse" in captured.out
