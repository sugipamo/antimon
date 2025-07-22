# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Auto-fix suggestions for common security issues
"""

import re

from .color_utils import ColorFormatter


class AutoFixSuggestion:
    """Container for an auto-fix suggestion"""

    def __init__(self, issue_type: str, original: str, fixed: str, explanation: str):
        self.issue_type = issue_type
        self.original = original
        self.fixed = fixed
        self.explanation = explanation


def suggest_api_key_fix(content: str) -> list[AutoFixSuggestion]:
    """Suggest fixes for API key issues"""
    suggestions = []

    # Pattern for direct API key assignments
    api_key_patterns = [
        # Function call (more specific, check first)
        (
            r'(api_key\s*=\s*["\'])([^"\']+)(["\'])',
            r'api_key=os.environ.get("API_KEY")',
            "Use os.environ",
        ),
        # Direct assignment with _KEY suffix
        (
            r'(\w+_KEY\s*=\s*["\'])([^"\']+)(["\'])',
            r"\g<1>${\g<1>}\g<3>",
            "Use environment variable",
        ),
        # Dictionary/JSON
        (
            r'(["\']api_key["\']\s*:\s*["\'])([^"\']+)(["\'])',
            r"\1${API_KEY}\3",
            "Use environment variable",
        ),
        # Bearer token
        (
            r"(Bearer\s+)([A-Za-z0-9\-._~+/]+)",
            r"Bearer ${AUTH_TOKEN}",
            "Use environment variable",
        ),
    ]

    for pattern, replacement, explanation in api_key_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            original = match.group(0)
            fixed = re.sub(pattern, replacement, original)
            suggestions.append(
                AutoFixSuggestion(
                    issue_type="api_key",
                    original=original,
                    fixed=fixed,
                    explanation=f"{explanation}. Store the key in .env file or environment",
                )
            )

    return suggestions


def suggest_llm_api_fix(content: str) -> list[AutoFixSuggestion]:
    """Suggest alternatives to external LLM APIs"""
    suggestions = []

    # LLM API alternatives
    llm_alternatives = {
        "from openai import OpenAI": "from transformers import AutoModelForCausalLM  # Use local Hugging Face models",
        "import openai": "import transformers  # Use local Hugging Face models instead",
        "openai.ChatCompletion.create": "model.generate  # Use local model inference",
        "import google.generativeai": "from transformers import pipeline  # Use local NLP pipeline",
        "anthropic.Anthropic()": "# Consider using local models or approved internal APIs",
    }

    for original, alternative in llm_alternatives.items():
        if original in content:
            suggestions.append(
                AutoFixSuggestion(
                    issue_type="llm_api",
                    original=original,
                    fixed=alternative,
                    explanation="Use local models or approved APIs instead of external LLM services",
                )
            )

    return suggestions


def suggest_docker_fix(content: str) -> list[AutoFixSuggestion]:
    """Suggest safer Docker practices"""
    suggestions = []

    # Docker security improvements
    docker_fixes = [
        # Run as non-root
        (r"FROM\s+(\S+)", r"FROM \1\nUSER nobody", "Run container as non-root user"),
        # Avoid latest tag
        (
            r"FROM\s+(\S+):latest",
            r"FROM \1:specific-version",
            "Use specific version instead of latest",
        ),
        # Add security options
        (
            r"docker run\s+([^-])",
            r"docker run --read-only --security-opt=no-new-privileges \1",
            "Add security options",
        ),
    ]

    for pattern, replacement, explanation in docker_fixes:
        matches = re.finditer(pattern, content)
        for match in matches:
            original = match.group(0)
            fixed = re.sub(pattern, replacement, original)
            suggestions.append(
                AutoFixSuggestion(
                    issue_type="docker",
                    original=original,
                    fixed=fixed,
                    explanation=explanation,
                )
            )

    return suggestions


def suggest_localhost_fix(content: str) -> list[AutoFixSuggestion]:
    """Suggest configuration-based alternatives to hardcoded localhost"""
    suggestions = []

    # Localhost patterns
    localhost_patterns = [
        (r"localhost:(\d+)", r"${HOST}:${PORT}", "Use environment variables"),
        (r"127\.0\.0\.1:(\d+)", r"${HOST}:${PORT}", "Use environment variables"),
        (r"http://localhost", r"${API_URL}", "Use configurable URL"),
        (
            r"0\.0\.0\.0:(\d+)",
            r"${BIND_ADDRESS}:${PORT}",
            "Use configurable bind address",
        ),
    ]

    for pattern, replacement, explanation in localhost_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            original = match.group(0)
            fixed = re.sub(pattern, replacement, original)
            suggestions.append(
                AutoFixSuggestion(
                    issue_type="localhost",
                    original=original,
                    fixed=fixed,
                    explanation=f"{explanation} for better portability",
                )
            )

    return suggestions


def suggest_fixes_for_content(
    content: str, issue_types: list[str]
) -> list[AutoFixSuggestion]:
    """
    Generate fix suggestions for detected issues

    Args:
        content: The code content with issues
        issue_types: List of detected issue types

    Returns:
        List of auto-fix suggestions
    """
    all_suggestions = []

    # Map issue types to suggestion functions
    suggestion_funcs = {
        "api_key": suggest_api_key_fix,
        "llm_api": suggest_llm_api_fix,
        "docker": suggest_docker_fix,
        "localhost": suggest_localhost_fix,
    }

    for issue_type in issue_types:
        if issue_type in suggestion_funcs:
            suggestions = suggestion_funcs[issue_type](content)
            all_suggestions.extend(suggestions)

    return all_suggestions


def display_autofix_suggestions(
    suggestions: list[AutoFixSuggestion], no_color: bool = False
):
    """Display auto-fix suggestions in a formatted way"""
    formatter = ColorFormatter(use_color=not no_color)

    if not suggestions:
        print(
            f"\n{formatter.info('ℹ️  No auto-fix suggestions available for this type of issue.')}"
        )
        return

    print(f"\n{formatter.bold('🔧 Auto-fix Suggestions')}")
    print(f"{'-' * 60}")

    # Group by issue type
    by_type: dict[str, list[AutoFixSuggestion]] = {}
    for suggestion in suggestions:
        if suggestion.issue_type not in by_type:
            by_type[suggestion.issue_type] = []
        by_type[suggestion.issue_type].append(suggestion)

    for issue_type, type_suggestions in by_type.items():
        print(f"\n{formatter.warning(f'{issue_type.upper()} Issues:')}")

        for i, suggestion in enumerate(type_suggestions, 1):
            print(f"\n  {formatter.bold(f'Fix #{i}:')}")
            print(f"  {formatter.error('Before:')} {suggestion.original}")
            print(f"  {formatter.success('After:')}  {suggestion.fixed}")
            print(f"  {formatter.info('Why:')}    {suggestion.explanation}")

    print(f"\n{'-' * 60}")
    print(
        f"{formatter.info('💡 Tip:')} Apply these fixes to make your code more secure."
    )
    print(
        f"{formatter.info('📝 Note:')} Remember to add required imports and configure environment variables.\n"
    )


def generate_fixed_content(content: str, suggestions: list[AutoFixSuggestion]) -> str:
    """
    Apply all suggestions to generate fixed content

    Args:
        content: Original content
        suggestions: List of fixes to apply

    Returns:
        Fixed content with all suggestions applied
    """
    fixed_content = content

    # Apply fixes in reverse order to maintain positions
    for suggestion in sorted(
        suggestions, key=lambda s: content.find(s.original), reverse=True
    ):
        fixed_content = fixed_content.replace(suggestion.original, suggestion.fixed)

    # Add necessary imports if not present
    if "os.environ" in fixed_content and "import os" not in fixed_content:
        fixed_content = "import os\n" + fixed_content

    return fixed_content
