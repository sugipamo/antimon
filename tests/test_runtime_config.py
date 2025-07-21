# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for runtime configuration
"""

import os
from unittest.mock import patch, Mock

import pytest

from antimon.runtime_config import RuntimeConfig, set_runtime_config, get_runtime_config


def test_runtime_config_from_args():
    """Test creating RuntimeConfig from command line arguments."""
    # Create mock args
    args = Mock()
    args.ignore_pattern = ["*.test.py", "examples/*"]
    args.allow_file = ["/home/user/.config/app.conf", "/etc/myapp.conf"]
    args.disable_detector = ["api_key", "localhost"]
    
    config = RuntimeConfig.from_args(args)
    
    assert config.ignore_patterns == ["*.test.py", "examples/*"]
    assert config.allowed_files == {"/home/user/.config/app.conf", "/etc/myapp.conf"}
    assert config.disabled_detectors == {"api_key", "localhost"}


def test_runtime_config_from_env():
    """Test loading RuntimeConfig from environment variables."""
    args = Mock()
    args.ignore_pattern = None
    args.allow_file = None
    args.disable_detector = None
    
    with patch.dict(os.environ, {
        "ANTIMON_IGNORE_PATTERNS": "*.log,tmp/*",
        "ANTIMON_ALLOW_FILES": "/etc/hosts,/etc/resolv.conf",
        "ANTIMON_DISABLE_DETECTORS": "docker,claude_antipatterns"
    }):
        config = RuntimeConfig.from_args(args)
    
    assert "*.log" in config.ignore_patterns
    assert "tmp/*" in config.ignore_patterns
    assert "/etc/hosts" in config.allowed_files
    assert "/etc/resolv.conf" in config.allowed_files
    assert "docker" in config.disabled_detectors
    assert "claude_antipatterns" in config.disabled_detectors


def test_is_file_ignored():
    """Test file ignore logic."""
    config = RuntimeConfig()
    config.ignore_patterns = ["*.test.py", "examples/*", "*.tmp"]
    config.allowed_files = {"/home/user/test.test.py", "test.test.py"}  # Add both forms
    
    # Test ignored patterns (allowed_files no longer affects is_file_ignored)
    assert config.is_file_ignored("test.test.py") is True  # Matches *.test.py pattern
    assert config.is_file_ignored("other.test.py") is True
    assert config.is_file_ignored("examples/demo.py") is True
    assert config.is_file_ignored("file.tmp") is True
    assert config.is_file_ignored("main.py") is False


def test_is_detector_enabled():
    """Test detector enable/disable logic."""
    config = RuntimeConfig()
    config.disabled_detectors = {"api_key", "localhost"}
    
    # Test with full detector names
    assert config.is_detector_enabled("detect_api_key") is False
    assert config.is_detector_enabled("detect_localhost") is False
    assert config.is_detector_enabled("detect_docker") is True
    
    # Test with short names
    assert config.is_detector_enabled("api_key") is False
    assert config.is_detector_enabled("localhost") is False
    assert config.is_detector_enabled("docker") is True


def test_get_summary():
    """Test configuration summary generation."""
    config = RuntimeConfig()
    config.ignore_patterns = ["*.test.py", "*.tmp"]
    config.allowed_files = {"/etc/myapp.conf"}
    config.disabled_detectors = {"api_key"}
    
    summary = config.get_summary()
    
    assert any("Ignored patterns: *.test.py, *.tmp" in line for line in summary)
    assert any("Allowed files: /etc/myapp.conf" in line for line in summary)
    assert any("Disabled detectors: api_key" in line for line in summary)


def test_global_runtime_config():
    """Test global runtime config getter/setter."""
    # Reset global config
    set_runtime_config(None)
    
    # Get should create default config
    config1 = get_runtime_config()
    assert isinstance(config1, RuntimeConfig)
    assert len(config1.ignore_patterns) == 0
    
    # Set new config
    new_config = RuntimeConfig()
    new_config.ignore_patterns = ["test.py"]
    set_runtime_config(new_config)
    
    # Get should return the set config
    config2 = get_runtime_config()
    assert config2 is new_config
    assert config2.ignore_patterns == ["test.py"]