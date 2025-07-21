# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Self-test functionality for antimon
"""

import json
import logging
import sys
from typing import Tuple

from .core import validate_hook_data


def run_self_test(verbose: bool = False) -> int:
    """
    Run a self-test to verify antimon is working correctly
    
    Args:
        verbose: Enable verbose output
        
    Returns:
        0 if all tests pass, 1 if any test fails
    """
    # Suppress logging during tests unless verbose mode is enabled
    if not verbose:
        logging.getLogger("antimon").setLevel(logging.ERROR)
    
    print("🔍 Running antimon self-test...\n")
    
    test_cases = [
        # Test 1: Should detect sensitive file access
        {
            "name": "Sensitive file detection",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "/etc/passwd",
                    "content": "malicious content"
                }
            },
            "should_detect": True,
            "expected_pattern": "Dangerous file path"
        },
        
        # Test 2: Should detect API key
        {
            "name": "API key detection",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "config.py",
                    "content": 'api_key = "sk-1234567890abcdef"'
                }
            },
            "should_detect": True,
            "expected_pattern": "API key"
        },
        
        # Test 3: Should detect LLM API usage
        {
            "name": "LLM API detection",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "chat.py",
                    "content": "from openai import OpenAI\nclient = OpenAI()"
                }
            },
            "should_detect": True,
            "expected_pattern": "LLM API"
        },
        
        # Test 4: Should detect Docker operations
        {
            "name": "Docker operation detection",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "deploy.sh",
                    "content": "docker run -d nginx"
                }
            },
            "should_detect": True,
            "expected_pattern": "Docker"
        },
        
        # Test 5: Should detect localhost connections
        {
            "name": "Localhost connection detection",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "app.py",
                    "content": 'url = "http://localhost:8080/api"'
                }
            },
            "should_detect": True,
            "expected_pattern": "localhost"
        },
        
        # Test 6: Safe operation should pass
        {
            "name": "Safe operation (should pass)",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "hello.py",
                    "content": 'print("Hello, World!")'
                }
            },
            "should_detect": False,
            "expected_pattern": None
        },
        
        # Test 7: Edit tool with API key
        {
            "name": "Edit tool API key detection",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "settings.py",
                    "old_string": "# Configuration",
                    "new_string": "OPENAI_API_KEY = 'sk-proj-123456'"
                }
            },
            "should_detect": True,
            "expected_pattern": "API key"
        },
        
        # Test 8: Non-code-editing tools should pass
        {
            "name": "Non-code-editing tool (should pass)",
            "data": {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {
                    "file_path": "README.md"
                }
            },
            "should_detect": False,
            "expected_pattern": None
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        
        if verbose:
            print(f"  Input: {json.dumps(test_case['data'], indent=2)}")
        
        has_issues, messages, stats = validate_hook_data(test_case['data'])
        
        if test_case['should_detect']:
            if has_issues:
                # Check if expected pattern is in any message
                pattern_found = any(
                    test_case['expected_pattern'].lower() in msg.lower()
                    for msg in messages
                )
                
                if pattern_found:
                    print(f"  ✅ PASS: Correctly detected {test_case['expected_pattern']}")
                    if verbose:
                        print(f"  Messages: {messages}")
                    passed += 1
                else:
                    print(f"  ❌ FAIL: Detected issues but not the expected pattern '{test_case['expected_pattern']}'")
                    print(f"  Messages: {messages}")
                    failed += 1
            else:
                print(f"  ❌ FAIL: Should have detected {test_case['expected_pattern']} but didn't")
                failed += 1
        else:
            if not has_issues:
                print(f"  ✅ PASS: Correctly allowed safe operation")
                passed += 1
            else:
                print(f"  ❌ FAIL: False positive - detected issues in safe operation")
                print(f"  Messages: {messages}")
                failed += 1
        
        print()
    
    # Summary
    total = passed + failed
    print("="*50)
    print(f"📊 Test Summary: {passed}/{total} tests passed")
    
    if failed == 0:
        print("✅ All tests passed! antimon is working correctly.")
        return 0
    else:
        print(f"❌ {failed} test(s) failed. Please check the installation.")
        return 1