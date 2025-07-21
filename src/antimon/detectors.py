"""
Detection modules for various security patterns
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import re


@dataclass
class DetectionResult:
    """Result of a detection check"""

    detected: bool
    message: str = ""
    severity: str = "error"
    details: Optional[Dict[str, Any]] = None


def detect_filenames(json_data: Dict[str, Any]) -> DetectionResult:
    """
    Detect dangerous or sensitive file paths

    Args:
        json_data: Hook data containing file path information

    Returns:
        DetectionResult indicating if dangerous paths were detected
    """
    dangerous_patterns = [
        r"/etc/passwd",
        r"/etc/shadow",
        r"\.ssh/id_rsa",
        r"\.ssh/id_ed25519",
        r"secrets\.yaml",
        r"credentials\.json",
        r"\.env$",
        r"\.pem$",
        r"\.key$",
        r"\.p12$",
        r"\.pfx$",
        r"deploy_key",
    ]

    file_path = json_data.get("tool_input", {}).get("file_path", "")

    for pattern in dangerous_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            return DetectionResult(
                detected=True,
                message=f"Dangerous file path detected: {file_path}",
                details={"pattern": pattern, "file_path": file_path},
            )

    return DetectionResult(detected=False)


def detect_llm_api(json_data: Dict[str, Any]) -> DetectionResult:
    """
    Detect references to external LLM APIs

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if LLM API references were detected
    """
    llm_patterns = [
        r"openai\.com",
        r"api\.openai\.com",
        r"gemini\.google\.com",
        r"gpt-[0-9]",
        r"claude\.ai",
        r"anthropic\.com",
        r"cohere\.ai",
        r"huggingface\.co",
        r"import\s+openai",
        r"from\s+openai",
        r"openai\.",
        r"import\s+anthropic",
        r"from\s+anthropic",
        r"anthropic\.",
        r"import\s+cohere",
        r"from\s+cohere",
        r"cohere\.",
        r"import\s+google\.generativeai",
        r"from\s+google\.generativeai",
    ]

    content = json_data.get("tool_input", {}).get("content", "")

    for pattern in llm_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return DetectionResult(
                detected=True,
                message=f"External LLM API reference detected: {pattern}",
                details={"pattern": pattern},
            )

    return DetectionResult(detected=False)


def detect_api_key(json_data: Dict[str, Any]) -> DetectionResult:
    """
    Detect hardcoded API keys in content

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if API keys were detected
    """
    api_key_patterns = [
        r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
        r'apikey\s*:\s*["\'][^"\']+["\']',
        r'secret[_-]?key\s*=\s*["\'][^"\']+["\']',
        r'access[_-]?token\s*=\s*["\'][^"\']+["\']',
        r"bearer\s+[a-zA-Z0-9\-\._~\+\/]+=*",
        r"sk-[a-zA-Z0-9]{48}",  # OpenAI style
        r"AIza[0-9A-Za-z\-_]{35}",  # Google API
    ]

    content = json_data.get("tool_input", {}).get("content", "")

    for pattern in api_key_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return DetectionResult(
                detected=True,
                message="Hardcoded API key detected",
                details={"pattern": pattern},
            )

    return DetectionResult(detected=False)


def detect_docker(json_data: Dict[str, Any]) -> DetectionResult:
    """
    Detect Docker-related operations

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if Docker operations were detected
    """
    docker_patterns = [
        r"docker\s+run",
        r"docker\s+build",
        r"docker-compose",
        r"dockerfile",
        r"docker\s+exec",
        r"docker\s+pull",
        r"docker\s+push",
    ]

    content = json_data.get("tool_input", {}).get("content", "")
    file_path = json_data.get("tool_input", {}).get("file_path", "")

    check_content = f"{content} {file_path}"

    for pattern in docker_patterns:
        if re.search(pattern, check_content, re.IGNORECASE):
            return DetectionResult(
                detected=True,
                message="Docker operation detected",
                details={"pattern": pattern},
            )

    return DetectionResult(detected=False)


def detect_localhost(json_data: Dict[str, Any]) -> DetectionResult:
    """
    Detect localhost and port references

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if localhost references were detected
    """
    localhost_patterns = [
        r"localhost:[0-9]+",
        r"127\.0\.0\.1:[0-9]+",
        r"0\.0\.0\.0:[0-9]+",
        r":\s*(3000|8000|8080|5000|5432|3306)\b",
    ]

    content = json_data.get("tool_input", {}).get("content", "")

    for pattern in localhost_patterns:
        if re.search(pattern, content):
            return DetectionResult(
                detected=True,
                message="Localhost/port reference detected",
                details={"pattern": pattern},
            )

    return DetectionResult(detected=False)


def detect_claude_antipatterns(json_data: Dict[str, Any]) -> DetectionResult:
    """
    Use Claude to detect anti-patterns and workarounds

    Note: This is a placeholder for Claude-based detection.
    In a real implementation, this would make an API call to Claude.

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if anti-patterns were detected
    """
    # Placeholder implementation
    # In production, this would make an actual Claude API call
    return DetectionResult(
        detected=False, message="Claude anti-pattern detection not implemented yet"
    )
