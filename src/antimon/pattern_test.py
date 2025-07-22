# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Pattern testing functionality for antimon
"""

import sys

from .color_utils import ColorFormatter
from .detectors import (
    detect_api_key,
    detect_docker,
    detect_filenames,
    detect_llm_api,
    detect_localhost,
)

SAMPLE_PATTERNS = {
    "api_key": [
        'api_key = "sk-1234567890abcdef"',
        'OPENAI_API_KEY = "sk-proj-abcdef123456"',
        "Authorization: Bearer sk-test-123456",
        "export API_KEY=abcd1234efgh5678",
        'client = OpenAI(api_key="sk-live-xxxxx")',
    ],
    "llm_api": [
        "from openai import OpenAI",
        "import google.generativeai as genai",
        "client = anthropic.Anthropic()",
        "response = openai.ChatCompletion.create()",
        'gemini.generate_content("Hello")',
    ],
    "docker": [
        "docker run -it ubuntu bash",
        "FROM python:3.11-slim",
        "docker-compose up -d",
        "sudo docker build .",
        "podman run --rm alpine",
    ],
    "localhost": [
        "http://localhost:8080",
        'connect("127.0.0.1", 3306)',
        "server.listen(0.0.0.0:5000)",
        "redis://localhost:6379",
        "mongodb://127.0.0.1:27017",
    ],
    "filenames": [
        "/etc/passwd",
        "~/.ssh/id_rsa",
        "/var/log/auth.log",
        "C:\\Windows\\System32\\config\\SAM",
        "../../.env",
    ],
}


def check_single_pattern(
    pattern: str,
    detector_type: str | None = None,
    verbose: bool = False,
    no_color: bool = False,
) -> dict[str, list[tuple[str, bool, str]]]:
    """
    Test a pattern against all or specific detectors

    Args:
        pattern: The pattern/content to test
        detector_type: Specific detector to test (None for all)
        verbose: Show verbose output
        no_color: Disable colored output

    Returns:
        Dictionary mapping detector names to results
    """
    formatter = ColorFormatter(use_color=not no_color)
    results = {}

    # Create test data structures for different contexts
    test_cases = [
        # Write tool test
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "test.py", "content": pattern},
        },
        # Edit tool test
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "test.py",
                "old_string": "# placeholder",
                "new_string": pattern,
            },
        },
        # Filename test (for path patterns)
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": pattern, "content": "test content"},
        },
        # Read tool test (for filename detector)
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": pattern},
        },
    ]

    detectors = {
        "api_key": detect_api_key,
        "llm_api": detect_llm_api,
        "docker": detect_docker,
        "localhost": detect_localhost,
        "filenames": detect_filenames,
    }

    # Filter detectors if specific type requested
    if detector_type:
        if detector_type not in detectors:
            print(
                f"{formatter.error('Error:')} Unknown detector type: {detector_type}",
                file=sys.stderr,
            )
            print(
                f"Available detectors: {', '.join(detectors.keys())}", file=sys.stderr
            )
            return {}
        detectors = {detector_type: detectors[detector_type]}

    # Test against each detector
    for name, detector in detectors.items():
        detector_results = []

        for test_case in test_cases:
            try:
                result = detector(test_case)
                if result.detected:
                    detector_results.append(
                        (test_case["tool_name"], True, result.message)
                    )
                    if verbose:
                        print(
                            f"  {formatter.warning('•')} {name} detector triggered on {test_case['tool_name']} tool"
                        )
                        print(f"    Message: {result.message}")
                        if hasattr(result, "suggestion") and result.suggestion:
                            print(f"    Suggestion: {result.suggestion}")
            except Exception as e:
                if verbose:
                    print(
                        f"  {formatter.error('✗')} Error testing {name} detector: {e}"
                    )

        results[name] = detector_results

    return results


def display_pattern_test_results(
    pattern: str,
    results: dict[str, list[tuple[str, bool, str]]],
    no_color: bool = False,
):
    """Display pattern test results in a formatted way"""
    formatter = ColorFormatter(use_color=not no_color)

    print(f"\n{formatter.bold('Pattern Test Results')}")
    print(f"{formatter.info('Pattern:')} {pattern}")
    print(f"{'-' * 60}")

    any_detected = False
    for detector_name, detector_results in results.items():
        if detector_results:
            any_detected = True
            print(f"\n{formatter.warning(f'⚠️  {detector_name} detector:')}")
            for tool, _detected, message in detector_results:
                print(f"   • Triggered on {formatter.bold(tool)} tool")
                print(f"     {message}")
        else:
            print(
                f"\n{formatter.success(f'✓ {detector_name} detector:')} No issues detected"
            )

    print(f"\n{'-' * 60}")
    if any_detected:
        print(f"{formatter.error('Result:')} Pattern would be BLOCKED")
    else:
        print(f"{formatter.success('Result:')} Pattern would be ALLOWED")
    print("")


def show_pattern_examples(detector_type: str | None = None, no_color: bool = False):
    """Show example patterns for detectors"""
    formatter = ColorFormatter(use_color=not no_color)

    print(f"\n{formatter.bold('📋 Pattern Examples')}")

    if detector_type:
        if detector_type not in SAMPLE_PATTERNS:
            print(
                f"{formatter.error('Error:')} Unknown detector type: {detector_type}",
                file=sys.stderr,
            )
            return
        patterns_to_show = {detector_type: SAMPLE_PATTERNS[detector_type]}
    else:
        patterns_to_show = SAMPLE_PATTERNS

    for detector, patterns in patterns_to_show.items():
        print(f"\n{formatter.highlight(f'{detector} detector patterns:')}")
        for pattern in patterns:
            print(f"  • {pattern}")

    print(
        f"\n{formatter.info('Tip:')} Use --test-pattern with any of these patterns to see detection in action"
    )
    print(
        f"{formatter.info('Example:')} antimon --test-pattern 'api_key = \"sk-123\"'\n"
    )


def run_pattern_test(
    pattern: str | None = None,
    detector_type: str | None = None,
    show_examples: bool = False,
    verbose: bool = False,
    no_color: bool = False,
) -> int:
    """
    Main entry point for pattern testing

    Args:
        pattern: Pattern to test (if None, shows examples)
        detector_type: Specific detector to test
        show_examples: Show example patterns
        verbose: Enable verbose output
        no_color: Disable colored output

    Returns:
        Exit code (0 for success)
    """
    formatter = ColorFormatter(use_color=not no_color)

    if show_examples or pattern is None:
        show_pattern_examples(detector_type, no_color)
        if pattern is None:
            return 0

    if pattern:
        print(f"\n{formatter.bold('🔍 Testing pattern against antimon detectors...')}")
        results = check_single_pattern(pattern, detector_type, verbose, no_color)
        display_pattern_test_results(pattern, results, no_color)

    return 0
