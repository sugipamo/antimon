"""Test success message improvements for version 0.2.12"""

import json
import subprocess
import sys
import tempfile
import os
import pytest


class TestSuccessMessages:
    """Test that success messages show helpful information about what was checked."""
    
    def run_antimon(self, data, args=None):
        """Helper to run antimon with JSON data and return results."""
        if args is None:
            args = []
        cmd = [sys.executable, "-m", "antimon"] + args
        result = subprocess.run(
            cmd,
            input=json.dumps(data),
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    
    def test_check_file_success_message(self):
        """Test that --check-file shows detailed success information."""
        # Create a test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("# Safe Python file\nprint('Hello, world!')\n")
            temp_file = f.name
        
        try:
            cmd = [sys.executable, "-m", "antimon", "--check-file", temp_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            assert result.returncode == 0
            assert "Success:" in result.stderr
            assert "No security issues found" in result.stderr
            assert f"File: {temp_file}" in result.stderr
            assert "Size:" in result.stderr
            assert "KB" in result.stderr
            assert "bytes" in result.stderr
            assert "Checks performed:" in result.stderr
            assert "security detectors" in result.stderr
        finally:
            os.unlink(temp_file)
    
    def test_check_content_success_message(self):
        """Test that --check-content shows detailed success information."""
        content = "def safe_function():\n    return 42\n"
        cmd = [sys.executable, "-m", "antimon", "--check-content", content]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "Success:" in result.stderr
        assert "No security issues found" in result.stderr
        assert "Content size:" in result.stderr
        assert "bytes" in result.stderr
        assert "Lines:" in result.stderr
        assert "Checks performed:" in result.stderr
        assert "security detectors" in result.stderr
    
    def test_json_input_success_message(self):
        """Test that JSON input shows enhanced success information."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "test.py",
                "content": "print('Hello')"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data)
        
        assert exit_code == 0
        assert "Success:" in stderr
        assert "No security issues found" in stderr
        assert "Tool: Write" in stderr
        assert "File: test.py" in stderr
        assert "Content:" in stderr
        assert "bytes" in stderr
        assert "Checks performed:" in stderr
        assert "security detectors" in stderr
    
    def test_quiet_mode_no_success_message(self):
        """Test that quiet mode still suppresses success messages."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "safe.py",
                "content": "x = 1"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data, ["--quiet"])
        
        assert exit_code == 0
        assert stderr == ""  # No output in quiet mode
    
    def test_verbose_mode_detailed_stats(self):
        """Test that verbose mode shows detailed statistics instead of simple message."""
        data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "test.py",
                "content": "x = 1"
            }
        }
        exit_code, stdout, stderr = self.run_antimon(data, ["--verbose"])
        
        assert exit_code == 0
        assert "Detection Summary:" in stderr
        assert "Total detectors run:" in stderr
        assert "Passed:" in stderr
        assert "Failed:" in stderr
        # Should not show the simple success message in verbose mode
        assert "Success:" not in stderr or "passed all security checks" in stderr
    
    def test_large_file_size_formatting(self):
        """Test that large file sizes are formatted nicely."""
        # Create a larger test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Write ~10KB of content
            content = "# Comment line\n" * 700
            f.write(content)
            temp_file = f.name
        
        try:
            cmd = [sys.executable, "-m", "antimon", "--check-file", temp_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            assert result.returncode == 0
            # Check that size is shown with comma separator for bytes
            assert "," in result.stderr  # e.g., "10,500 bytes"
            assert "KB" in result.stderr
        finally:
            os.unlink(temp_file)