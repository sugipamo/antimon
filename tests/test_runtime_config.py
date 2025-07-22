# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for runtime configuration
"""

import os
from unittest.mock import Mock, patch

from antimon.runtime_config import RuntimeConfig, get_runtime_config, set_runtime_config


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


def test_is_file_allowed_glob_patterns():
    """Test file allow logic with glob patterns."""
    config = RuntimeConfig()
    config.allowed_files = {
        "/etc/myapp.conf",  # Exact match
        "*.env",  # Simple glob
        "config/*.json",  # Directory glob
        "**/*.secret",  # Recursive glob
        "test_*.py",  # Prefix glob
        "*.test.py",  # Suffix glob
    }

    # Test exact matches
    assert config.is_file_allowed("/etc/myapp.conf") is True

    # Test simple glob patterns
    assert config.is_file_allowed(".env") is True
    assert config.is_file_allowed("production.env") is True
    assert config.is_file_allowed("local.env") is True
    assert config.is_file_allowed("env") is False

    # Test directory glob patterns
    assert config.is_file_allowed("config/app.json") is True
    assert config.is_file_allowed("config/database.json") is True
    assert config.is_file_allowed("app.json") is False
    assert config.is_file_allowed("other/app.json") is False

    # Test recursive glob patterns
    assert config.is_file_allowed("api.secret") is True
    assert config.is_file_allowed("config/api.secret") is True
    assert config.is_file_allowed("deep/nested/dir/api.secret") is True
    assert config.is_file_allowed("secret") is False

    # Test prefix/suffix patterns
    assert config.is_file_allowed("test_app.py") is True
    assert config.is_file_allowed("app_test.py") is False
    assert config.is_file_allowed("app.test.py") is True
    assert config.is_file_allowed("test.py") is False


def test_is_file_allowed_special_chars():
    """Test file allow logic with special characters in patterns."""
    config = RuntimeConfig()
    config.allowed_files = {
        "file?.txt",  # ? matches single character
        "[abc]file.txt",  # Character class
        "file[0-9].txt",  # Character range
    }

    # Test ? pattern (matches any single character)
    assert config.is_file_allowed("file1.txt") is True
    assert config.is_file_allowed("fileA.txt") is True
    assert config.is_file_allowed("file.txt") is False
    assert config.is_file_allowed("file12.txt") is False

    # Test character class
    assert config.is_file_allowed("afile.txt") is True
    assert config.is_file_allowed("bfile.txt") is True
    assert config.is_file_allowed("cfile.txt") is True
    assert config.is_file_allowed("dfile.txt") is False

    # Test character range (only matches digits 0-9)
    assert config.is_file_allowed("file0.txt") is True
    assert config.is_file_allowed("file5.txt") is True
    assert config.is_file_allowed("file9.txt") is True
    # fileA.txt matches file?.txt pattern, not file[0-9].txt
    assert config.is_file_allowed("fileX.txt") is True  # matches file?.txt
