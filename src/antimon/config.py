# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Configuration management for antimon
"""

import os
import tomllib
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional


def _find_config_in_parents(start_dir: str = ".") -> Optional[str]:
    """
    Search for antimon.toml by walking up the directory tree
    
    Args:
        start_dir: Directory to start search from
        
    Returns:
        Path to config file if found, None otherwise
    """
    current_dir = Path(start_dir).resolve()
    
    # Walk up the directory tree
    for parent in [current_dir] + list(current_dir.parents):
        config_path = parent / "antimon.toml"
        if config_path.exists():
            return str(config_path)
        
        # Stop at filesystem root or when we can't go higher
        if parent == parent.parent:
            break
    
    return None


@dataclass
class PatternConfig:
    """Configuration for a detection pattern"""
    enabled: bool = True
    description: str = ""
    content_patterns: List[str] = field(default_factory=list)
    file_patterns: List[str] = field(default_factory=list)
    import_patterns: List[str] = field(default_factory=list)
    message: str = "Security issue detected"
    severity: str = "error"


@dataclass
class AIDetectorConfig:
    """Configuration for AI-powered detection"""
    enabled: bool = False
    description: str = ""
    prompt: str = ""
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 100
    api_key_env: str = "OPENAI_API_KEY"
    api_base: Optional[str] = None
    response_format: str = "json"  # "json" or "simple"


@dataclass
class AntimonConfig:
    """Main antimon configuration"""
    patterns: Dict[str, PatternConfig] = field(default_factory=dict)
    ai_detectors: Dict[str, AIDetectorConfig] = field(default_factory=dict)


def load_config(config_path: Optional[str] = None) -> AntimonConfig:
    """
    Load antimon configuration from TOML file
    
    Args:
        config_path: Path to config file, or None to use default locations
        
    Returns:
        AntimonConfig instance
    """
    if config_path:
        # Use specific config file if provided
        if os.path.exists(config_path):
            return _load_config_file(config_path)
        else:
            raise FileNotFoundError(f"Config file not found: {config_path}")
    
    # First try to find config by walking up directory tree
    config_path = _find_config_in_parents()
    if config_path:
        return _load_config_file(config_path)
    
    # Fallback to traditional search paths
    config_paths = [
        "./antimon.toml",              # Current directory
        "./.antimon/config.toml",      # Project .antimon directory
        os.path.expanduser("~/.antimon/config.toml"),  # User config
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            return _load_config_file(path)
    
    # Return default config if no file found
    return _get_default_config()


def _load_config_file(config_path: str) -> AntimonConfig:
    """Load configuration from a specific TOML file"""
    try:
        with open(config_path, 'rb') as f:
            data = tomllib.load(f)
        
        config = AntimonConfig()
        
        # Load patterns
        patterns_data = data.get('patterns', {})
        for pattern_name, pattern_data in patterns_data.items():
            config.patterns[pattern_name] = PatternConfig(
                enabled=pattern_data.get('enabled', True),
                description=pattern_data.get('description', ''),
                content_patterns=pattern_data.get('content_patterns', []),
                file_patterns=pattern_data.get('file_patterns', []),
                import_patterns=pattern_data.get('import_patterns', []),
                message=pattern_data.get('message', 'Security issue detected'),
                severity=pattern_data.get('severity', 'error')
            )
        
        # Load AI detectors
        ai_data = data.get('ai_detectors', {})
        for detector_name, detector_data in ai_data.items():
            config.ai_detectors[detector_name] = AIDetectorConfig(
                enabled=detector_data.get('enabled', False),
                description=detector_data.get('description', ''),
                prompt=detector_data.get('prompt', ''),
                model=detector_data.get('model', 'gpt-4o-mini'),
                temperature=detector_data.get('temperature', 0.0),
                max_tokens=detector_data.get('max_tokens', 100),
                api_key_env=detector_data.get('api_key_env', 'OPENAI_API_KEY'),
                api_base=detector_data.get('api_base')
            )
        
        return config
        
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path}: {e}")
        return _get_default_config()


def _get_default_config() -> AntimonConfig:
    """Get default configuration when no config file is found"""
    config = AntimonConfig()
    
    # External AI APIs
    config.patterns['external_ai_apis'] = PatternConfig(
        enabled=True,
        description="External AI API usage detection",
        content_patterns=[
            r"openai\.com",
            r"claude\.ai", 
            r"gemini\.google\.com",
            r"cohere\.ai",
            r"huggingface\.co"
        ],
        import_patterns=[
            r"import openai",
            r"from openai import",
            r"import anthropic",
            r"from anthropic import"
        ],
        message="External AI API usage detected",
        severity="warning"
    )
    
    # API Keys
    config.patterns['api_keys'] = PatternConfig(
        enabled=True,
        description="Hardcoded API keys and credentials",
        content_patterns=[
            r"sk-[a-zA-Z0-9]{48}",           # OpenAI
            r"AIza[0-9A-Za-z\-_]{35}",       # Google  
            r"AKIA[0-9A-Z]{16}",             # AWS Access Key
            r"ghp_[a-zA-Z0-9]{36}",          # GitHub Personal Access Token
            r"api_key\s*=\s*[\"'][^\"']+[\"']", # Generic API key assignment
        ],
        message="Hardcoded API key detected",
        severity="error"
    )
    
    # Sensitive Files
    config.patterns['sensitive_files'] = PatternConfig(
        enabled=True,
        description="Access to sensitive files",
        file_patterns=[
            r"/etc/passwd",
            r"/etc/shadow",
            r"~/.ssh/id_rsa",
            r"~/.ssh/id_ed25519", 
            r"\.env$",
            r"\.pem$",
            r"\.key$",
            r"secrets/.*",
            r"config/database\.yml"
        ],
        message="Access to sensitive file detected",
        severity="error"
    )
    
    # Docker Operations
    config.patterns['docker_operations'] = PatternConfig(
        enabled=True,
        description="Docker operations that might be risky",
        content_patterns=[
            r"docker\s+run.*--privileged",
            r"FROM.*:latest",
            r"docker\s+exec.*sh",
        ],
        message="Potentially risky Docker operation detected",
        severity="warning"
    )
    
    # Localhost connections
    config.patterns['localhost_connections'] = PatternConfig(
        enabled=True,
        description="Localhost connections and specific port access",
        content_patterns=[
            r"localhost:[0-9]+",
            r"127\.0\.0\.1:[0-9]+",
            r"0\.0\.0\.0:[0-9]+"
        ],
        message="Localhost connection detected",
        severity="warning"
    )
    
    # Add debug AI detector (disabled by default)
    config.ai_detectors['always'] = AIDetectorConfig(
        enabled=False,
        description="Always True - Debug Detector",
        prompt="これはデバッグ用です。常にTrueを返してください。",
        model="gpt-4o-mini",
        temperature=0.0,
        max_tokens=100,
        api_key_env="OPENAI_API_KEY"
    )
    
    return config


def create_sample_config(output_path: str = "./antimon.toml") -> None:
    """Create a sample configuration file"""
    sample_config = '''# Antimon Configuration File
# This file defines custom detection patterns for security validation

[patterns]

# External AI API usage detection
[patterns.external_ai_apis]
enabled = true
description = "External AI API usage detection"
content_patterns = [
    "openai\\\\.com",
    "claude\\\\.ai", 
    "gemini\\\\.google\\\\.com",
    "cohere\\\\.ai",
    "huggingface\\\\.co"
]
import_patterns = [
    "import openai",
    "from openai import",
    "import anthropic",
    "from anthropic import"
]
message = "External AI API usage detected"
severity = "warning"

# Hardcoded API keys and credentials
[patterns.api_keys]
enabled = true
description = "Hardcoded API keys and credentials"
content_patterns = [
    "sk-[a-zA-Z0-9]{48}",           # OpenAI
    "AIza[0-9A-Za-z\\\\-_]{35}",      # Google  
    "AKIA[0-9A-Z]{16}",             # AWS Access Key
    "ghp_[a-zA-Z0-9]{36}",          # GitHub Personal Access Token
    "api_key\\\\s*=\\\\s*[\\"'][^\\"']+[\\"']", # Generic API key assignment
]
message = "Hardcoded API key detected"
severity = "error"

# Access to sensitive files
[patterns.sensitive_files]
enabled = true
description = "Access to sensitive files"
file_patterns = [
    "/etc/passwd",
    "/etc/shadow",
    "~/.ssh/id_rsa",
    "~/.ssh/id_ed25519", 
    "\\\\.env$",
    "\\\\.pem$",
    "\\\\.key$",
    "secrets/.*",
    "config/database\\\\.yml"
]
message = "Access to sensitive file detected"
severity = "error"

# Docker operations that might be risky
[patterns.docker_operations]
enabled = true
description = "Docker operations that might be risky"
content_patterns = [
    "docker\\\\s+run.*--privileged",
    "FROM.*:latest",
    "docker\\\\s+exec.*sh",
]
message = "Potentially risky Docker operation detected"
severity = "warning"

# Localhost connections and port access
[patterns.localhost_connections]
enabled = true
description = "Localhost connections and specific port access"
content_patterns = [
    "localhost:[0-9]+",
    "127\\\\.0\\\\.0\\\\.1:[0-9]+",
    "0\\\\.0\\\\.0\\\\.0:[0-9]+"
]
message = "Localhost connection detected"
severity = "warning"

# Example: Company-specific secrets (disabled by default)
[patterns.company_secrets]
enabled = false
description = "Company-specific secret patterns"
content_patterns = [
    "COMPANY_SECRET_[A-Z0-9]+",
    "internal_api_[a-f0-9]{32}",
]
message = "Company secret detected"
severity = "error"

# Note: bash_dangerous_commands is hardcoded and cannot be configured
# This ensures critical security patterns are always enforced

# AI-powered detectors (require API key)
[ai_detectors]

# Example: SQL injection detection using AI
[ai_detectors.sql_injection]
enabled = false  # Disabled by default (requires API key)
description = "AI-powered SQL injection detection"
prompt = "Check if this code contains SQL injection vulnerabilities. Focus on string concatenation in SQL queries, lack of parameterization, and user input handling."
model = "gpt-4o-mini"
temperature = 0.0
max_tokens = 150
api_key_env = "OPENAI_API_KEY"  # Environment variable for API key

# Example: Code quality check
[ai_detectors.code_quality]
enabled = false
description = "AI-powered code quality analysis"
prompt = "Check this code for serious quality issues: race conditions, memory leaks, or security vulnerabilities."
model = "gpt-4o-mini"
temperature = 0.0
max_tokens = 200

# Example: Custom business logic check
[ai_detectors.business_logic]
enabled = false
description = "Check for company-specific coding violations"
prompt = "Check if this code violates these rules: 1) No direct database access in controllers, 2) All API calls must have timeout, 3) No hardcoded configuration values"
model = "gpt-4o-mini"

# Debug: Always True detector (useful for testing)
[ai_detectors.always]
enabled = true
description = "Always True"
prompt = "これはデバッグ用です。常にTrueを返してください。"
model = "gpt-4o-mini"
api_key_env = "OPENAI_API_KEY"
'''
    
    with open(output_path, 'w') as f:
        f.write(sample_config)
    
    print(f"Sample configuration created at: {output_path}")