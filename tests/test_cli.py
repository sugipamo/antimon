"""
Tests for CLI behavior and exit codes
"""

import json
import subprocess
import sys
from pathlib import Path


class TestCLIExitCodes:
    """Test cases for CLI exit codes and output behavior."""
    
    def run_antimon(self, input_data: dict, args: list[str] = None) -> tuple[int, str, str]:
        """Helper to run antimon with JSON input and capture output."""
        cmd = [sys.executable, "-m", "antimon"]
        if args:
            cmd.extend(args)
        
        result = subprocess.run(
            cmd,
            input=json.dumps(input_data),
            text=True,
            capture_output=True
        )
        return result.returncode, result.stdout, result.stderr
    
    def test_exit_code_0_for_safe_operation(self):
        """Test that safe operations return exit code 0."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "hello.py",
                "content": "print('Hello World')"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data)
        assert exit_code == 0
        # In normal mode, no output for safe operations
        assert stdout == ""
        assert "Security issues detected" not in stderr
        assert "No security issues detected" not in stderr  # No success message in normal mode
    
    def test_exit_code_0_for_safe_tools(self):
        """Test that safe tools like Read return exit code 0."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/etc/passwd"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data)
        assert exit_code == 0
        # In normal mode, no output for safe tools
        assert stdout == ""
        assert "Tool 'Read' is considered safe" not in stderr  # No message in normal mode
    
    def test_exit_code_1_for_json_error(self):
        """Test that JSON parse errors return exit code 1."""
        cmd = [sys.executable, "-m", "antimon"]
        result = subprocess.run(
            cmd,
            input="not valid json",
            text=True,
            capture_output=True
        )
        assert result.returncode == 1
        assert "JSON parsing error" in result.stderr
        assert "How to fix:" in result.stderr
    
    def test_exit_code_2_for_security_issues(self):
        """Test that security issues return exit code 2."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/etc/passwd",
                "content": "malicious"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data)
        assert exit_code == 2
        assert "Security issues detected" in stderr
        assert "Dangerous file path" in stderr
    
    def test_exit_code_1_for_missing_content_field(self):
        """Test that missing required fields return exit code 1."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "test.py"
                # Missing 'content' field
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data)
        assert exit_code == 1
        assert "Missing required field 'content'" in stderr
        assert "How to fix:" in stderr
    
    def test_exit_code_1_for_missing_new_string_field(self):
        """Test that Edit tool with missing new_string returns exit code 1."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "test.py",
                "old_string": "foo"
                # Missing 'new_string' field
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data)
        assert exit_code == 1
        assert "Missing required field 'new_string'" in stderr
        assert "How to fix:" in stderr


class TestCLIOutputModes:
    """Test cases for different output modes (normal, verbose, quiet)."""
    
    def run_antimon(self, input_data: dict, args: list[str] = None) -> tuple[int, str, str]:
        """Helper to run antimon with JSON input and capture output."""
        cmd = [sys.executable, "-m", "antimon"]
        if args:
            cmd.extend(args)
        
        result = subprocess.run(
            cmd,
            input=json.dumps(input_data),
            text=True,
            capture_output=True
        )
        return result.returncode, result.stdout, result.stderr
    
    def test_quiet_mode_shows_security_issues(self):
        """Test that quiet mode still shows security issues."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/etc/passwd",
                "content": "test"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data, ["-q"])
        assert exit_code == 2
        assert "Security issues detected" in stderr
        assert "Dangerous file path" in stderr
        # But no "How to proceed" section in quiet mode
        assert "How to proceed:" not in stderr
    
    def test_quiet_mode_silent_for_safe_operations(self):
        """Test that quiet mode is silent for safe operations."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "hello.py",
                "content": "print('Hello')"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data, ["-q"])
        assert exit_code == 0
        assert stdout == ""
        assert stderr == ""  # Completely silent
    
    def test_verbose_mode_shows_details(self):
        """Test that verbose mode shows detailed information."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "hello.py",
                "content": "print('Hello')"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data, ["-v"])
        assert exit_code == 0
        # Verbose mode shows detection summary
        assert "Detection Summary:" in stderr
        assert "Total detectors run:" in stderr
        assert "Passed:" in stderr
    
    def test_verbose_mode_with_security_issues(self):
        """Test verbose mode output when security issues are found."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/etc/passwd",
                "content": "test"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data, ["--verbose"])
        assert exit_code == 2
        assert "Detection Results:" in stderr
        assert "File:" in stderr
        assert "Tool:" in stderr
        assert "Summary:" in stderr
        assert "failed" in stderr
    
    def test_verbose_mode_for_safe_tools(self):
        """Test verbose mode shows info for safe tools."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {
                "file_path": "/etc/passwd"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data, ["-v"])
        assert exit_code == 0
        assert "Tool 'Read' is considered safe" in stderr