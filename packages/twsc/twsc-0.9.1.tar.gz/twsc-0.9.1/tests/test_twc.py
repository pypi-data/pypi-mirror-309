import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import subprocess
import tempfile
from src import (
    is_git_repository,
    clean_file_trailing_whitespace,
    clean_entire_codebase,
    clean_untracked_files,
    clean_tracked_files,
    clean_trailing_whitespace
)


class TestTrailingWhitespaceCleaner(unittest.TestCase):

    @patch("subprocess.run")
    def test_is_git_repository_true(self, mock_run):
        """Test is_git_repository() when the directory is a Git repository."""
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(is_git_repository())
        mock_run.assert_called_once_with(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True)

    @patch("subprocess.run")
    def test_is_git_repository_false(self, mock_run):
        """Test is_git_repository() when the directory is not a Git repository."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")
        self.assertFalse(is_git_repository())

    @patch("builtins.open", new_callable=mock_open, read_data="line1 \nline2\t\nline3   \n")
    def test_clean_file_trailing_whitespace(self, mock_file):
        """Test clean_file_trailing_whitespace() removes trailing whitespace."""
        file_path = "dummy_file.py"
        clean_file_trailing_whitespace(file_path)
        mock_file.assert_called_with(file_path, "w")
        mock_file().write.assert_any_call("line1\n")
        mock_file().write.assert_any_call("line2\n")
        mock_file().write.assert_any_call("line3\n")

    @patch("src.clean_file_trailing_whitespace")
    def test_clean_entire_codebase(self, mock_clean_file):
        """Test clean_entire_codebase() with a mocked temporary directory."""
        # Create a temporary directory with mock files
        directory = os.getcwd()
        with tempfile.TemporaryDirectory(dir=directory) as temp_dir:
            # Create some files
            supported_file = os.path.join(temp_dir, "file1.py")
            unsupported_file = os.path.join(temp_dir, "file2.txt")
            nested_dir = os.path.join(temp_dir, "nested")
            os.mkdir(nested_dir)
            nested_supported_file = os.path.join(nested_dir, "file3.js")

            with open(supported_file, "w") as f:
                f.write("line1 \nline2   \n")

            with open(unsupported_file, "w") as f:
                f.write("This should not be cleaned.\n")

            with open(nested_supported_file, "w") as f:
                f.write("nested line1 \n")

            # Run the function
            with patch("builtins.input", return_value="y"):
                clean_entire_codebase(temp_dir)

            # Verify that clean_file_trailing_whitespace was called only for supported files
            mock_clean_file.assert_any_call(supported_file)
            mock_clean_file.assert_any_call(nested_supported_file)

            # mock_clean_file.assert_no_call(unsupported_file)

    @patch("src.clean_file_trailing_whitespace")
    def test_clean_entire_codebase_empty_dir(self, mock_clean_file):
        """Test clean_entire_codebase() with an empty temporary directory."""
        directory = os.getcwd()
        with tempfile.TemporaryDirectory(dir=directory) as temp_dir:
            # Run the function on an empty directory
            os.chdir(temp_dir)  # Ensure the function operates within the temp dir
            with patch("builtins.input", return_value="y"):
                clean_entire_codebase(temp_dir)

            # Verify no files were cleaned
            mock_clean_file.assert_not_called()

    @patch("subprocess.run")
    @patch("src.clean_file_trailing_whitespace")
    def test_clean_untracked_files(self, mock_clean_file, mock_run):
        """Test clean_untracked_files() processes untracked files."""
        mock_run.return_value.stdout = "untracked1.py\nuntracked2.js\n"
        mock_clean_file.reset_mock()
        clean_untracked_files()
        mock_clean_file.assert_any_call("untracked1.py")
        mock_clean_file.assert_any_call("untracked2.js")
        self.assertEqual(mock_clean_file.call_count, 2)

    @patch("subprocess.run")
    @patch("src.clean_file_trailing_whitespace")
    def test_clean_tracked_files(self, mock_clean_file, mock_run):
        """Test clean_tracked_files() cleans only changed lines."""
        mock_run.return_value.stdout = """diff --git a/file1.py b/file1.py
@@ -1,3 +1,3 @@
 line1
 line2
 line3
"""
        with patch("builtins.open", mock_open(read_data="line1\nline2 \nline3\n")) as mock_file:
            clean_tracked_files()
            mock_clean_file.assert_called_once_with("file1.py")

    @patch("src.clean_entire_codebase")
    @patch("src.clean_untracked_files")
    @patch("src.clean_tracked_files")
    @patch("src.is_git_repository")
    def test_clean_trailing_whitespace_force_clean(self, mock_is_git, mock_clean_tracked, mock_clean_untracked, mock_clean_all):
        """Test clean_trailing_whitespace() with --force-clean-all flag."""
        mock_is_git.return_value = True
        with patch("sys.argv", ["program_name", "--force-clean-all"]):
            clean_trailing_whitespace()
            mock_clean_all.assert_called_once()
            mock_clean_tracked.assert_not_called()
            mock_clean_untracked.assert_not_called()

    @patch("src.clean_entire_codebase")
    @patch("src.clean_untracked_files")
    @patch("src.clean_tracked_files")
    @patch("src.is_git_repository")
    def test_clean_trailing_whitespace_in_git_repo(self, mock_is_git, mock_clean_tracked, mock_clean_untracked, mock_clean_all):
        """Test clean_trailing_whitespace() in a Git repository."""
        mock_is_git.return_value = True
        with patch("sys.argv", ["program_name"]):
            clean_trailing_whitespace()
            mock_clean_tracked.assert_called_once()
            mock_clean_untracked.assert_called_once()
            mock_clean_all.assert_not_called()

    @patch("src.clean_entire_codebase")
    @patch("src.is_git_repository")
    def test_clean_trailing_whitespace_non_git(self, mock_is_git, mock_clean_all):
        """Test clean_trailing_whitespace() in a non-Git repository."""
        mock_is_git.return_value = False
        with patch("sys.argv", ["program_name"]):
            clean_trailing_whitespace()
            mock_clean_all.assert_called_once()

if __name__ == "__main__":
    unittest.main()
