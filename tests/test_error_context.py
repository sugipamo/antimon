# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for error context functionality
"""


from antimon.error_context import ErrorContext, show_error_help


def test_error_context_api_key():
    """Test error context for API key detection."""
    context = ErrorContext(no_color=True)

    message = "API key found in content"
    hook_data = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": "config.py",
            "content": "api_key = 'sk-123'"
        }
    }

    result = context.get_context_for_error(message, hook_data)

    assert "📄 File: config.py" in result
    assert "🔧 Tool: Write" in result
    assert "💡 Suggestions:" in result
    assert "Use environment variables instead" in result
    assert "Store secrets in a .env file" in result


def test_error_context_sensitive_file():
    """Test error context for sensitive file access."""
    context = ErrorContext(no_color=True)

    message = "Attempt to access sensitive file: /etc/passwd"
    hook_data = {
        "tool_name": "Read",
        "tool_input": {
            "file_path": "/etc/passwd"
        }
    }

    result = context.get_context_for_error(message, hook_data)

    assert "📄 File: /etc/passwd" in result
    assert "Use user-specific config files" in result
    assert "Read from project-local configuration" in result


def test_error_context_llm_api():
    """Test error context for LLM API detection."""
    context = ErrorContext(no_color=True)

    message = "External LLM API usage detected"
    hook_data = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": "chat.py",
            "content": "from openai import OpenAI"
        }
    }

    result = context.get_context_for_error(message, hook_data)

    assert "Consider using local models" in result
    assert "llama.cpp, ollama" in result
    assert "Use the AI assistant's built-in capabilities" in result


def test_format_error_with_context():
    """Test formatting error with full context."""
    context = ErrorContext(no_color=True)

    message = "API key found in content"
    hook_data = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": "config.py",
            "content": "key = 'secret'"
        }
    }

    result = context.format_error_with_context(message, hook_data)

    assert "❌ Security issue detected:" in result
    assert message in result
    assert "📄 File: config.py" in result
    assert "💡 Suggestions:" in result


def test_show_error_help(capsys):
    """Test showing error help."""
    show_error_help(no_color=True)

    captured = capsys.readouterr()
    assert "🆘 Dealing with antimon blocks:" in captured.out
    assert "Read the error message carefully" in captured.out
    assert "Check the suggestions" in captured.out
    assert "For false positives:" in captured.out
    assert "Need to bypass temporarily?" in captured.out
    assert "claude-code config unset hooks.PreToolUse" in captured.out
