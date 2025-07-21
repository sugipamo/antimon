"""
Tests for core validation logic
"""

from antimon.core import validate_hook_data


class TestValidateHookData:
    """Test cases for the core validation hook functionality.
    
    Tests the main validate_hook_data function which:
    - Orchestrates all detectors
    - Handles different tool types (Write, Edit, MultiEdit, etc.)
    - Returns aggregated results and statistics
    - Properly ignores non-code-editing tools
    """
    def test_non_code_editing_tool(self):
        json_data = {"tool_name": "LS", "tool_input": {"path": "/home/user"}}
        has_issues, issues, stats = validate_hook_data(json_data)
        assert has_issues is False
        assert len(issues) == 0
        assert stats == {}
    
    def test_read_tool_with_sensitive_file(self):
        json_data = {"tool_name": "Read", "tool_input": {"file_path": "/etc/passwd"}}
        has_issues, issues, stats = validate_hook_data(json_data)
        assert has_issues is True
        assert len(issues) == 1
        assert "sensitive file" in issues[0]

    def test_write_tool_with_dangerous_path(self):
        json_data = {
            "tool_name": "Write",
            "tool_input": {"file_path": "/etc/passwd", "content": "hacked"},
        }
        has_issues, issues, stats = validate_hook_data(json_data)
        assert has_issues is True
        assert len(issues) > 0
        assert any("Dangerous file path" in issue for issue in issues)
        assert stats["total"] == 6
        assert stats["failed"] >= 1

    def test_edit_tool_with_api_key(self):
        json_data = {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "config.py",
                "content": 'api_key = "sk-secret123"',
            },
        }
        has_issues, issues, stats = validate_hook_data(json_data)
        assert has_issues is True
        assert any("API key" in issue for issue in issues)
        assert stats["total"] == 6
        assert stats["failed"] >= 1

    def test_multiedit_tool_with_llm_api(self):
        json_data = {
            "tool_name": "MultiEdit",
            "tool_input": {
                "file_path": "main.py",
                "content": "import openai\nclient = openai.Client()",
            },
        }
        has_issues, issues, stats = validate_hook_data(json_data)
        assert has_issues is True
        assert any("LLM API" in issue for issue in issues)
        assert stats["total"] == 6
        assert stats["failed"] >= 1

    def test_safe_write(self):
        json_data = {
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/home/user/project/main.py",
                "content": 'def hello():\n    print("Hello, World!")',
            },
        }
        has_issues, issues, stats = validate_hook_data(json_data)
        assert has_issues is False
        assert len(issues) == 0
        assert stats["total"] == 6
        assert stats["passed"] == 6
        assert stats["failed"] == 0
