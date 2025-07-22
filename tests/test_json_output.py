# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for JSON output format functionality
"""

import json
import subprocess

import pytest


class TestJSONOutput:
    """Test JSON output format with --output-format json"""

    def test_check_files_json_output(self, tmp_path):
        """Test --check-files with JSON output format"""
        # Create test files
        (tmp_path / "file1.py").write_text('api_key = "sk-1234567890abcdef"')
        (tmp_path / "file2.py").write_text('print("hello world")')
        (tmp_path / "file3.py").write_text('openai.api_key = "sk-test"')

        # Run batch check with JSON output
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-files",
                f"{tmp_path}/*.py",
                "--output-format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2  # Security issues found

        # Parse JSON output
        output = json.loads(result.stdout)

        assert output["files_checked"] == 3
        assert output["files_with_issues"] == 2
        assert not output["success"]
        assert len(output["issues"]) == 2
        assert any("file1.py" in issue for issue in output["issues"])
        assert any("file3.py" in issue for issue in output["issues"])
        assert "total_time" in output
        assert output["pattern"] == f"{tmp_path}/*.py"

    def test_check_files_json_output_no_issues(self, tmp_path):
        """Test --check-files with JSON output when all files are safe"""
        # Create safe test files
        (tmp_path / "safe1.py").write_text('print("hello")')
        (tmp_path / "safe2.py").write_text("def foo(): return 42")

        # Run batch check with JSON output
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-files",
                f"{tmp_path}/*.py",
                "--output-format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Parse JSON output
        output = json.loads(result.stdout)

        assert output["files_checked"] == 2
        assert output["files_with_issues"] == 0
        assert output["success"]
        assert len(output["issues"]) == 0
        assert "total_time" in output

    def test_check_file_json_output(self, tmp_path):
        """Test --check-file with JSON output format"""
        # Create test file
        test_file = tmp_path / "test.py"
        test_file.write_text('api_key = "sk-secret"')

        # Run file check with JSON output
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-file",
                str(test_file),
                "--output-format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        # For single file check, JSON output might need to be implemented
        # This test documents expected behavior
        assert result.returncode == 2

    def test_check_content_json_output(self):
        """Test --check-content with JSON output format"""
        # Run content check with JSON output
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-content",
                'api_key = "sk-123"',
                "--output-format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        # For content check, JSON output might need to be implemented
        # This test documents expected behavior
        assert result.returncode == 2

    def test_json_output_with_quiet(self, tmp_path):
        """Test JSON output with quiet mode"""
        # Create test file
        (tmp_path / "bad.py").write_text('api_key = "sk-test123"')

        # Run with both JSON output and quiet mode
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-files",
                f"{tmp_path}/*.py",
                "--output-format",
                "json",
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2

        # JSON output should still work in quiet mode
        output = json.loads(result.stdout)
        assert output["files_with_issues"] == 1

    def test_json_output_machine_readable(self, tmp_path):
        """Test that JSON output is properly formatted for machine parsing"""
        # Create test files
        for i in range(5):
            content = 'api_key = "sk-test"' if i % 2 == 0 else 'print("safe")'
            (tmp_path / f"file{i}.py").write_text(content)

        # Run batch check
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-files",
                f"{tmp_path}/*.py",
                "--output-format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        # Verify JSON is valid
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            pytest.fail("Output is not valid JSON")

        # Verify structure
        assert isinstance(output, dict)
        assert isinstance(output["files_checked"], int)
        assert isinstance(output["files_with_issues"], int)
        assert isinstance(output["success"], bool)
        assert isinstance(output["issues"], list)
        assert isinstance(output["total_time"], float)
