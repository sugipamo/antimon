# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for batch file checking functionality
"""

import subprocess


class TestBatchFileCheck:
    """Test batch file checking with --check-files"""

    def test_check_files_no_matches(self):
        """Test --check-files with no matching files"""
        result = subprocess.run(
            ["python3", "-m", "antimon", "--check-files", "nonexistent/**/*.py"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "No files found matching pattern" in result.stderr

    def test_check_files_with_api_key(self, tmp_path):
        """Test --check-files with files containing API keys"""
        # Create test files
        (tmp_path / "file1.py").write_text('api_key = "sk-1234567890abcdef"')
        (tmp_path / "file2.py").write_text('print("hello world")')
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file3.py").write_text('openai.api_key = "sk-test"')

        # Run batch check
        result = subprocess.run(
            ["python3", "-m", "antimon", "--check-files", f"{tmp_path}/**/*.py"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2  # Security issues found
        assert "Checking 3 files" in result.stderr
        assert "Files with issues: 2" in result.stderr
        assert "file1.py" in result.stderr
        assert "file3.py" in result.stderr

    def test_check_files_all_safe(self, tmp_path):
        """Test --check-files with all safe files"""
        # Create safe test files
        (tmp_path / "safe1.py").write_text('print("hello")')
        (tmp_path / "safe2.py").write_text("def foo(): return 42")
        (tmp_path / "safe3.py").write_text("import os\nprint(os.getcwd())")

        # Run batch check
        result = subprocess.run(
            ["python3", "-m", "antimon", "--check-files", f"{tmp_path}/*.py"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Checking 3 files" in result.stderr
        assert "All files passed security checks!" in result.stderr

    def test_check_files_with_verbose(self, tmp_path):
        """Test --check-files with verbose mode"""
        # Create test file
        (tmp_path / "test.py").write_text('print("test")')

        # Run batch check with verbose
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-files",
                f"{tmp_path}/*.py",
                "--verbose",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "[1/1] Checking:" in result.stderr
        assert "test.py" in result.stderr

    def test_check_files_with_quiet(self, tmp_path):
        """Test --check-files with quiet mode"""
        # Create test file with issue
        (tmp_path / "bad.py").write_text('api_key = "sk-test123"')

        # Run batch check with quiet
        result = subprocess.run(
            [
                "python3",
                "-m",
                "antimon",
                "--check-files",
                f"{tmp_path}/*.py",
                "--quiet",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        # In quiet mode, should only show errors
        assert "Hardcoded API key detected" in result.stderr
        assert "Batch Check Summary" not in result.stderr

    def test_check_files_mixed_results(self, tmp_path):
        """Test --check-files with mixed safe and unsafe files"""
        # Create a mix of files
        (tmp_path / "safe.py").write_text('# Safe file\nprint("hello")')
        (tmp_path / "api.py").write_text('api_key = "sk-secret"')
        (tmp_path / "docker.py").write_text("docker run -it ubuntu")
        (tmp_path / "normal.py").write_text("def main(): pass")

        # Run batch check
        result = subprocess.run(
            ["python3", "-m", "antimon", "--check-files", f"{tmp_path}/*.py"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        assert "Checking 4 files" in result.stderr
        assert "Files with issues: 2" in result.stderr
        assert "api.py" in result.stderr
        assert "docker.py" in result.stderr

    def test_check_files_with_subdirectories(self, tmp_path):
        """Test --check-files with nested directories"""
        # Create nested structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text('print("main")')
        (tmp_path / "src" / "lib").mkdir()
        (tmp_path / "src" / "lib" / "util.py").write_text('api_key = "sk-123"')
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test.py").write_text("assert True")

        # Run batch check with recursive pattern
        result = subprocess.run(
            ["python3", "-m", "antimon", "--check-files", f"{tmp_path}/**/*.py"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        assert "Checking 3 files" in result.stderr
        assert "Files with issues: 1" in result.stderr
        assert "util.py" in result.stderr

    def test_check_files_empty_pattern(self):
        """Test --check-files with empty pattern"""
        result = subprocess.run(
            ["python3", "-m", "antimon", "--check-files", "*.nonexistent"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "No files found" in result.stderr

    def test_check_files_timing_info(self, tmp_path):
        """Test that batch check shows timing information"""
        # Create a few files
        for i in range(5):
            (tmp_path / f"file{i}.py").write_text(f'print("file {i}")')

        # Run batch check
        result = subprocess.run(
            ["python3", "-m", "antimon", "--check-files", f"{tmp_path}/*.py"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Total time:" in result.stderr
        assert "Checking 5 files" in result.stderr
