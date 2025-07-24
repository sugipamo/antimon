# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Error context and helpful suggestions for antimon
"""


from .color_utils import Colors, apply_color
from .constants import GITHUB_REPO_URL
from .runtime_config import get_runtime_config


class ErrorContext:
    """Provides context and suggestions for security violations."""

    def __init__(self, no_color: bool = False):
        self.no_color = no_color

    def get_context_for_error(self, message: str, hook_data: dict) -> str:
        """Get contextual information and suggestions for an error."""
        context_lines = []

        # Extract key information from hook data
        tool_name = hook_data.get("tool_name", "")
        tool_input = hook_data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")

        # Add file context if available
        if file_path:
            context_lines.append(
                apply_color(f"📄 File: {file_path}", Colors.BOLD, self.no_color)
            )

        # Add tool context
        if tool_name:
            context_lines.append(
                apply_color(f"🔧 Tool: {tool_name}", Colors.BOLD, self.no_color)
            )

        # Get specific suggestions based on error type
        suggestions = self._get_suggestions(message, hook_data)
        if suggestions:
            context_lines.append("")  # Empty line
            context_lines.append(
                apply_color("💡 Suggestions:", Colors.OKBLUE, self.no_color)
            )
            for suggestion in suggestions:
                context_lines.append(f"   • {suggestion}")

        # Add FAQ link for common errors
        faq_link = self._get_faq_link(message)
        if faq_link:
            context_lines.append("")
            context_lines.append(
                apply_color(f"📚 Learn more: {faq_link}", Colors.OKBLUE, self.no_color)
            )

        return "\n".join(context_lines)

    def _get_suggestions(self, message: str, hook_data: dict) -> list[str]:
        """Get specific suggestions based on the error message."""
        suggestions = []

        # API key detection
        if "API key" in message:
            suggestions.extend(
                [
                    "Use environment variables instead: os.environ.get('API_KEY')",
                    "Store secrets in a .env file (add to .gitignore)",
                    "For examples/docs, use placeholders like 'your-api-key-here'",
                ]
            )

        # Sensitive file access
        elif "sensitive file" in message:
            file_path = hook_data.get("tool_input", {}).get("file_path", "")
            if "/etc/" in file_path:
                suggestions.extend(
                    [
                        "Use user-specific config files instead (e.g., ~/.config/)",
                        "Read from project-local configuration files",
                    ]
                )
            elif ".ssh" in file_path:
                suggestions.extend(
                    [
                        "SSH keys should not be modified by AI tools",
                        "Consider using SSH agent or key management tools",
                    ]
                )

        # LLM API usage
        elif "LLM API" in message or "external AI" in message:
            suggestions.extend(
                [
                    "Consider using local models or approved internal APIs",
                    "Use the AI assistant's built-in capabilities instead",
                    "For demos, use mock responses instead of real API calls",
                ]
            )

        # Docker operations
        elif "Docker" in message:
            suggestions.extend(
                [
                    "Use docker-compose for container management",
                    "Consider using development containers instead",
                    "Review Docker security best practices",
                ]
            )

        # Localhost connections
        elif "localhost" in message:
            suggestions.extend(
                [
                    "Use environment-specific configuration",
                    "Consider using service discovery instead of hardcoded URLs",
                    "Use reverse proxies for local development",
                ]
            )

        # Dangerous bash commands
        elif "dangerous command" in message or "bash" in message.lower():
            suggestions.extend(
                [
                    "Use safer alternatives or built-in tools",
                    "Consider using Python/Node.js scripts instead of shell commands",
                    "Always validate and sanitize inputs",
                ]
            )

        return suggestions

    def _get_faq_link(self, message: str) -> str | None:
        """Get a relevant FAQ link based on the error."""
        base_url = f"{GITHUB_REPO_URL}/blob/main/docs/faq.md"

        if "API key" in message:
            return f"{base_url}#api-key-false-positives"
        elif "sensitive file" in message:
            return f"{base_url}#sensitive-file-access"
        elif "LLM API" in message:
            return f"{base_url}#llm-api-alternatives"

        return None

    def format_error_with_context(
        self, message: str, hook_data: dict, exit_code: int = 2
    ) -> str:
        """Format an error message with full context."""
        lines = []
        config = get_runtime_config()

        # Main error message
        lines.append(
            apply_color("❌ Security issue detected:", Colors.FAIL, self.no_color)
        )
        lines.append(f"   {message}")

        # In brief mode, just show the core error and recovery hint
        if config.brief:
            lines.append("")
            lines.append(
                apply_color(
                    "💡 Check the error output above for details",
                    Colors.OKBLUE,
                    self.no_color,
                )
            )
        else:
            lines.append("")
            # Add context
            context = self.get_context_for_error(message, hook_data)
            if context:
                lines.append(context)

            # Add error recovery hint
            lines.append("")
            lines.append(
                apply_color(
                    "💡 For more details and solutions:", Colors.OKBLUE, self.no_color
                )
            )
            lines.append("   Check the detailed error information above")

        # Add exit code documentation
        lines.append("")
        lines.append(
            apply_color(
                f"Exit code: {exit_code} (Security issue detected)",
                Colors.WARNING,
                self.no_color,
            )
        )

        return "\n".join(lines)


def show_error_help(no_color: bool = False) -> None:
    """Show help for dealing with antimon errors."""
    print()
    print(apply_color("🆘 Dealing with antimon blocks:", Colors.HEADER, no_color))
    print(apply_color("=" * 40, Colors.HEADER, no_color))
    print()
    print("If antimon blocked your operation:")
    print()
    print(
        "1. " + apply_color("Read the error message carefully", Colors.BOLD, no_color)
    )
    print("   It explains what was detected and why it's dangerous")
    print()
    print("2. " + apply_color("Check the suggestions", Colors.BOLD, no_color))
    print("   antimon provides safer alternatives for most blocks")
    print()
    print("3. " + apply_color("For false positives:", Colors.BOLD, no_color))
    print("   • Use clearly fake values in examples")
    print("   • Split sensitive strings in documentation")
    print("   • Use environment variables for real secrets")
    print()
    print("4. " + apply_color("Need to bypass temporarily?", Colors.BOLD, no_color))
    print("   • Disable the hook: claude-code config unset hooks.PreToolUse")
    print("   • Re-enable after: claude-code config set hooks.PreToolUse antimon")
    print()
    print(apply_color("📚 Full documentation:", Colors.OKBLUE, no_color), end=" ")
    print(f"{GITHUB_REPO_URL}/blob/main/README.md")
    print()
