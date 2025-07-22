# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Detection modules for various security patterns
"""

import re
from dataclasses import dataclass
from typing import Any, TypedDict

from .runtime_config import get_runtime_config


class ToolInput(TypedDict, total=False):
    """Type definition for tool input data."""

    file_path: str
    content: str
    new_string: str
    old_string: str
    command: str


class HookData(TypedDict, total=False):
    """Type definition for hook data structure."""

    hook_event_name: str
    tool_name: str
    tool_input: ToolInput


@dataclass
class DetectionResult:
    """Result of a detection check"""

    detected: bool
    message: str = ""
    severity: str = "error"
    details: dict[str, Any] | None = None


def find_line_number(text: str, pattern_match: re.Match[str]) -> int:
    """
    Find the line number where a pattern match occurs

    Args:
        text: The full text
        pattern_match: The regex match object

    Returns:
        Line number (1-indexed)
    """
    start_pos = pattern_match.start()
    return text[:start_pos].count("\n") + 1


def detect_filenames(json_data: HookData) -> DetectionResult:
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

    # Check if file is explicitly allowed or ignored
    config = get_runtime_config()
    if config.is_file_allowed(file_path) or config.is_file_ignored(file_path):
        return DetectionResult(detected=False)

    for pattern in dangerous_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            # Provide more specific context based on the pattern
            if "/etc/" in pattern:
                file_type = "system configuration file"
                risk = "could expose system settings or user credentials"
                suggestion = (
                    "Use application-specific config files in your project directory"
                )
            elif ".ssh" in pattern:
                file_type = "SSH key file"
                risk = "could compromise server access and authentication"
                suggestion = "Never modify SSH keys programmatically. Use ssh-keygen or ssh-agent instead"
            elif ".env" in pattern:
                file_type = "environment variables file"
                risk = "often contains API keys and secrets"
                suggestion = "Read environment variables at runtime using os.environ or process.env"
            elif pattern in [r"\.pem$", r"\.key$", r"\.p12$", r"\.pfx$"]:
                file_type = "cryptographic key or certificate"
                risk = "could compromise encryption and authentication"
                suggestion = "Use proper key management services (AWS KMS, HashiCorp Vault, etc.)"
            elif "credentials" in pattern or "secrets" in pattern:
                file_type = "credentials file"
                risk = "likely contains authentication tokens or passwords"
                suggestion = (
                    "Use secure secret management solutions or environment variables"
                )
            else:
                file_type = "sensitive file"
                risk = "may contain confidential information"
                suggestion = "Review if this file really needs to be accessed"

            message_parts = [
                f"Attempting to access {file_type}: {file_path}",
                f"      Type: {file_type}",
                f"      Risk: {risk}",
                f"      Suggestion: {suggestion}",
                f"      To allow this specific file: antimon --allow-file '{file_path}'",
            ]
            return DetectionResult(
                detected=True,
                message="\n".join(message_parts),
                details={"pattern": pattern, "file_path": file_path},
            )

    return DetectionResult(detected=False)


def detect_llm_api(json_data: HookData) -> DetectionResult:
    """
    Detect references to external LLM APIs

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if LLM API references were detected
    """
    # Check if file is ignored
    file_path = json_data.get("tool_input", {}).get("file_path", "")
    config = get_runtime_config()
    if file_path and config.is_file_ignored(file_path):
        return DetectionResult(detected=False)

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
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                line_num = find_line_number(text, match)
                matched_text = match.group(0)
                # Determine which LLM service is being referenced
                if "openai" in matched_text.lower():
                    service = "OpenAI"
                    local_alt = "ollama with llama2 or mistral models"
                    import_alt = "# Instead of: from openai import OpenAI\n            # Use: import ollama"
                elif (
                    "gemini" in matched_text.lower() or "google" in matched_text.lower()
                ):
                    service = "Google Gemini"
                    local_alt = "llama.cpp with gemma models"
                    import_alt = "# Consider using local models instead"
                elif (
                    "anthropic" in matched_text.lower()
                    or "claude" in matched_text.lower()
                ):
                    service = "Anthropic Claude"
                    local_alt = "the current AI assistant's capabilities"
                    import_alt = (
                        "# You're already using Claude - no external API needed"
                    )
                elif "cohere" in matched_text.lower():
                    service = "Cohere"
                    local_alt = "sentence-transformers for embeddings"
                    import_alt = "# For embeddings: from sentence_transformers import SentenceTransformer"
                else:
                    service = "external LLM"
                    local_alt = "local open-source models"
                    import_alt = "# Consider local alternatives"

                message_parts = [
                    f"{service} API reference detected on line {line_num}",
                    f"      Found: {matched_text}",
                    "      Risk: Data leaves your system, costs can accumulate, requires API keys",
                    f"      Local alternative: {local_alt}",
                    f"      {import_alt}",
                    "      To allow external APIs: antimon --disable-detector llm_api",
                ]
                return DetectionResult(
                    detected=True,
                    message="\n".join(message_parts),
                    details={
                        "pattern": pattern,
                        "line": line_num,
                        "match": matched_text,
                    },
                )

    return DetectionResult(detected=False)


def detect_api_key(json_data: HookData) -> DetectionResult:
    """
    Detect hardcoded API keys in content

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if API keys were detected
    """
    # Check if file is ignored
    file_path = json_data.get("tool_input", {}).get("file_path", "")
    config = get_runtime_config()
    if file_path and config.is_file_ignored(file_path):
        return DetectionResult(detected=False)

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
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                line_num = find_line_number(text, match)
                matched_text = match.group(0)
                # Extract key name if possible
                key_name_match = re.search(r'(\w+)\s*[=:]\s*["\']', matched_text)
                key_name = key_name_match.group(1) if key_name_match else "key"

                # Determine the type of credential
                if "api" in matched_text.lower():
                    cred_type = "API key"
                    example_fix = f"{key_name} = os.environ.get('{key_name.upper()}')"
                elif "token" in matched_text.lower():
                    cred_type = "access token"
                    example_fix = f"{key_name} = os.getenv('{key_name.upper()}')"
                elif "secret" in matched_text.lower():
                    cred_type = "secret key"
                    example_fix = f"{key_name} = config.get_secret('{key_name}')"
                else:
                    cred_type = "credential"
                    example_fix = f"{key_name} = os.environ['{key_name.upper()}']"

                message_parts = [
                    f"Hardcoded {cred_type} detected on line {line_num}",
                    f"      Found: {matched_text}",
                    "      Risk: Exposed credentials can be stolen from code repositories",
                    f"      Quick fix: {example_fix}",
                    "      Best practice: Use .env files or secret management services",
                    f"      For examples: Use placeholders like '{key_name} = \"your-{key_name}-here\"'",
                ]
                return DetectionResult(
                    detected=True,
                    message="\n".join(message_parts),
                    details={
                        "pattern": pattern,
                        "line": line_num,
                        "match": matched_text,
                    },
                )

    return DetectionResult(detected=False)


def detect_docker(json_data: HookData) -> DetectionResult:
    """
    Detect Docker-related operations

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if Docker operations were detected
    """
    # Check if file is ignored
    file_path = json_data.get("tool_input", {}).get("file_path", "")
    config = get_runtime_config()
    if file_path and config.is_file_ignored(file_path):
        return DetectionResult(detected=False)

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
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                line_num = find_line_number(text, match)
                matched_text = match.group(0)
                message_parts = [
                    "Docker operation detected",
                    f"      Line {line_num}: {matched_text}",
                    f"      Pattern matched: {pattern}",
                    "      Why: Docker operations can pose security risks if not properly configured",
                    "      Suggestion: Review Docker commands for security best practices",
                ]
                return DetectionResult(
                    detected=True,
                    message="\n".join(message_parts),
                    details={
                        "pattern": pattern,
                        "line": line_num,
                        "match": matched_text,
                    },
                )

    return DetectionResult(detected=False)


def detect_localhost(json_data: HookData) -> DetectionResult:
    """
    Detect localhost and port references

    Args:
        json_data: Hook data containing content to check

    Returns:
        DetectionResult indicating if localhost references were detected
    """
    # Check if file is ignored
    file_path = json_data.get("tool_input", {}).get("file_path", "")
    config = get_runtime_config()
    if file_path and config.is_file_ignored(file_path):
        return DetectionResult(detected=False)

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
            match = re.search(pattern, text)
            if match:
                line_num = find_line_number(text, match)
                matched_text = match.group(0)
                message_parts = [
                    "Localhost/port reference detected",
                    f"      Line {line_num}: {matched_text}",
                    f"      Pattern matched: {pattern}",
                    "      Why: Hardcoded localhost references may not work in production",
                    "      Suggestion: Use configuration files or environment variables for host/port settings",
                ]
                return DetectionResult(
                    detected=True,
                    message="\n".join(message_parts),
                    details={
                        "pattern": pattern,
                        "line": line_num,
                        "match": matched_text,
                    },
                )

    return DetectionResult(detected=False)


def detect_claude_antipatterns(json_data: HookData) -> DetectionResult:
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


def detect_read_sensitive_files(json_data: HookData) -> DetectionResult:
    """
    Detect Read tool attempts to access sensitive files

    Args:
        json_data: Hook data containing file path information

    Returns:
        DetectionResult indicating if sensitive file read was attempted
    """
    # Only check Read tool
    if json_data.get("tool_name") != "Read":
        return DetectionResult(detected=False)

    # Check if file is explicitly allowed or ignored
    file_path = json_data.get("tool_input", {}).get("file_path", "")
    config = get_runtime_config()
    if file_path in config.allowed_files or config.is_file_ignored(file_path):
        return DetectionResult(detected=False)

    # Sensitive file patterns for Read operations
    sensitive_patterns = [
        r"/etc/shadow",
        r"/etc/passwd",
        r"\.ssh/id_[^/]+$",  # SSH private keys
        r"\.ssh/known_hosts",
        r"\.ssh/authorized_keys",
        r"\.pem$",
        r"\.key$",
        r"\.pfx$",
        r"\.p12$",
        r"\.jks$",  # Java keystore
        r"\.gpg$",  # GPG keys
        r"\.asc$",  # ASCII armored keys
        r"\.env$",
        r"\.aws/credentials",
        r"\.aws/config",
        r"\.kube/config",
        r"\.docker/config\.json",
        r"\.npmrc",
        r"\.pypirc",
        r"\.gitconfig",
        r"\.netrc",
        r"credentials\.json",
        r"secrets\.yaml",
        r"secrets\.yml",
        r"service[_-]?account[_-]?key\.json",
        r"private[_-]?key",
        r"deploy[_-]?key",
        r"/proc/",  # Process information
        r"/sys/",  # System information
        r"/dev/",  # Device files
        r"\.history$",  # Shell history files
        r"\.bash_history",
        r"\.zsh_history",
        r"\.mysql_history",
        r"\.psql_history",
        r"\.sqlite_history",
        r"wallet\.dat",  # Cryptocurrency wallets
        r"\.gnupg/",
        r"\.password-store/",
    ]

    file_path = json_data.get("tool_input", {}).get("file_path", "")

    for pattern in sensitive_patterns:
        if re.search(pattern, file_path, re.IGNORECASE):
            message_parts = [
                f"Attempt to read sensitive file: {file_path}",
                f"      Pattern matched: {pattern}",
                "      Why: This file may contain sensitive credentials or system information",
                "      Suggestion: Consider if this access is necessary and handle with appropriate security measures",
            ]
            return DetectionResult(
                detected=True,
                message="\n".join(message_parts),
                details={"pattern": pattern, "file_path": file_path},
            )

    return DetectionResult(detected=False)


def detect_bash_dangerous_commands(json_data: HookData) -> DetectionResult:
    """
    Detect dangerous Bash commands

    Args:
        json_data: Hook data containing command information

    Returns:
        DetectionResult indicating if dangerous commands were detected
    """
    # Only check Bash tool
    if json_data.get("tool_name") != "Bash":
        return DetectionResult(detected=False)

    command = json_data.get("tool_input", {}).get("command", "")

    # Dangerous command patterns
    dangerous_patterns = [
        # Destructive commands
        (r"rm\s+-rf\s+/", "Destructive file removal of root directory"),
        (r"rm\s+-rf\s+\*", "Destructive file removal with wildcard"),
        (r">\s*/dev/sda", "Direct disk write operation"),
        (r"dd\s+.*of=/dev/[^/\s]+", "Direct disk write with dd"),
        (r"mkfs\.", "Filesystem formatting command"),
        # System modification
        (r"chmod\s+777", "Overly permissive file permissions"),
        (r"chmod\s+-R\s+777", "Recursive overly permissive permissions"),
        (r"chown\s+-R\s+root", "Recursive root ownership change"),
        # Privilege escalation
        (r"sudo\s+su", "Privilege escalation to root"),
        (r"sudo\s+-i", "Interactive root shell"),
        (r"sudo\s+bash", "Root shell execution"),
        (r"sudo\s+sh", "Root shell execution"),
        # Remote code execution
        (r"curl\s+[^|]+\|\s*bash", "Remote script execution via curl"),
        (r"wget\s+[^|]+\|\s*bash", "Remote script execution via wget"),
        (r"curl\s+[^|]+\|\s*sh", "Remote script execution via curl"),
        (r"wget\s+[^|]+\|\s*sh", "Remote script execution via wget"),
        (r"eval\s*\(", "Dynamic code execution with eval"),
        (r"exec\s*\(", "Dynamic code execution with exec"),
        # System file modification
        (r">\s*/etc/", "Writing to system configuration directory"),
        (r">>\s*/etc/", "Appending to system configuration directory"),
        (r"echo\s+.*>\s*/etc/", "Writing to system configuration"),
        (r"echo\s+.*>>\s*/etc/", "Appending to system configuration"),
        # Network operations
        (r"nc\s+-l", "Netcat listener (potential backdoor)"),
        (r"ncat\s+-l", "Ncat listener (potential backdoor)"),
        (r"socat\s+.*LISTEN", "Socat listener (potential backdoor)"),
        # Package management (potentially dangerous)
        (r"pip\s+install\s+--force", "Force pip installation"),
        (r"npm\s+install\s+--force", "Force npm installation"),
        (r"apt-get\s+install\s+-y", "Unattended package installation"),
        (r"yum\s+install\s+-y", "Unattended package installation"),
        # Cryptocurrency mining
        (r"xmrig", "Cryptocurrency miner"),
        (r"minergate", "Cryptocurrency miner"),
        (r"nicehash", "Cryptocurrency miner"),
        # Information disclosure
        (r"cat\s+/etc/shadow", "Attempting to read password hashes"),
        (r"cat\s+.*\.ssh/id_", "Attempting to read SSH private keys"),
        (r"find\s+.*-name\s+.*password", "Searching for password files"),
        (r"grep\s+-r\s+.*password", "Searching for passwords in files"),
    ]

    for pattern, description in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            message_parts = [
                f"Dangerous command detected: {description}",
                f"      Command: {command}",
                f"      Pattern matched: {pattern}",
                "      Why: This command could damage the system or expose sensitive data",
                "      Suggestion: Review if this operation is necessary and consider safer alternatives",
            ]
            return DetectionResult(
                detected=True,
                message="\n".join(message_parts),
                details={
                    "pattern": pattern,
                    "command": command,
                    "description": description,
                },
            )

    # Check for attempts to read sensitive files via common commands
    sensitive_file_patterns = [
        (r"cat\s+[^|]*\.env", "Reading environment file"),
        (r"cat\s+[^|]*credentials", "Reading credential file"),
        (r"less\s+[^|]*\.env", "Reading environment file"),
        (r"less\s+[^|]*credentials", "Reading credential file"),
        (r"more\s+[^|]*\.env", "Reading environment file"),
        (r"more\s+[^|]*credentials", "Reading credential file"),
        (r"head\s+[^|]*\.env", "Reading environment file"),
        (r"tail\s+[^|]*\.env", "Reading environment file"),
    ]

    for pattern, description in sensitive_file_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            message_parts = [
                f"Sensitive file access via command: {description}",
                f"      Command: {command}",
                f"      Pattern matched: {pattern}",
                "      Why: This may expose sensitive credentials or configuration",
                "      Suggestion: Use appropriate security measures when handling sensitive files",
            ]
            return DetectionResult(
                detected=True,
                message="\n".join(message_parts),
                details={
                    "pattern": pattern,
                    "command": command,
                    "description": description,
                },
            )

    return DetectionResult(detected=False)
