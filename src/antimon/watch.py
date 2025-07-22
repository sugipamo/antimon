# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Watch mode functionality for antimon
"""

import glob
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from .color_utils import Colors, apply_color
from .core import check_file_directly
from .runtime_config import get_runtime_config


class FileWatcher:
    """Monitor files for changes and re-check modified files automatically"""

    def __init__(
        self,
        directory: str,
        verbose: bool = False,
        quiet: bool = False,
        no_color: bool = False,
        output_format: str = "text",
    ):
        self.directory = Path(directory).resolve()
        self.verbose = verbose
        self.quiet = quiet
        self.no_color = no_color
        self.output_format = output_format
        self.watched_files: dict[str, float] = {}  # file_path -> mtime
        self.last_check_time = time.time()
        self.check_count = 0
        self.issues_found = 0

    def scan_directory(self) -> set[str]:
        """Scan directory for Python files to watch"""
        patterns = [
            "**/*.py",
            "**/*.js",
            "**/*.ts",
            "**/*.jsx",
            "**/*.tsx",
            "**/*.yaml",
            "**/*.yml",
            "**/*.json",
            "**/*.sh",
            "**/*.bash",
        ]

        all_files = set()
        for pattern in patterns:
            files = glob.glob(str(self.directory / pattern), recursive=True)
            all_files.update(files)

        # Apply runtime config filters
        config = get_runtime_config()
        filtered_files = set()
        for file_path in all_files:
            if not config.is_file_ignored(file_path):
                filtered_files.add(file_path)

        return filtered_files

    def get_file_mtime(self, file_path: str) -> float:
        """Get file modification time"""
        try:
            return os.path.getmtime(file_path)
        except OSError:
            return 0.0

    def check_for_changes(self) -> set[str]:
        """Check for modified files since last scan"""
        changed_files = set()
        current_files = self.scan_directory()

        # Check for new files
        for file_path in current_files:
            if file_path not in self.watched_files:
                changed_files.add(file_path)
                self.watched_files[file_path] = self.get_file_mtime(file_path)

        # Check for modified files
        for file_path in list(self.watched_files.keys()):
            if file_path not in current_files:
                # File was deleted
                del self.watched_files[file_path]
            else:
                current_mtime = self.get_file_mtime(file_path)
                if current_mtime > self.watched_files[file_path]:
                    changed_files.add(file_path)
                    self.watched_files[file_path] = current_mtime

        return changed_files

    def check_file(self, file_path: str) -> bool:
        """Check a single file and return True if issues found"""
        self.check_count += 1
        result = check_file_directly(
            file_path,
            verbose=self.verbose,
            quiet=True,  # We'll handle output ourselves
            no_color=self.no_color,
            output_format="text",  # Get text for display
        )

        if result == 2:  # Security issue found
            self.issues_found += 1
            if not self.quiet:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(
                    f"\n{apply_color('[' + timestamp + ']', Colors.YELLOW, self.no_color)} "
                    f"Security issue in {apply_color(file_path, Colors.RED, self.no_color)}"
                )
            return True
        elif not self.quiet and self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(
                f"{apply_color('[' + timestamp + ']', Colors.GREEN, self.no_color)} "
                f"✓ {file_path}"
            )

        return False

    def display_status(self):
        """Display current watch status"""
        if not self.quiet:
            print(f"\n{'─' * 60}")
            print("📊 Watch Status:")
            print(f"   • Directory: {self.directory}")
            print(f"   • Files monitored: {len(self.watched_files)}")
            print(f"   • Checks performed: {self.check_count}")
            print(f"   • Issues found: {self.issues_found}")
            print(f"{'─' * 60}")

    def run(self):
        """Run the file watcher"""
        print(
            f"\n🔍 Starting watch mode for: {apply_color(str(self.directory), Colors.CYAN, self.no_color)}"
        )
        print(
            f"   Press {apply_color('Ctrl+C', Colors.YELLOW, self.no_color)} to stop watching"
        )

        # Initial scan
        if not self.quiet:
            print("\n📂 Scanning directory...")

        initial_files = self.scan_directory()
        for file_path in initial_files:
            self.watched_files[file_path] = self.get_file_mtime(file_path)

        if not self.quiet:
            print(f"   Found {len(initial_files)} files to monitor")

        # Initial check of all files
        if not self.quiet:
            print("\n🔎 Performing initial security check...")

        issues_in_initial = 0
        for file_path in initial_files:
            if self.check_file(file_path):
                issues_in_initial += 1

        if not self.quiet:
            if issues_in_initial > 0:
                print(f"\n⚠️  Found {issues_in_initial} files with security issues")
            else:
                print("\n✅ All files passed initial security check")

        self.display_status()

        # Watch loop
        try:
            while True:
                time.sleep(1)  # Check every second

                changed_files = self.check_for_changes()
                if changed_files:
                    for file_path in changed_files:
                        if not self.quiet:
                            print(
                                f"\n🔄 File modified: {apply_color(file_path, Colors.CYAN, self.no_color)}"
                            )
                        self.check_file(file_path)

                # Display status every 30 seconds if verbose
                if self.verbose and time.time() - self.last_check_time > 30:
                    self.display_status()
                    self.last_check_time = time.time()

        except KeyboardInterrupt:
            if not self.quiet:
                print("\n\n👋 Stopped watching")
                self.display_status()
            return 0


def watch_directory(
    directory: str,
    verbose: bool = False,
    quiet: bool = False,
    no_color: bool = False,
    output_format: str = "text",
) -> int:
    """
    Watch a directory for file changes and check modified files

    Args:
        directory: Directory to watch
        verbose: Enable verbose output
        quiet: Suppress non-error output
        no_color: Disable colored output
        output_format: Output format (text or json)

    Returns:
        Exit code (0 for success)
    """
    # Validate directory
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"\n❌ Error: Directory does not exist: {directory}", file=sys.stderr)
        return 1

    if not dir_path.is_dir():
        print(f"\n❌ Error: Not a directory: {directory}", file=sys.stderr)
        return 1

    # Create and run watcher
    watcher = FileWatcher(
        directory,
        verbose=verbose,
        quiet=quiet,
        no_color=no_color,
        output_format=output_format,
    )
    return watcher.run()
