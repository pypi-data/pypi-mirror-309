import subprocess
import os
import sys
import logging
import pkg_resources
import argparse
from .utils import should_ignore_directory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

supported_ext = tuple([
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".c",
    ".cpp",
    ".rb",
    ".sh",
    ".rs",
    ".cs",
    ".html",
    ".css"
    # ".php" # not supported. the only cleanup possible is deleting the entire codebase!
])

def is_git_repository():
    """
    Check if the current directory is a Git repository.
    """
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True)
        logging.info("This is a Git repository.")
        return True
    except subprocess.CalledProcessError:
        logging.info("Not a Git repository.")
        return False

def clean_file_trailing_whitespace(file_path):
    """
    Remove trailing whitespace from all lines in a file.
    """
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        with open(file_path, "w") as f:
            for line in lines:
                f.write(line.rstrip() + "\n")
        logging.info(f"Cleaned trailing whitespace in: {file_path}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")


def clean_entire_codebase(directory):
    logging.info("Cleaning up the entire codebase...")
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not should_ignore_directory(d)]
        for file in files:
            if file.endswith(supported_ext):
                clean_file_trailing_whitespace(os.path.join(root, file))
    logging.info("Whitespace cleanup completed.")


def clean_untracked_files():
    """
    Clean up trailing whitespace in all untracked files.
    This function assumes that you manage your own gitignore such that:
        no unwanted untracked items dangling around.
    """
    try:
        # Get the list of untracked files
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True
        )
        untracked_files = result.stdout.splitlines()

        if not untracked_files:
            logging.info("No untracked files found.")
            return

        for file in untracked_files:
            if os.path.exists(file) and file.endswith(supported_ext):
                clean_file_trailing_whitespace(file)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving untracked files: {e}")


def clean_tracked_files():
    # Get the diff of changed lines since the last commit
    diff_output = subprocess.run(
        ["git", "diff", "--unified=0"],
        capture_output=True,
        text=True
    ).stdout

    if not diff_output.strip():
        logging.info("No changes detected since the last commit.")
        return

    file_changes = {}
    current_file = None

    # Parse the diff output
    for line in diff_output.splitlines():
        if line.startswith("diff --git"):
            # Identify the file being modified
            parts = line.split(" ")
            current_file = parts[-1].replace("b/", "", 1)
        elif line.startswith("@@"):
            # Extract line numbers from the hunk header
            hunk_header = line.split(" ")[2]
            start_line = int(hunk_header.split(",")[0].replace("+", ""))
            num_lines = int(hunk_header.split(",")[1]) if "," in hunk_header else 1

            if current_file not in file_changes:
                file_changes[current_file] = []
            file_changes[current_file].extend(range(start_line, start_line + num_lines))

    # Process the files
    for file, changed_lines in file_changes.items():
        try:
            with open(file, "r") as f:
                lines = f.readlines()

            with open(file, "w") as f:
                for i, line in enumerate(lines, start=1):
                    # Remove trailing whitespace only for changed lines
                    if i in changed_lines:
                        f.write(line.rstrip() + "\n")
                    else:
                        f.write(line)
            logging.info(f"Cleaned changes in: {file}")
        except FileNotFoundError:
            logging.error(f"File not found: {file}")
        except Exception as e:
            logging.error(f"Error processing {file}: {e}")

def prompt_cleanall() -> bool:
    """
    Offer to clean up trailing whitespace for the entire codebase.
    """
    confirm = input("This directory is not a Git repository. Would you like to clean up trailing whitespace for all files in the codebase? (y/n): ").strip().lower()
    if confirm != "y":
        logging.info("Operation canceled.")
        return False
    return True


def clean_trailing_whitespace():
    """
    Remove trailing whitespace from changed lines or the entire codebase.
    """

    version = pkg_resources.get_distribution("twsc").version
    parser = argparse.ArgumentParser(
        description="A tool to clean trailing whitespace from recently changed lines or an entire codebase.",
        epilog="For more information, visit https://github.com/letsgogeeky/twc"
    )
    parser.add_argument('--version', action='version', version=f"twsc {version}")
    parser.add_argument(
        '--force-clean-all', action='store_true',
        help="Force clean the entire codebase even if it's a git repository"
    )
    args = parser.parse_args()
    directory = "."  # by default it takes current directory
    if args.force_clean_all:
        logging.info("Force clean!!!")
        clean_entire_codebase(directory)
        return

    if not is_git_repository():
        if prompt_cleanall():
            clean_entire_codebase(directory)
        return

    logging.info("Start: Cleaning recently changed files.")
    clean_tracked_files()
    logging.info("End: Cleaning recently changed files.")
    logging.info("Start: Cleaning untracked files.")
    clean_untracked_files()
    logging.info("End: Cleaning untracked files.")
