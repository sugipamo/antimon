#!/usr/bin/env python3
"""Test direct file and content checking functionality"""

import os
import tempfile

from antimon import check_content_directly, check_file_directly


class TestDirectFileCheck:
    """Test check_file_directly function"""

    def test_check_file_with_api_key(self):
        """Test checking a file with API key"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('api_key = "sk-1234567890abcdef"')
            f.flush()

            try:
                result = check_file_directly(f.name, quiet=True)
                assert result == 2  # Security issue detected
            finally:
                os.unlink(f.name)

    def test_check_file_safe_content(self):
        """Test checking a file with safe content"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('print("Hello, World!")')
            f.flush()

            try:
                result = check_file_directly(f.name, quiet=True)
                assert result == 0  # No issues
            finally:
                os.unlink(f.name)

    def test_check_nonexistent_file(self):
        """Test checking a file that doesn't exist"""
        result = check_file_directly("/nonexistent/file.py", quiet=True)
        assert result == 1  # Error

    def test_check_file_with_llm_api(self):
        """Test checking a file with LLM API usage"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("from openai import OpenAI\nclient = OpenAI()")
            f.flush()

            try:
                result = check_file_directly(f.name, quiet=True)
                assert result == 2  # Security issue detected
            finally:
                os.unlink(f.name)

    def test_check_file_with_docker(self):
        """Test checking a file with Docker operations"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('os.system("docker run ubuntu")')
            f.flush()

            try:
                result = check_file_directly(f.name, quiet=True)
                assert result == 2  # Security issue detected
            finally:
                os.unlink(f.name)


class TestDirectContentCheck:
    """Test check_content_directly function"""

    def test_check_content_with_api_key(self):
        """Test checking content with API key"""
        result = check_content_directly('api_key = "sk-1234567890abcdef"', quiet=True)
        assert result == 2  # Security issue detected

    def test_check_content_safe(self):
        """Test checking safe content"""
        result = check_content_directly('print("Hello, World!")', quiet=True)
        assert result == 0  # No issues

    def test_check_content_with_localhost(self):
        """Test checking content with localhost reference"""
        result = check_content_directly('url = "http://localhost:8080"', quiet=True)
        assert result == 2  # Security issue detected

    def test_check_content_multiple_issues(self):
        """Test checking content with multiple issues"""
        content = """
api_key = "sk-1234567890abcdef"
from openai import OpenAI
client = OpenAI()
"""
        result = check_content_directly(content, quiet=True)
        assert result == 2  # Security issue detected

    def test_check_content_with_custom_filename(self):
        """Test checking content with custom filename"""
        result = check_content_directly(
            'api_key = "sk-123"', file_name="config.py", quiet=True
        )
        assert result == 2  # Security issue detected

    def test_check_empty_content(self):
        """Test checking empty content"""
        result = check_content_directly("", quiet=True)
        assert result == 0  # No issues (empty content is safe)

    def test_check_content_environment_variable(self):
        """Test content using environment variables (should be safe)"""
        content = """
import os
api_key = os.environ.get('API_KEY')
openai_key = os.getenv('OPENAI_API_KEY', 'default')
"""
        result = check_content_directly(content, quiet=True)
        assert result == 0  # No issues (using env vars is safe)
