# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for pattern testing functionality
"""

from unittest.mock import patch

from antimon.pattern_test import (
    check_single_pattern,
    display_pattern_test_results,
    run_pattern_test,
    show_pattern_examples,
)


class TestPatternTest:
    """Test pattern testing functionality"""

    def test_check_single_pattern_api_key(self):
        """Test detecting API key patterns"""
        pattern = 'api_key = "sk-1234567890"'
        results = check_single_pattern(pattern, detector_type="api_key")

        assert "api_key" in results
        assert len(results["api_key"]) > 0
        assert any(detected for _, detected, _ in results["api_key"])

    def test_check_single_pattern_llm_api(self):
        """Test detecting LLM API patterns"""
        pattern = "from openai import OpenAI"
        results = check_single_pattern(pattern, detector_type="llm_api")

        assert "llm_api" in results
        assert len(results["llm_api"]) > 0
        assert any(detected for _, detected, _ in results["llm_api"])

    def test_check_single_pattern_safe(self):
        """Test safe patterns"""
        pattern = 'print("Hello, World!")'
        results = check_single_pattern(pattern)

        # Should test all detectors
        assert len(results) == 5  # All detectors

        # None should detect this safe pattern
        for detector_results in results.values():
            assert len(detector_results) == 0

    def test_check_single_pattern_filename(self):
        """Test filename patterns"""
        pattern = "/etc/passwd"
        results = check_single_pattern(pattern, detector_type="filenames")

        assert "filenames" in results
        assert len(results["filenames"]) > 0
        assert any(detected for _, detected, _ in results["filenames"])

    def test_check_single_pattern_invalid_detector(self, capsys):
        """Test with invalid detector type"""
        pattern = "test pattern"
        results = check_single_pattern(pattern, detector_type="invalid_detector")

        assert results == {}
        captured = capsys.readouterr()
        assert "Unknown detector type: invalid_detector" in captured.err
        assert "Available detectors:" in captured.err

    def test_check_single_pattern_verbose(self, capsys):
        """Test verbose output"""
        pattern = "docker run ubuntu"
        check_single_pattern(pattern, detector_type="docker", verbose=True)

        captured = capsys.readouterr()
        assert "docker detector triggered" in captured.out

    @patch("antimon.pattern_test.detect_api_key")
    def test_check_single_pattern_with_error(self, mock_detector, capsys):
        """Test handling detector errors"""
        mock_detector.side_effect = Exception("Test error")

        pattern = 'api_key = "test"'
        results = check_single_pattern(pattern, detector_type="api_key", verbose=True)

        assert "api_key" in results
        assert len(results["api_key"]) == 0  # No successful detections

        captured = capsys.readouterr()
        assert "Error testing api_key detector" in captured.out

    def test_display_pattern_test_results_blocked(self, capsys):
        """Test displaying results for blocked pattern"""
        results = {
            "api_key": [("Write", True, "API key found in content")],
            "llm_api": [],
            "docker": [],
        }

        display_pattern_test_results("test pattern", results, no_color=True)
        captured = capsys.readouterr()

        assert "Pattern Test Results" in captured.out
        assert "api_key detector:" in captured.out
        assert "API key found in content" in captured.out
        assert "Pattern would be BLOCKED" in captured.out

    def test_display_pattern_test_results_allowed(self, capsys):
        """Test displaying results for allowed pattern"""
        results = {
            "api_key": [],
            "llm_api": [],
            "docker": [],
        }

        display_pattern_test_results("safe pattern", results, no_color=True)
        captured = capsys.readouterr()

        assert "Pattern Test Results" in captured.out
        assert "No issues detected" in captured.out
        assert "Pattern would be ALLOWED" in captured.out

    def test_show_pattern_examples_all(self, capsys):
        """Test showing all pattern examples"""
        show_pattern_examples(no_color=True)
        captured = capsys.readouterr()

        assert "Pattern Examples" in captured.out
        assert "api_key detector patterns:" in captured.out
        assert "llm_api detector patterns:" in captured.out
        assert "docker detector patterns:" in captured.out
        assert "localhost detector patterns:" in captured.out
        assert "filenames detector patterns:" in captured.out

    def test_show_pattern_examples_specific(self, capsys):
        """Test showing specific detector examples"""
        show_pattern_examples(detector_type="api_key", no_color=True)
        captured = capsys.readouterr()

        assert "Pattern Examples" in captured.out
        assert "api_key detector patterns:" in captured.out
        assert "llm_api detector patterns:" not in captured.out

    def test_show_pattern_examples_invalid(self, capsys):
        """Test showing examples for invalid detector"""
        show_pattern_examples(detector_type="invalid", no_color=True)
        captured = capsys.readouterr()

        assert "Unknown detector type: invalid" in captured.err

    def test_run_pattern_test_with_pattern(self, capsys):
        """Test run_pattern_test with a pattern"""
        result = run_pattern_test(pattern='api_key = "sk-123"', no_color=True)

        assert result == 0
        captured = capsys.readouterr()
        assert "Testing pattern against antimon detectors" in captured.out
        assert "Pattern Test Results" in captured.out

    def test_run_pattern_test_examples_only(self, capsys):
        """Test run_pattern_test showing examples only"""
        result = run_pattern_test(show_examples=True, no_color=True)

        assert result == 0
        captured = capsys.readouterr()
        assert "Pattern Examples" in captured.out

    def test_run_pattern_test_no_args(self, capsys):
        """Test run_pattern_test with no arguments"""
        result = run_pattern_test(no_color=True)

        assert result == 0
        captured = capsys.readouterr()
        assert "Pattern Examples" in captured.out

    def test_run_pattern_test_with_detector(self, capsys):
        """Test run_pattern_test with specific detector"""
        result = run_pattern_test(
            pattern="FROM ubuntu:latest", detector_type="docker", no_color=True
        )

        assert result == 0
        captured = capsys.readouterr()
        assert "docker detector:" in captured.out
        assert "api_key detector:" not in captured.out  # Should only test docker

    def test_pattern_test_integration(self):
        """Integration test for full pattern testing flow"""
        # Test various patterns
        test_cases = [
            ('api_key = "sk-test"', True),  # Should be blocked
            ('print("hello")', False),  # Should be allowed
            ("docker run -it ubuntu", True),  # Should be blocked
            ("localhost:8080", True),  # Should be blocked
            ("/etc/passwd", True),  # Should be blocked
        ]

        for pattern, should_block in test_cases:
            results = check_single_pattern(pattern)

            # Check if any detector triggered
            any_detected = any(
                len(detector_results) > 0 for detector_results in results.values()
            )

            assert (
                any_detected == should_block
            ), f"Pattern '{pattern}' detection mismatch"
