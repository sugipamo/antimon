# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Detection modules for various security patterns
"""

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class DetectionResult:
    """Result of a detection check"""

    detected: bool
    message: str = ""
    severity: str = "error"
    details: dict[str, Any] | None = None


def detect_filenames(json_data: dict[str, Any]) -> DetectionResult:
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
                message=f"Dangerous file path detected: {file_path}\n" +
                        f"      Pattern matched: {pattern}\n" +
                        f"      Why: This appears to be a sensitive system or credential file\n" +
                        f"      Suggestion: Use environment variables or secure key management services instead",
                details={"pattern": pattern, "file_path": file_path},
            )

    return DetectionResult(detected=False)


def detect_llm_api(json_data: dict[str, Any]) -> DetectionResult:
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

    # Check content field (for Write tool) and new_string field (for Edit/MultiEdit)
    tool_input = json_data.get("tool_input", {})
    content = tool_input.get("content", "")
    new_string = tool_input.get("new_string", "")

    # For MultiEdit, check all edits
    edits = tool_input.get("edits", [])
    all_content = [content, new_string]
    for edit in edits:
        all_content.append(edit.get("new_string", ""))

    for text in all_content:
        if not text:
            continue
        for pattern in llm_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return DetectionResult(
                    detected=True,
                    message=f"External LLM API reference detected\n" +
                            f"      Pattern matched: {pattern}\n" +
                            f"      Why: Direct API calls to external LLMs may expose sensitive data\n" +
                            f"      Suggestion: Use Claude Code's built-in capabilities or proxy through a secure backend",
                    details={"pattern": pattern},
                )

    return DetectionResult(detected=False)


def detect_api_key(json_data: dict[str, Any]) -> DetectionResult:
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

    # Check content field (for Write tool) and new_string field (for Edit/MultiEdit)
    tool_input = json_data.get("tool_input", {})
    content = tool_input.get("content", "")
    new_string = tool_input.get("new_string", "")

    # For MultiEdit, check all edits
    edits = tool_input.get("edits", [])
    all_content = [content, new_string]
    for edit in edits:
        all_content.append(edit.get("new_string", ""))

    for text in all_content:
        if not text:
            continue
        for pattern in api_key_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return DetectionResult(
                    detected=True,
                    message=f"Hardcoded API key or secret detected\n" +
                            f"      Pattern matched: {pattern}\n" +
                            f"      Why: Hardcoded credentials are a security risk\n" +
                            f"      Suggestion: Use environment variables (e.g., os.getenv('API_KEY')) or secure vaults",
                    details={"pattern": pattern},
                )

    return DetectionResult(detected=False)


def detect_docker(json_data: dict[str, Any]) -> DetectionResult:
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

    # Check content field (for Write tool) and new_string field (for Edit/MultiEdit)
    tool_input = json_data.get("tool_input", {})
    content = tool_input.get("content", "")
    new_string = tool_input.get("new_string", "")
    file_path = tool_input.get("file_path", "")

    # For MultiEdit, check all edits
    edits = tool_input.get("edits", [])
    all_content = [content, new_string, file_path]
    for edit in edits:
        all_content.append(edit.get("new_string", ""))

    for text in all_content:
        if not text:
            continue
        for pattern in docker_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return DetectionResult(
                    detected=True,
                    message=f"Docker operation detected\n" +
                            f"      Pattern matched: {pattern}\n" +
                            f"      Why: Docker operations can pose security risks if not properly configured\n" +
                            f"      Suggestion: Review Docker commands for security best practices",
                    details={"pattern": pattern},
                )

    return DetectionResult(detected=False)


def detect_localhost(json_data: dict[str, Any]) -> DetectionResult:
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

    # Check content field (for Write tool) and new_string field (for Edit/MultiEdit)
    tool_input = json_data.get("tool_input", {})
    content = tool_input.get("content", "")
    new_string = tool_input.get("new_string", "")

    # For MultiEdit, check all edits
    edits = tool_input.get("edits", [])
    all_content = [content, new_string]
    for edit in edits:
        all_content.append(edit.get("new_string", ""))

    for text in all_content:
        if not text:
            continue
        for pattern in localhost_patterns:
            if re.search(pattern, text):
                return DetectionResult(
                    detected=True,
                    message=f"Localhost/port reference detected\n" +
                            f"      Pattern matched: {pattern}\n" +
                            f"      Why: Hardcoded localhost references may not work in production\n" +
                            f"      Suggestion: Use configuration files or environment variables for host/port settings",
                    details={"pattern": pattern},
                )

    return DetectionResult(detected=False)


def detect_claude_antipatterns(json_data: dict[str, Any]) -> DetectionResult:
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
