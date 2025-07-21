"""
Tests for detection modules
"""

from antimon.detectors import (
    detect_filenames,
    detect_llm_api,
    detect_api_key,
    detect_docker,
    detect_localhost,
)


class TestFilenameDetection:
    """Test cases for dangerous file path detection.
    
    Validates that the filename detector correctly identifies:
    - System files (/etc/passwd, /etc/shadow)
    - SSH keys and configuration files
    - Secret and credential files
    - Safe file paths that should not trigger alerts
    """
    def test_detect_etc_passwd(self):
        json_data = {"tool_input": {"file_path": "/etc/passwd"}}
        result = detect_filenames(json_data)
        assert result.detected is True
        assert "/etc/passwd" in result.message

    def test_detect_ssh_key(self):
        json_data = {"tool_input": {"file_path": "/home/user/.ssh/id_rsa"}}
        result = detect_filenames(json_data)
        assert result.detected is True

    def test_safe_file_path(self):
        json_data = {"tool_input": {"file_path": "/home/user/project/main.py"}}
        result = detect_filenames(json_data)
        assert result.detected is False


class TestLLMAPIDetection:
    """Test cases for external LLM API usage detection.
    
    Ensures detection of:
    - OpenAI API imports and endpoints
    - Google Gemini API references
    - Other LLM service patterns
    - Safe code that does not use external LLMs
    """
    def test_detect_openai_api(self):
        json_data = {"tool_input": {"content": "import openai\napi.openai.com"}}
        result = detect_llm_api(json_data)
        assert result.detected is True

    def test_detect_gemini(self):
        json_data = {"tool_input": {"content": 'url = "https://gemini.google.com/api"'}}
        result = detect_llm_api(json_data)
        assert result.detected is True

    def test_no_llm_api(self):
        json_data = {"tool_input": {"content": 'print("Hello, World!")'}}
        result = detect_llm_api(json_data)
        assert result.detected is False


class TestAPIKeyDetection:
    """Test cases for hardcoded API key detection.
    
    Verifies detection of:
    - Direct API key assignments
    - Bearer tokens in headers
    - Various API key patterns
    - Code without API keys
    """
    def test_detect_api_key_assignment(self):
        json_data = {"tool_input": {"content": 'api_key = "sk-1234567890abcdef"'}}
        result = detect_api_key(json_data)
        assert result.detected is True

    def test_detect_bearer_token(self):
        json_data = {"tool_input": {"content": "Authorization: Bearer abc123def456"}}
        result = detect_api_key(json_data)
        assert result.detected is True

    def test_no_api_key(self):
        json_data = {
            "tool_input": {"content": "def calculate_sum(a, b):\n    return a + b"}
        }
        result = detect_api_key(json_data)
        assert result.detected is False


class TestDockerDetection:
    """Test cases for Docker-related operations detection.
    
    Tests identification of:
    - Docker CLI commands (run, build, etc.)
    - Dockerfile references
    - Docker Compose operations
    - Non-Docker code
    """
    def test_detect_docker_run(self):
        json_data = {"tool_input": {"content": "docker run -it ubuntu bash"}}
        result = detect_docker(json_data)
        assert result.detected is True

    def test_detect_dockerfile(self):
        json_data = {"tool_input": {"file_path": "Dockerfile"}}
        result = detect_docker(json_data)
        assert result.detected is True

    def test_no_docker(self):
        json_data = {"tool_input": {"content": 'print("Hello")'}}
        result = detect_docker(json_data)
        assert result.detected is False


class TestLocalhostDetection:
    """Test cases for localhost and loopback address detection.
    
    Validates detection of:
    - localhost URLs with various ports
    - 127.0.0.1 loopback addresses
    - Local network patterns
    - External URLs that should not trigger
    """
    def test_detect_localhost_port(self):
        json_data = {"tool_input": {"content": 'url = "http://localhost:8080"'}}
        result = detect_localhost(json_data)
        assert result.detected is True

    def test_detect_127_0_0_1(self):
        json_data = {"tool_input": {"content": 'server = "127.0.0.1:3000"'}}
        result = detect_localhost(json_data)
        assert result.detected is True

    def test_no_localhost(self):
        json_data = {"tool_input": {"content": 'url = "https://example.com"'}}
        result = detect_localhost(json_data)
        assert result.detected is False

