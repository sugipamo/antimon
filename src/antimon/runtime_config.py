# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Runtime configuration management for antimon
"""

import fnmatch
import os
import re
from dataclasses import dataclass, field


@dataclass
class RuntimeConfig:
    """Runtime configuration for antimon."""

    # Patterns to ignore
    ignore_patterns: list[str] = field(default_factory=list)

    # Specific files to allow
    allowed_files: set[str] = field(default_factory=set)

    # Disabled detectors
    disabled_detectors: set[str] = field(default_factory=set)

    # Dry run mode
    dry_run: bool = False

    # Show stats
    show_stats: bool = False

    # Brief mode - concise output
    brief: bool = False


    @classmethod
    def from_args(cls, args) -> "RuntimeConfig":
        """Create RuntimeConfig from command line arguments."""
        config = cls()

        # Add ignore patterns
        if args.ignore_pattern:
            config.ignore_patterns.extend(args.ignore_pattern)

        # Add allowed files
        if args.allow_file:
            config.allowed_files.update(args.allow_file)

        # Add disabled detectors
        if args.disable_detector:
            config.disabled_detectors.update(args.disable_detector)

        # Set dry run mode
        if hasattr(args, "dry_run"):
            config.dry_run = args.dry_run

        # Set stats mode
        if hasattr(args, "stats"):
            config.show_stats = args.stats

        # Set brief mode
        if hasattr(args, "brief"):
            config.brief = args.brief


        # Also check environment variables
        config._load_from_env()

        return config

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # ANTIMON_IGNORE_PATTERNS: comma-separated list of patterns
        if ignore_patterns := os.environ.get("ANTIMON_IGNORE_PATTERNS"):
            self.ignore_patterns.extend(ignore_patterns.split(","))

        # ANTIMON_ALLOW_FILES: comma-separated list of files
        if allow_files := os.environ.get("ANTIMON_ALLOW_FILES"):
            self.allowed_files.update(allow_files.split(","))

        # ANTIMON_DISABLE_DETECTORS: comma-separated list of detectors
        if disable_detectors := os.environ.get("ANTIMON_DISABLE_DETECTORS"):
            self.disabled_detectors.update(disable_detectors.split(","))

    def is_file_ignored(self, file_path: str) -> bool:
        """Check if a file should be ignored based on patterns."""
        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True

        return False

    def is_file_allowed(self, file_path: str) -> bool:
        """Check if a file is explicitly allowed.

        Supports:
        - Exact file paths
        - Glob patterns (*.env, config/*.json)
        - Recursive patterns (**/*.secret)
        """
        # Check exact match first
        if file_path in self.allowed_files:
            return True

        # Check glob patterns
        for pattern in self.allowed_files:
            # If pattern contains glob characters, use fnmatch
            if any(char in pattern for char in ["*", "?", "[", "]"]):
                # Handle ** for recursive matching
                if "**" in pattern:
                    # Convert ** to match any directory depth
                    # e.g., **/*.txt matches any .txt file in any subdirectory
                    # First, escape special regex characters except * and ?
                    regex_pattern = re.escape(pattern)
                    # Then convert glob patterns to regex
                    regex_pattern = regex_pattern.replace(
                        r"\*\*/", "(.*/)?"
                    )  # **/ matches any depth including none
                    regex_pattern = regex_pattern.replace(
                        r"\*\*", ".*"
                    )  # ** matches anything
                    regex_pattern = regex_pattern.replace(
                        r"\*", "[^/]*"
                    )  # * matches anything except /
                    regex_pattern = regex_pattern.replace(
                        r"\?", "[^/]"
                    )  # ? matches single char except /
                    regex_pattern = "^" + regex_pattern + "$"
                    if re.match(regex_pattern, file_path):
                        return True
                else:
                    # Use fnmatch for simple glob patterns
                    if fnmatch.fnmatch(file_path, pattern):
                        return True

        return False

    def is_detector_enabled(self, detector_name: str) -> bool:
        """Check if a detector is enabled."""
        # Normalize detector name (remove "detect_" prefix if present)
        if detector_name.startswith("detect_"):
            detector_name = detector_name[7:]  # Remove "detect_" prefix

        return detector_name not in self.disabled_detectors

    def get_summary(self) -> list[str]:
        """Get a summary of the current configuration."""
        summary = []

        if self.ignore_patterns:
            summary.append(f"Ignored patterns: {', '.join(self.ignore_patterns)}")

        if self.allowed_files:
            summary.append(f"Allowed files: {', '.join(self.allowed_files)}")

        if self.disabled_detectors:
            summary.append(f"Disabled detectors: {', '.join(self.disabled_detectors)}")

        if self.dry_run:
            summary.append("Mode: DRY RUN (preview only, no blocking)")

        if self.show_stats:
            summary.append("Stats: Enabled")

        if self.brief:
            summary.append("Output: Brief mode")

        return summary


# Global runtime config instance
_runtime_config: RuntimeConfig | None = None


def set_runtime_config(config: RuntimeConfig) -> None:
    """Set the global runtime configuration."""
    global _runtime_config
    _runtime_config = config


def get_runtime_config() -> RuntimeConfig:
    """Get the global runtime configuration."""
    global _runtime_config
    if _runtime_config is None:
        _runtime_config = RuntimeConfig()
        _runtime_config._load_from_env()
    return _runtime_config
