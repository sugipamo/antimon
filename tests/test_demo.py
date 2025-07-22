# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for the demo module
"""

from unittest.mock import patch

import pytest

from antimon.demo import InteractiveDemo, run_demo


def test_demo_cases_structure():
    """Test that demo cases are properly structured."""
    demo = InteractiveDemo()
    assert len(demo.demo_cases) == 10  # We have 10 demo cases

    for desc, hook_data, should_fail, explanation in demo.demo_cases:
        # Check structure
        assert isinstance(desc, str)
        assert isinstance(hook_data, dict)
        assert isinstance(should_fail, bool)
        assert isinstance(explanation, str)

        # Check hook_data structure
        assert "hook_event_name" in hook_data
        assert "tool_name" in hook_data
        assert "tool_input" in hook_data
        assert hook_data["hook_event_name"] == "PreToolUse"
        assert hook_data["tool_name"] in ["Write", "Read", "Edit"]


def test_blocked_operations():
    """Test that dangerous operations are correctly marked as blocked."""
    demo = InteractiveDemo()

    blocked_descriptions = [
        "Attempt to write to /etc/passwd",
        "Hardcoded API key in Python code",
        "Reading SSH private key",
        "Using OpenAI API in code",
        "Creating a Dockerfile",
        "Connecting to localhost service",
        "Writing to .env file",
        "Editing code to add API key",
    ]

    for desc, _, should_fail, _ in demo.demo_cases:
        if desc in blocked_descriptions:
            assert should_fail, f"{desc} should be marked as blocked"


def test_allowed_operations():
    """Test that safe operations are correctly marked as allowed."""
    demo = InteractiveDemo()

    allowed_descriptions = ["Writing a simple Python script", "Reading a README file"]

    for desc, _, should_fail, _ in demo.demo_cases:
        if desc in allowed_descriptions:
            assert not should_fail, f"{desc} should be marked as allowed"


@patch("antimon.demo.input")
@patch("antimon.demo.print")
def test_demo_exit(mock_print, mock_input):
    """Test that demo exits properly when user chooses '0'."""
    mock_input.return_value = "0"

    demo = InteractiveDemo()
    demo.run()

    # Check that success message was printed
    # The demo uses _print_success which adds color codes conditionally
    success_call = None
    for call in mock_print.call_args_list:
        if len(call[0]) > 0 and "Thank you for trying antimon!" in str(call[0][0]):
            success_call = call
            break
    assert success_call is not None, "Success message not found in print calls"


@patch("antimon.demo.input")
@patch("antimon.demo.print")
@patch("antimon.demo.validate_hook_data")
def test_single_demo_execution(mock_validate, mock_print, mock_input):
    """Test running a single demo case."""
    # Choose demo 1, then exit
    mock_input.side_effect = ["1", "0"]
    mock_validate.return_value = (
        True,
        ["Attempt to access sensitive file: /etc/passwd"],
    )

    demo = InteractiveDemo()
    demo.run()

    # Verify validation was called with correct data
    mock_validate.assert_called_once()
    call_args = mock_validate.call_args[0][0]
    assert call_args["tool_input"]["file_path"] == "/etc/passwd"


@patch("antimon.demo.input")
@patch("antimon.demo.print")
def test_invalid_choice(mock_print, mock_input):
    """Test handling of invalid menu choices."""
    # Invalid choice, then exit
    mock_input.side_effect = ["invalid", "0"]

    demo = InteractiveDemo()
    demo.run()

    # Check that error message was printed
    # The demo uses _print_error which adds color codes conditionally
    error_call = None
    for call in mock_print.call_args_list:
        if len(call[0]) > 0 and "Invalid choice. Please try again." in str(call[0][0]):
            error_call = call
            break
    assert error_call is not None, "Error message not found in print calls"


@patch("antimon.demo.input")
@patch("antimon.demo.print")
@patch("antimon.demo.validate_hook_data")
def test_custom_demo_write(mock_validate, mock_print, mock_input):
    """Test custom demo mode with Write tool."""
    # Choose custom demo, provide inputs, then exit
    mock_input.side_effect = [
        "c",  # Choose custom demo
        "Write",  # Tool name
        "test.py",  # File path
        "print()",  # Content line 1
        "END",  # End content
        "0",  # Exit
    ]
    mock_validate.return_value = (False, [])

    demo = InteractiveDemo()
    demo.run()

    # Verify validation was called with custom data
    assert mock_validate.called
    call_args = mock_validate.call_args[0][0]
    assert call_args["tool_name"] == "Write"
    assert call_args["tool_input"]["file_path"] == "test.py"
    assert call_args["tool_input"]["content"] == "print()"


@patch("antimon.demo.input")
@patch("antimon.demo.print")
def test_custom_demo_invalid_tool(mock_print, mock_input):
    """Test custom demo mode with invalid tool name."""
    # Choose custom demo, provide invalid tool, then exit
    mock_input.side_effect = [
        "c",  # Choose custom demo
        "InvalidTool",  # Invalid tool name
        "0",  # Exit
    ]

    demo = InteractiveDemo()
    demo.run()

    # Check that error message was printed
    # The demo uses _print_error which adds color codes conditionally
    error_call = None
    for call in mock_print.call_args_list:
        if len(call[0]) > 0 and "Invalid tool name" in str(call[0][0]):
            error_call = call
            break
    assert error_call is not None, "Error message not found in print calls"


def test_run_demo_function():
    """Test the run_demo entry point function."""
    with patch.object(InteractiveDemo, "run") as mock_run:
        run_demo()
        mock_run.assert_called_once()


def test_keyboard_interrupt():
    """Test handling of keyboard interrupt."""
    with patch.object(InteractiveDemo, "run", side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit) as exc_info:
            run_demo()
        assert exc_info.value.code == 0
