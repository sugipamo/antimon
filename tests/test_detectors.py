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
