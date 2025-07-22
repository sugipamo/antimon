"""
Tests for dangerous Python code detection
"""

import pytest
from antimon.detectors import detect_dangerous_python_code


class TestDangerousPythonCodeDetection:
    """Test cases for dangerous Python code pattern detection.
    
    Validates detection of:
    - os.system() with dangerous commands
    - subprocess calls with shell=True
    - eval() and exec() with user input
    - __import__() dynamic imports
    - compile() with user input
    """
    
    def test_detect_os_system_rm_rf(self):
        """Test detection of os.system('rm -rf /')."""
        json_data = {
            "tool_input": {
                "file_path": "script.py",
                "content": "import os\nos.system('rm -rf /')"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "os.system" in result.message
        assert "dangerous command" in result.message.lower()
    
    def test_detect_subprocess_shell_true(self):
        """Test detection of subprocess with shell=True."""
        json_data = {
            "tool_input": {
                "file_path": "deploy.py",
                "content": "import subprocess\nsubprocess.run('echo $USER', shell=True)"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "shell=True" in result.message
    
    def test_detect_eval_with_input(self):
        """Test detection of eval() with user input."""
        json_data = {
            "tool_input": {
                "file_path": "calculator.py",
                "content": "user_input = input('Enter expression: ')\nresult = eval(user_input)"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "eval" in result.message
    
    def test_detect_exec_with_string(self):
        """Test detection of exec() with dynamic code."""
        json_data = {
            "tool_input": {
                "file_path": "dynamic.py",
                "content": "code = 'print(\"hello\")'\nexec(code)"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "exec" in result.message
    
    def test_detect_dunder_import(self):
        """Test detection of __import__() usage."""
        json_data = {
            "tool_input": {
                "file_path": "loader.py",
                "content": "module_name = 'os'\nmodule = __import__(module_name)"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "__import__" in result.message
    
    def test_detect_compile_function(self):
        """Test detection of compile() with user input."""
        json_data = {
            "tool_input": {
                "file_path": "compiler.py",
                "content": "code = input('Enter code: ')\ncompiled = compile(code, 'string', 'exec')"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "compile" in result.message
    
    def test_safe_python_code(self):
        """Test that normal Python code is not flagged."""
        json_data = {
            "tool_input": {
                "file_path": "safe.py",
                "content": "def hello():\n    print('Hello World')\n\nhello()"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is False
    
    def test_no_content_field(self):
        """Test behavior when content field is missing."""
        json_data = {
            "tool_input": {
                "file_path": "test.py"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is False
    
    def test_multiline_dangerous_code(self):
        """Test detection across multiple lines."""
        json_data = {
            "tool_input": {
                "file_path": "multiline.py",
                "content": """
import os
import subprocess

def dangerous_function():
    # This is dangerous
    os.system('rm -rf /tmp/*')
    
    # Also dangerous
    subprocess.call(['rm', '-rf', '/'], shell=True)
"""
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
    
    def test_detect_os_popen(self):
        """Test detection of os.popen() usage."""
        json_data = {
            "tool_input": {
                "file_path": "popen_test.py",
                "content": "import os\nresult = os.popen('ls -la').read()"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "os.popen" in result.message
    
    def test_detect_subprocess_popen_shell(self):
        """Test detection of subprocess.Popen with shell=True."""
        json_data = {
            "tool_input": {
                "file_path": "popen2.py",
                "content": "import subprocess\np = subprocess.Popen('echo test', shell=True)"
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "shell=True" in result.message
    
    def test_combined_with_other_content(self):
        """Test detection when dangerous code is mixed with safe code."""
        json_data = {
            "tool_input": {
                "file_path": "mixed.py",
                "content": """
# Safe imports
import json
import datetime

# Safe function
def get_date():
    return datetime.datetime.now()

# Dangerous code hidden in the middle
eval(input())

# More safe code
def process_data(data):
    return json.dumps(data)
"""
            }
        }
        result = detect_dangerous_python_code(json_data)
        assert result.detected is True
        assert "eval" in result.message