# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Tests for watch mode functionality
"""

import tempfile
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

from antimon.watch import FileWatcher, watch_directory


class TestFileWatcher:
    """Test FileWatcher class"""

    def test_init(self):
        """Test FileWatcher initialization"""
        watcher = FileWatcher("/tmp", verbose=True, quiet=False, no_color=True)
        assert watcher.directory == Path("/tmp").resolve()
        assert watcher.verbose is True
        assert watcher.quiet is False
        assert watcher.no_color is True
        assert watcher.output_format == "text"
        assert watcher.watched_files == {}
        assert watcher.check_count == 0
        assert watcher.issues_found == 0

    def test_scan_directory(self, tmp_path):
        """Test directory scanning"""
        # Create test files
        (tmp_path / "test.py").write_text("print('hello')")
        (tmp_path / "config.json").write_text("{}")
        (tmp_path / "script.sh").write_text("#!/bin/bash")
        (tmp_path / "ignore.txt").write_text("ignored")

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "nested.py").write_text("# nested file")

        watcher = FileWatcher(str(tmp_path))
        files = watcher.scan_directory()

        # Should find Python, JSON, and shell files
        assert len(files) >= 3
        assert any("test.py" in f for f in files)
        assert any("config.json" in f for f in files)
        assert any("script.sh" in f for f in files)
        assert any("nested.py" in f for f in files)
        assert not any("ignore.txt" in f for f in files)

    def test_get_file_mtime(self, tmp_path):
        """Test getting file modification time"""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        watcher = FileWatcher(str(tmp_path))
        mtime = watcher.get_file_mtime(str(test_file))
        assert mtime > 0

        # Non-existent file should return 0
        assert watcher.get_file_mtime("/non/existent/file") == 0.0

    def test_check_for_changes(self, tmp_path):
        """Test detecting file changes"""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        watcher = FileWatcher(str(tmp_path))

        # Initial scan - should detect the file as new
        changes = watcher.check_for_changes()
        assert len(changes) == 1
        assert any("test.py" in f for f in changes)

        # No changes - should return empty
        changes = watcher.check_for_changes()
        assert len(changes) == 0

        # Modify file
        time.sleep(0.01)  # Ensure mtime changes
        test_file.write_text("print('modified')")

        changes = watcher.check_for_changes()
        assert len(changes) == 1
        assert any("test.py" in f for f in changes)

        # Add new file
        new_file = tmp_path / "new.py"
        new_file.write_text("# new file")

        changes = watcher.check_for_changes()
        assert len(changes) == 1
        assert any("new.py" in f for f in changes)

        # Delete file
        test_file.unlink()
        changes = watcher.check_for_changes()
        assert len(changes) == 0  # Deletion doesn't show as change
        assert str(test_file) not in watcher.watched_files

    @patch("antimon.watch.check_file_directly")
    def test_check_file(self, mock_check):
        """Test checking individual files"""
        watcher = FileWatcher("/tmp", quiet=True)

        # Test with no issues
        mock_check.return_value = 0
        result = watcher.check_file("/tmp/safe.py")
        assert result is False
        assert watcher.check_count == 1
        assert watcher.issues_found == 0

        # Test with security issue
        mock_check.return_value = 2
        result = watcher.check_file("/tmp/dangerous.py")
        assert result is True
        assert watcher.check_count == 2
        assert watcher.issues_found == 1

    @patch("antimon.watch.check_file_directly")
    def test_check_file_output(self, mock_check, capsys):
        """Test check_file output formatting"""
        # Test quiet mode
        watcher = FileWatcher("/tmp", quiet=True)
        mock_check.return_value = 2
        watcher.check_file("/tmp/test.py")
        captured = capsys.readouterr()
        assert captured.out == ""

        # Test normal mode with issue
        watcher = FileWatcher("/tmp", quiet=False, no_color=True)
        mock_check.return_value = 2
        watcher.check_file("/tmp/test.py")
        captured = capsys.readouterr()
        assert "Security issue" in captured.out
        assert "/tmp/test.py" in captured.out

        # Test verbose mode with no issue
        watcher = FileWatcher("/tmp", quiet=False, verbose=True, no_color=True)
        mock_check.return_value = 0
        watcher.check_file("/tmp/safe.py")
        captured = capsys.readouterr()
        assert "✓" in captured.out
        assert "safe.py" in captured.out

    def test_display_status(self, capsys):
        """Test status display"""
        watcher = FileWatcher("/tmp", quiet=False)
        watcher.watched_files = {"file1": 1.0, "file2": 2.0}
        watcher.check_count = 5
        watcher.issues_found = 2

        watcher.display_status()
        captured = capsys.readouterr()

        assert "Watch Status:" in captured.out
        assert "Directory: /tmp" in captured.out
        assert "Files monitored: 2" in captured.out
        assert "Checks performed: 5" in captured.out
        assert "Issues found: 2" in captured.out

        # Test quiet mode
        watcher.quiet = True
        watcher.display_status()
        captured = capsys.readouterr()
        assert captured.out == ""


class TestWatchDirectory:
    """Test watch_directory function"""

    def test_watch_directory_invalid_path(self, capsys):
        """Test watch_directory with invalid paths"""
        # Non-existent directory
        result = watch_directory("/non/existent/path")
        assert result == 1
        captured = capsys.readouterr()
        assert "Directory does not exist" in captured.err

        # File instead of directory
        with tempfile.NamedTemporaryFile() as f:
            result = watch_directory(f.name)
            assert result == 1
            captured = capsys.readouterr()
            assert "Not a directory" in captured.err

    @patch("antimon.watch.FileWatcher")
    def test_watch_directory_valid(self, mock_watcher_class, tmp_path):
        """Test watch_directory with valid directory"""
        mock_watcher = MagicMock()
        mock_watcher.run.return_value = 0
        mock_watcher_class.return_value = mock_watcher

        result = watch_directory(
            str(tmp_path),
            verbose=True,
            quiet=False,
            no_color=True,
            output_format="json",
        )

        assert result == 0
        mock_watcher_class.assert_called_once_with(
            str(tmp_path),
            verbose=True,
            quiet=False,
            no_color=True,
            output_format="json",
        )
        mock_watcher.run.assert_called_once()


class TestWatcherIntegration:
    """Integration tests for watch mode"""

    @patch("antimon.watch.time.sleep")
    @patch("antimon.watch.check_file_directly")
    def test_run_initial_scan(self, mock_check, mock_sleep, tmp_path, capsys):
        """Test initial scan and check"""
        # Create test files
        (tmp_path / "safe.py").write_text("print('hello')")
        (tmp_path / "dangerous.py").write_text("api_key = 'sk-12345'")

        # Mock check results
        def check_side_effect(file_path, **kwargs):
            if "dangerous.py" in file_path:
                return 2  # Security issue
            return 0  # Safe

        mock_check.side_effect = check_side_effect

        # Simulate Ctrl+C after initial scan
        mock_sleep.side_effect = KeyboardInterrupt

        watcher = FileWatcher(str(tmp_path), quiet=False, no_color=True)
        result = watcher.run()

        assert result == 0
        assert watcher.check_count == 2
        assert watcher.issues_found == 1

        captured = capsys.readouterr()
        assert "Starting watch mode" in captured.out
        assert "Found 2 files to monitor" in captured.out
        assert "Found 1 files with security issues" in captured.out
        assert "Stopped watching" in captured.out

    @patch("antimon.watch.time.sleep")
    @patch("antimon.watch.check_file_directly")
    def test_run_file_modification(self, mock_check, mock_sleep, tmp_path, capsys):
        """Test detecting and checking modified files"""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        mock_check.return_value = 0

        # Create a watcher
        watcher = FileWatcher(str(tmp_path), quiet=False, no_color=True)

        # Manually set up initial state
        watcher.watched_files[str(test_file)] = test_file.stat().st_mtime

        # Simulate file modification on second iteration
        def sleep_side_effect(duration):
            if mock_sleep.call_count == 2:
                time.sleep(0.01)  # Small delay
                test_file.write_text("print('modified')")
            elif mock_sleep.call_count > 3:
                raise KeyboardInterrupt

        mock_sleep.side_effect = sleep_side_effect

        # Run watcher
        result = watcher.run()

        assert result == 0
        captured = capsys.readouterr()
        assert "File modified:" in captured.out
        assert "test.py" in captured.out
