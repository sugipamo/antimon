# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for auto-fix suggestions
"""


from antimon.autofix import (
    AutoFixSuggestion,
    display_autofix_suggestions,
    generate_fixed_content,
    suggest_api_key_fix,
    suggest_docker_fix,
    suggest_fixes_for_content,
    suggest_llm_api_fix,
    suggest_localhost_fix,
)


class TestAutoFixSuggestion:
    """Test AutoFixSuggestion class"""

    def test_autofix_suggestion_init(self):
        """Test AutoFixSuggestion initialization"""
        suggestion = AutoFixSuggestion(
            issue_type="api_key",
            original='api_key = "sk-123"',
            fixed='api_key = os.environ.get("API_KEY")',
            explanation="Use environment variable",
        )

        assert suggestion.issue_type == "api_key"
        assert suggestion.original == 'api_key = "sk-123"'
        assert suggestion.fixed == 'api_key = os.environ.get("API_KEY")'
        assert suggestion.explanation == "Use environment variable"


class TestApiKeyFixes:
    """Test API key fix suggestions"""

    def test_suggest_api_key_fix_direct_assignment(self):
        """Test fixing direct API key assignments"""
        content = 'api_key = "sk-1234567890abcdef"'
        suggestions = suggest_api_key_fix(content)

        assert len(suggestions) >= 1
        assert suggestions[0].original == 'api_key = "sk-1234567890abcdef"'
        assert "environ" in suggestions[0].fixed or "${" in suggestions[0].fixed

    def test_suggest_api_key_fix_dictionary(self):
        """Test fixing API keys in dictionaries"""
        content = '{"api_key": "sk-test-123"}'
        suggestions = suggest_api_key_fix(content)

        assert len(suggestions) >= 1
        assert '"api_key": "sk-test-123"' in suggestions[0].original
        assert "${API_KEY}" in suggestions[0].fixed

    def test_suggest_api_key_fix_bearer_token(self):
        """Test fixing Bearer tokens"""
        content = 'headers = {"Authorization": "Bearer sk-proj-12345"}'
        suggestions = suggest_api_key_fix(content)

        assert len(suggestions) >= 1
        assert "Bearer" in suggestions[0].original
        assert "${AUTH_TOKEN}" in suggestions[0].fixed

    def test_suggest_api_key_fix_no_keys(self):
        """Test content with no API keys"""
        content = 'print("Hello, World!")'
        suggestions = suggest_api_key_fix(content)

        assert len(suggestions) == 0


class TestLLMAPIFixes:
    """Test LLM API fix suggestions"""

    def test_suggest_llm_api_fix_openai(self):
        """Test fixing OpenAI imports"""
        content = "from openai import OpenAI\nclient = OpenAI()"
        suggestions = suggest_llm_api_fix(content)

        assert len(suggestions) >= 1
        assert "from openai import OpenAI" in suggestions[0].original
        assert (
            "transformers" in suggestions[0].fixed
            or "local" in suggestions[0].fixed.lower()
        )

    def test_suggest_llm_api_fix_google(self):
        """Test fixing Google Generative AI imports"""
        content = "import google.generativeai as genai"
        suggestions = suggest_llm_api_fix(content)

        assert len(suggestions) >= 1
        assert "google.generativeai" in suggestions[0].original
        assert "local" in suggestions[0].fixed.lower()

    def test_suggest_llm_api_fix_no_apis(self):
        """Test content with no LLM APIs"""
        content = "import pandas as pd"
        suggestions = suggest_llm_api_fix(content)

        assert len(suggestions) == 0


class TestDockerFixes:
    """Test Docker fix suggestions"""

    def test_suggest_docker_fix_dockerfile(self):
        """Test fixing Dockerfile issues"""
        content = "FROM ubuntu:latest"
        suggestions = suggest_docker_fix(content)

        assert len(suggestions) >= 1
        # Should suggest specific version
        assert any("specific-version" in s.fixed for s in suggestions)

    def test_suggest_docker_fix_run_command(self):
        """Test fixing docker run commands"""
        content = "docker run ubuntu bash"
        suggestions = suggest_docker_fix(content)

        assert len(suggestions) >= 1
        # Should suggest security options
        assert any("--security-opt" in s.fixed for s in suggestions)

    def test_suggest_docker_fix_no_docker(self):
        """Test content with no Docker commands"""
        content = 'print("No Docker here")'
        suggestions = suggest_docker_fix(content)

        assert len(suggestions) == 0


class TestLocalhostFixes:
    """Test localhost fix suggestions"""

    def test_suggest_localhost_fix_with_port(self):
        """Test fixing localhost with port"""
        content = 'url = "http://localhost:8080/api"'
        suggestions = suggest_localhost_fix(content)

        assert len(suggestions) >= 1
        assert "localhost:8080" in suggestions[0].original
        assert "${HOST}:${PORT}" in suggestions[0].fixed or "${" in suggestions[0].fixed

    def test_suggest_localhost_fix_ip_address(self):
        """Test fixing 127.0.0.1"""
        content = 'connect("127.0.0.1:3306")'
        suggestions = suggest_localhost_fix(content)

        assert len(suggestions) >= 1
        assert "127.0.0.1" in suggestions[0].original
        assert "${" in suggestions[0].fixed

    def test_suggest_localhost_fix_bind_address(self):
        """Test fixing 0.0.0.0 bind address"""
        content = 'server.listen("0.0.0.0:5000")'
        suggestions = suggest_localhost_fix(content)

        assert len(suggestions) >= 1
        assert "0.0.0.0" in suggestions[0].original
        assert "${BIND_ADDRESS}" in suggestions[0].fixed

    def test_suggest_localhost_fix_no_localhost(self):
        """Test content with no localhost"""
        content = 'url = "https://example.com"'
        suggestions = suggest_localhost_fix(content)

        assert len(suggestions) == 0


class TestSuggestFixesForContent:
    """Test the main suggest_fixes_for_content function"""

    def test_suggest_fixes_for_content_multiple_issues(self):
        """Test fixing content with multiple issue types"""
        content = """
api_key = "sk-123"
from openai import OpenAI
url = "http://localhost:8080"
"""
        issue_types = ["api_key", "llm_api", "localhost"]
        suggestions = suggest_fixes_for_content(content, issue_types)

        assert len(suggestions) >= 3
        # Should have fixes for each issue type
        issue_types_found = {s.issue_type for s in suggestions}
        assert "api_key" in issue_types_found
        assert "llm_api" in issue_types_found
        assert "localhost" in issue_types_found

    def test_suggest_fixes_for_content_single_issue(self):
        """Test fixing content with single issue type"""
        content = "docker run ubuntu:latest"
        suggestions = suggest_fixes_for_content(content, ["docker"])

        assert len(suggestions) >= 1
        assert all(s.issue_type == "docker" for s in suggestions)

    def test_suggest_fixes_for_content_no_issues(self):
        """Test content with no issues"""
        content = 'print("Hello, World!")'
        suggestions = suggest_fixes_for_content(content, ["api_key", "docker"])

        assert len(suggestions) == 0


class TestDisplayAutofixSuggestions:
    """Test display_autofix_suggestions function"""

    def test_display_no_suggestions(self, capsys):
        """Test displaying when no suggestions available"""
        display_autofix_suggestions([], no_color=True)
        captured = capsys.readouterr()

        assert "No auto-fix suggestions available" in captured.out

    def test_display_single_suggestion(self, capsys):
        """Test displaying single suggestion"""
        suggestion = AutoFixSuggestion(
            issue_type="api_key",
            original='key = "sk-123"',
            fixed='key = os.environ.get("API_KEY")',
            explanation="Use environment variable",
        )

        display_autofix_suggestions([suggestion], no_color=True)
        captured = capsys.readouterr()

        assert "Auto-fix Suggestions" in captured.out
        assert "API_KEY Issues:" in captured.out
        assert "Before:" in captured.out
        assert 'key = "sk-123"' in captured.out
        assert "After:" in captured.out
        assert 'os.environ.get("API_KEY")' in captured.out
        assert "Use environment variable" in captured.out

    def test_display_multiple_suggestions(self, capsys):
        """Test displaying multiple suggestions"""
        suggestions = [
            AutoFixSuggestion("api_key", 'a = "sk-1"', 'a = "${A}"', "Fix 1"),
            AutoFixSuggestion("api_key", 'b = "sk-2"', 'b = "${B}"', "Fix 2"),
            AutoFixSuggestion("docker", "FROM latest", "FROM 1.0", "Fix 3"),
        ]

        display_autofix_suggestions(suggestions, no_color=True)
        captured = capsys.readouterr()

        assert "API_KEY Issues:" in captured.out
        assert "DOCKER Issues:" in captured.out
        assert "Fix #1:" in captured.out
        assert "Fix #2:" in captured.out


class TestGenerateFixedContent:
    """Test generate_fixed_content function"""

    def test_generate_fixed_content_single_fix(self):
        """Test applying single fix"""
        content = 'api_key = "sk-123"'
        suggestion = AutoFixSuggestion(
            issue_type="api_key",
            original='api_key = "sk-123"',
            fixed='api_key = os.environ.get("API_KEY")',
            explanation="Use env var",
        )

        fixed = generate_fixed_content(content, [suggestion])
        assert 'os.environ.get("API_KEY")' in fixed
        assert "sk-123" not in fixed
        assert "import os" in fixed  # Should add import

    def test_generate_fixed_content_multiple_fixes(self):
        """Test applying multiple fixes"""
        content = """
api_key = "sk-123"
url = "http://localhost:8080"
"""
        suggestions = [
            AutoFixSuggestion(
                "api_key",
                'api_key = "sk-123"',
                'api_key = os.environ.get("API_KEY")',
                "Fix 1",
            ),
            AutoFixSuggestion(
                "localhost", "localhost:8080", "${HOST}:${PORT}", "Fix 2"
            ),
        ]

        fixed = generate_fixed_content(content, suggestions)
        assert "os.environ.get" in fixed
        assert "${HOST}:${PORT}" in fixed
        assert "sk-123" not in fixed
        assert "localhost:8080" not in fixed

    def test_generate_fixed_content_import_already_present(self):
        """Test when import os is already present"""
        content = '''import os
api_key = "sk-123"'''

        suggestion = AutoFixSuggestion(
            issue_type="api_key",
            original='api_key = "sk-123"',
            fixed='api_key = os.environ.get("API_KEY")',
            explanation="Use env var",
        )

        fixed = generate_fixed_content(content, [suggestion])
        # Should not add duplicate import
        assert fixed.count("import os") == 1
