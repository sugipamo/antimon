# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Color utilities for antimon terminal output
"""

import os
import sys


class Colors:
    """ANSI color codes for terminal output"""

    # Basic colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Styles
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Reset
    RESET = "\033[0m"

    # Semantic aliases
    HEADER = BOLD
    OKBLUE = BLUE
    OKGREEN = GREEN
    WARNING = YELLOW
    FAIL = RED
    INFO = CYAN


def supports_color() -> bool:
    """
    Check if the terminal supports color output

    Returns:
        True if color is supported, False otherwise
    """
    # Check if output is a TTY
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False

    # Check for NO_COLOR environment variable
    if os.environ.get("NO_COLOR"):
        return False

    # Check for TERM environment variable
    term = os.environ.get("TERM", "")
    if term == "dumb":
        return False

    # Check platform
    if sys.platform == "win32":
        # Windows 10+ supports ANSI colors
        try:
            import platform

            version = platform.version()
            major = int(version.split(".")[0])
            if major >= 10:
                # Enable ANSI color support on Windows 10+
                # Note: os.system('') is the documented way to enable ANSI on Windows
                # See: https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
                os.system("")  # This enables ANSI escape sequences
                return True
        except Exception:
            pass
        return False

    return True


class ColorFormatter:
    """Format text with colors for terminal output"""

    def __init__(self, use_color: bool | None = None):
        """
        Initialize color formatter

        Args:
            use_color: Force color on/off. If None, auto-detect.
        """
        if use_color is None:
            self.use_color = supports_color()
        else:
            self.use_color = use_color

    def _colorize(self, text: str, color: str, bold: bool = False) -> str:
        """Apply color to text if colors are enabled"""
        if not self.use_color:
            return text

        if bold:
            return f"{Colors.BOLD}{color}{text}{Colors.RESET}"
        return f"{color}{text}{Colors.RESET}"

    def error(self, text: str, bold: bool = True) -> str:
        """Format error messages in red"""
        return self._colorize(text, Colors.RED, bold)

    def success(self, text: str, bold: bool = True) -> str:
        """Format success messages in green"""
        return self._colorize(text, Colors.GREEN, bold)

    def warning(self, text: str, bold: bool = True) -> str:
        """Format warning messages in yellow"""
        return self._colorize(text, Colors.YELLOW, bold)

    def info(self, text: str, bold: bool = False) -> str:
        """Format info messages in blue"""
        return self._colorize(text, Colors.BLUE, bold)

    def highlight(self, text: str, bold: bool = True) -> str:
        """Format highlighted text in cyan"""
        return self._colorize(text, Colors.CYAN, bold)

    def bold(self, text: str) -> str:
        """Format text in bold"""
        if not self.use_color:
            return text
        return f"{Colors.BOLD}{text}{Colors.RESET}"

    def format_security_issue(self, message: str) -> str:
        """
        Format security issue messages with appropriate colors

        Args:
            message: The security issue message

        Returns:
            Formatted message with colors
        """
        lines = message.split("\n")
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
            elif line.startswith("Line "):
                # Format line number and matched text
                parts = line.split(":", 1)
                parts_count = len(parts)
                if parts_count == 2:
                    line_info = parts[0]
                    code = parts[1].strip()
                    formatted_lines.append(
                        f"      {self.highlight(line_info + ':')} {self.bold(code)}"
                    )
                else:
                    formatted_lines.append(f"      {line}")
            elif line.startswith("Pattern matched:"):
                formatted_lines.append(
                    f"      {self.warning('Pattern matched:')} {self.highlight(line.split(':', 1)[1].strip())}"
                )
            elif line.startswith("Why:"):
                formatted_lines.append(
                    f"      {self.info('Why:')} {line.split(':', 1)[1].strip()}"
                )
            elif line.startswith("Suggestion:"):
                formatted_lines.append(
                    f"      {self.success('Suggestion:')} {line.split(':', 1)[1].strip()}"
                )
            else:
                # Main error message
                formatted_lines.append(self.error(line))

        return "\n".join(formatted_lines)


def apply_color(text: str, color: str, no_color: bool = False) -> str:
    """
    Apply color to text if color is enabled

    Args:
        text: Text to colorize
        color: Color code from Colors class
        no_color: If True, don't apply color

    Returns:
        Colored text or original text if no_color is True
    """
    if no_color or not supports_color():
        return text

    return f"{color}{text}{Colors.RESET}"
