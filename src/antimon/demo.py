# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Interactive demo mode for antimon
"""

import sys
import time

from .color_utils import Colors, supports_color
from .core import validate_hook_data


class InteractiveDemo:
    """Interactive demonstration of antimon's detection capabilities."""

    def __init__(self):
        self.colors = Colors()
        self.color_enabled = supports_color()
        self.demo_cases = self._get_demo_cases()

    def _print_success(self, message: str):
        """Print success message in green."""
        if self.color_enabled:
            print(self.colors.GREEN + message + self.colors.RESET)
        else:
            print(message)

    def _print_error(self, message: str):
        """Print error message in red."""
        if self.color_enabled:
            print(self.colors.RED + message + self.colors.RESET)
        else:
            print(message)

    def _get_demo_cases(self) -> list[tuple[str, dict, bool, str]]:
        """Get list of demo cases: (description, hook_data, should_fail, explanation)"""
        return [
            # Case 1: Sensitive file access
            (
                "Attempt to write to /etc/passwd",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": "/etc/passwd",
                        "content": "root:x:0:0:root:/root:/bin/bash"
                    }
                },
                True,
                "This is blocked because /etc/passwd is a critical system file containing user account information."
            ),

            # Case 2: API key detection
            (
                "Hardcoded API key in Python code",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": "config.py",
                        "content": 'API_KEY = "sk-1234567890abcdef123456"'
                    }
                },
                True,
                "API keys should never be hardcoded. Use environment variables or secure vaults instead."
            ),

            # Case 3: SSH key access
            (
                "Reading SSH private key",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Read",
                    "tool_input": {
                        "file_path": "/home/user/.ssh/id_rsa"
                    }
                },
                True,
                "SSH private keys contain sensitive authentication credentials and should not be accessed."
            ),

            # Case 4: External LLM API usage
            (
                "Using OpenAI API in code",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": "chat.py",
                        "content": "from openai import OpenAI\nclient = OpenAI()\nresponse = client.chat.completions.create(model='gpt-4')"
                    }
                },
                True,
                "External LLM APIs should be avoided. Consider using local models like llama.cpp or ollama."
            ),

            # Case 5: Docker operation
            (
                "Creating a Dockerfile",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": "Dockerfile",
                        "content": "FROM python:3.9\nRUN pip install flask\nCMD ['python', 'app.py']"
                    }
                },
                True,
                "Docker operations are restricted for security reasons."
            ),

            # Case 6: Localhost connection
            (
                "Connecting to localhost service",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": "client.py",
                        "content": "import requests\nresponse = requests.get('http://localhost:8080/api')"
                    }
                },
                True,
                "Localhost connections to specific ports (like 8080) are monitored for security."
            ),

            # Case 7: Environment file
            (
                "Writing to .env file",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": ".env",
                        "content": "DATABASE_URL=postgresql://user:pass@localhost/db"
                    }
                },
                True,
                "Environment files often contain sensitive configuration and should be handled carefully."
            ),

            # Case 8: Safe operation - regular Python file
            (
                "Writing a simple Python script",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "tool_input": {
                        "file_path": "hello.py",
                        "content": "def greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('World'))"
                    }
                },
                False,
                "This is a safe operation - writing normal Python code without sensitive content."
            ),

            # Case 9: Safe operation - reading documentation
            (
                "Reading a README file",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Read",
                    "tool_input": {
                        "file_path": "README.md"
                    }
                },
                False,
                "Reading documentation files is perfectly safe."
            ),

            # Case 10: Edit operation with API key
            (
                "Editing code to add API key",
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Edit",
                    "tool_input": {
                        "file_path": "app.py",
                        "old_string": "# Configuration",
                        "new_string": "# Configuration\nAPI_KEY = 'sk-proj-abcdef123456'"
                    }
                },
                True,
                "Edit operations are also checked for sensitive content like API keys."
            )
        ]

    def run(self):
        """Run the interactive demo."""
        self._print_header()
        self._print_introduction()

        while True:
            choice = self._show_menu()

            if choice == '0':
                self._print_success("\nThank you for trying antimon!")
                break
            elif choice == 'a':
                self._run_all_demos()
            elif choice.isdigit() and 1 <= int(choice) <= len(self.demo_cases):
                self._run_single_demo(int(choice) - 1)
            elif choice == 'c':
                self._custom_demo()
            else:
                self._print_error("Invalid choice. Please try again.")

    def _print_header(self):
        """Print the demo header."""
        print("\n" + "="*60)
        print(self.colors.BOLD + "ANTIMON INTERACTIVE DEMO" + self.colors.RESET)
        print("="*60)

    def _print_introduction(self):
        """Print introduction text."""
        print("\nWelcome to the antimon interactive demo!")
        print("This demo will show you how antimon detects various security issues")
        print("in AI coding assistant operations.\n")

    def _show_menu(self) -> str:
        """Show the demo menu and get user choice."""
        print("\n" + self.colors.BOLD + "Available Demos:" + self.colors.RESET)
        print("-" * 40)

        for i, (desc, _, should_fail, _) in enumerate(self.demo_cases, 1):
            status = self.colors.RED + "[BLOCKED]" + self.colors.RESET if should_fail else self.colors.GREEN + "[ALLOWED]" + self.colors.RESET
            print(f"{i}. {desc} {status}")

        print("\n" + self.colors.BOLD + "Options:" + self.colors.RESET)
        print("a. Run all demos")
        print("c. Try custom input")
        print("0. Exit demo")

        return input("\n" + self.colors.CYAN + "Choose an option: " + self.colors.RESET).strip().lower()

    def _run_all_demos(self):
        """Run all demo cases."""
        print("\n" + self.colors.BOLD + "Running all demos..." + self.colors.RESET)
        print("="*60)

        for i, demo in enumerate(self.demo_cases):
            self._run_single_demo(i)
            if i < len(self.demo_cases) - 1:
                input("\n" + self.colors.CYAN + "Press Enter to continue..." + self.colors.RESET)

    def _run_single_demo(self, index: int):
        """Run a single demo case."""
        desc, hook_data, should_fail, explanation = self.demo_cases[index]

        print(f"\n{self.colors.BOLD}Demo {index + 1}: {desc}{self.colors.RESET}")
        print("-" * 60)

        # Show the operation
        print(self.colors.CYAN + "Operation:" + self.colors.RESET)
        print(f"  Tool: {hook_data['tool_name']}")

        tool_input = hook_data['tool_input']
        if 'file_path' in tool_input:
            print(f"  File: {tool_input['file_path']}")

        if 'content' in tool_input:
            print("  Content Preview:")
            content_lines = tool_input['content'].split('\n')
            for line in content_lines[:3]:  # Show first 3 lines
                print(f"    {line}")
            if len(content_lines) > 3:
                print(f"    ... ({len(content_lines) - 3} more lines)")

        if 'old_string' in tool_input and 'new_string' in tool_input:
            print(f"  Replacing: {tool_input['old_string']!r}")
            print(f"  With: {tool_input['new_string']!r}")

        # Simulate running antimon
        print(f"\n{self.colors.CYAN}Running antimon...{self.colors.RESET}")
        time.sleep(0.5)  # Small delay for effect

        # Run actual validation
        has_issues, messages = validate_hook_data(hook_data)

        # Show result
        if has_issues:
            self._print_error("\n✗ BLOCKED: Security issue detected")
            for msg in messages:
                print(f"  • {msg}")
        else:
            self._print_success("\n✓ ALLOWED: No security issues detected")

        # Show explanation
        print(f"\n{self.colors.BOLD}Explanation:{self.colors.RESET}")
        print(f"  {explanation}")

        # Verify expectation
        if has_issues != should_fail:
            self._print_error("\n⚠️  UNEXPECTED RESULT!")

    def _custom_demo(self):
        """Allow user to try custom input."""
        print(f"\n{self.colors.BOLD}Custom Demo Mode{self.colors.RESET}")
        print("Create your own test case to see how antimon responds.")
        print("-" * 60)

        # Get tool name
        print("\nAvailable tools: Write, Read, Edit, MultiEdit")
        tool_name = input(self.colors.CYAN + "Tool name: " + self.colors.RESET).strip()

        if tool_name not in ["Write", "Read", "Edit", "MultiEdit"]:
            self._print_error("Invalid tool name")
            return

        # Get file path
        file_path = input(self.colors.CYAN + "File path: " + self.colors.RESET).strip()

        # Build tool_input based on tool
        tool_input = {"file_path": file_path}

        if tool_name == "Write":
            print("Enter content (type 'END' on a new line when done):")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            tool_input["content"] = "\n".join(lines)

        elif tool_name == "Edit":
            old_string = input(self.colors.CYAN + "Text to replace: " + self.colors.RESET)
            new_string = input(self.colors.CYAN + "Replace with: " + self.colors.RESET)
            tool_input["old_string"] = old_string
            tool_input["new_string"] = new_string

        # Create hook data
        hook_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "tool_input": tool_input
        }

        # Run validation
        print(f"\n{self.colors.CYAN}Running antimon...{self.colors.RESET}")
        has_issues, messages = validate_hook_data(hook_data)

        # Show result
        if has_issues:
            self._print_error("\n✗ BLOCKED: Security issue detected")
            for msg in messages:
                print(f"  • {msg}")
        else:
            self._print_success("\n✓ ALLOWED: No security issues detected")


def run_demo(non_interactive: bool = False):
    """Entry point for the demo command.
    
    Args:
        non_interactive: Run in non-interactive mode (automatic demo)
    """
    if non_interactive:
        demo = NonInteractiveDemo()
    else:
        demo = InteractiveDemo()

    try:
        demo.run()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
        sys.exit(0)


class NonInteractiveDemo(InteractiveDemo):
    """Non-interactive demo mode."""

    def run(self):
        """Run non-interactive demo mode (automatic demonstration)."""
        print("\n" + "=" * 70)
        print(f"{self.colors.BOLD}antimon Non-Interactive Demo{self.colors.RESET}")
        print("=" * 70 + "\n")

        print("This demo shows what antimon can detect and block.\n")

        # Run through all demo cases
        for i, (description, hook_data, should_fail, explanation) in enumerate(self.demo_cases):
            print(f"{self.colors.BOLD}[{i+1}/{len(self.demo_cases)}] {description}{self.colors.RESET}")
            print("-" * 50)

            # Show the operation being tested
            print(f"{self.colors.CYAN}Tool:{self.colors.RESET} {hook_data['tool_name']}")
            if 'file_path' in hook_data['tool_input']:
                print(f"{self.colors.CYAN}File:{self.colors.RESET} {hook_data['tool_input']['file_path']}")

            # Show a snippet of content
            content = hook_data['tool_input'].get('content', '')
            if content:
                snippet = content[:100] + "..." if len(content) > 100 else content
                print(f"{self.colors.CYAN}Content:{self.colors.RESET} {snippet}")

            # Run validation
            print(f"\n{self.colors.CYAN}Running antimon...{self.colors.RESET}")
            time.sleep(0.5)  # Small delay for visual effect

            has_issues, messages, _ = validate_hook_data(hook_data)

            # Show result
            if has_issues:
                self._print_error("✗ BLOCKED")
                if messages:
                    print(f"{self.colors.YELLOW}Reason:{self.colors.RESET} {messages[0].split('\n')[0]}")
            else:
                self._print_success("✓ ALLOWED")

            # Verify expected result
            if has_issues == should_fail:
                self._print_success("✓ Result matches expectation")
            else:
                self._print_error("✗ Unexpected result!")

            print(f"\n{self.colors.CYAN}Explanation:{self.colors.RESET} {explanation}")
            print()

            # Pause between demos
            if i < len(self.demo_cases) - 1:
                time.sleep(1)

        print("=" * 70)
        print(f"{self.colors.BOLD}Demo Complete!{self.colors.RESET}")
        print("=" * 70)
        print("\nTo run antimon on your own content:")
        print("  • JSON input:    echo '{...}' | antimon")
        print("  • Check file:    antimon --check-file yourfile.py")
        print("  • Check content: antimon --check-content 'your code here'")
        print("\nTo integrate with Claude Code:")
        print("  • Run: antimon --setup-claude-code")
        print()
