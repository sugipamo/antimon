# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Pattern-based detection engine using configuration files
"""

import re
from typing import List, Tuple

from .config import AntimonConfig, PatternConfig, load_config
from .detectors import DetectionResult, HookData


class PatternDetector:
    """Configuration-based pattern detection engine"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize pattern detector with configuration
        
        Args:
            config_path: Path to configuration file, or None for default
        """
        self.config = load_config(config_path)
    
    def detect_patterns(self, json_data: HookData) -> List[DetectionResult]:
        """
        Run all enabled pattern detectors
        
        Args:
            json_data: Hook data from AI assistant
            
        Returns:
            List of detection results
        """
        results = []
        
        for pattern_name, pattern_config in self.config.patterns.items():
            if not pattern_config.enabled:
                continue
            
            result = self._check_pattern(pattern_name, pattern_config, json_data)
            if result and result.detected:
                results.append(result)
        
        return results
    
    def _check_pattern(self, pattern_name: str, pattern_config: PatternConfig, json_data: HookData) -> DetectionResult:
        """
        Check a single pattern against the data
        
        Args:
            pattern_name: Name of the pattern
            pattern_config: Pattern configuration
            json_data: Hook data to check
            
        Returns:
            Detection result
        """
        tool_input = json_data.get("tool_input", {})
        
        # Check file patterns
        if pattern_config.file_patterns:
            file_path = tool_input.get("file_path", "")
            if file_path and self._matches_any_pattern(file_path, pattern_config.file_patterns):
                return DetectionResult(
                    detected=True,
                    message=f"{pattern_config.message}: {file_path}",
                    severity=pattern_config.severity,
                    details={"pattern_name": pattern_name, "matched_path": file_path}
                )
        
        # Check content patterns
        if pattern_config.content_patterns:
            content = self._get_content_to_check(tool_input)
            matches = self._find_pattern_matches(content, pattern_config.content_patterns)
            if matches:
                return DetectionResult(
                    detected=True,
                    message=f"{pattern_config.message}",
                    severity=pattern_config.severity,
                    details={
                        "pattern_name": pattern_name, 
                        "matches": matches[:3]  # Limit to first 3 matches
                    }
                )
        
        # Check import patterns
        if pattern_config.import_patterns:
            content = self._get_content_to_check(tool_input)
            matches = self._find_pattern_matches(content, pattern_config.import_patterns)
            if matches:
                return DetectionResult(
                    detected=True,
                    message=f"{pattern_config.message} (import detected)",
                    severity=pattern_config.severity,
                    details={
                        "pattern_name": pattern_name,
                        "import_matches": matches[:3]
                    }
                )
        
        return DetectionResult(detected=False)
    
    def _get_content_to_check(self, tool_input: dict) -> str:
        """
        Extract content to check from tool input
        
        Args:
            tool_input: Tool input data
            
        Returns:
            Content string to check
        """
        content_parts = []
        
        # Get main content
        if "content" in tool_input:
            content_parts.append(tool_input["content"])
        
        # Get edit strings
        if "old_string" in tool_input:
            content_parts.append(tool_input["old_string"])
        if "new_string" in tool_input:
            content_parts.append(tool_input["new_string"])
        
        # Get multi-edit content
        if "edits" in tool_input:
            for edit in tool_input["edits"]:
                if "old_string" in edit:
                    content_parts.append(edit["old_string"])
                if "new_string" in edit:
                    content_parts.append(edit["new_string"])
        
        # Get command content
        if "command" in tool_input:
            content_parts.append(tool_input["command"])
        
        return "\n".join(content_parts)
    
    def _matches_any_pattern(self, text: str, patterns: List[str]) -> bool:
        """
        Check if text matches any of the given patterns
        
        Args:
            text: Text to check
            patterns: List of regex patterns
            
        Returns:
            True if any pattern matches
        """
        for pattern in patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    return True
            except re.error:
                # Skip invalid regex patterns
                continue
        return False
    
    def _find_pattern_matches(self, text: str, patterns: List[str]) -> List[Tuple[str, str]]:
        """
        Find all pattern matches in text
        
        Args:
            text: Text to check
            patterns: List of regex patterns
            
        Returns:
            List of (pattern, matched_text) tuples
        """
        matches = []
        for pattern in patterns:
            try:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    matches.append((pattern, match.group()))
                    if len(matches) >= 10:  # Limit total matches
                        return matches
            except re.error:
                # Skip invalid regex patterns
                continue
        return matches
    
    def get_enabled_patterns(self) -> List[str]:
        """
        Get list of enabled pattern names
        
        Returns:
            List of enabled pattern names
        """
        return [name for name, config in self.config.patterns.items() if config.enabled]
    
    def get_pattern_info(self, pattern_name: str) -> PatternConfig:
        """
        Get configuration for a specific pattern
        
        Args:
            pattern_name: Name of the pattern
            
        Returns:
            Pattern configuration or None if not found
        """
        return self.config.patterns.get(pattern_name)