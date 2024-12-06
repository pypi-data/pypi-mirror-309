# TWSC: Trailing Whitespace Cleaner

TWSC (Trailing Whitespace Cleaner) is a Python package designed to clean up trailing whitespace in code files efficiently. It works for files in Git repositories, untracked files, or even entire codebases when not in a Git environment.

---

## Features

1. **Clean Tracked Changes:**
   - Cleans only the changed lines in tracked files since the last commit.
   
2. **Handle Untracked Files:**
   - Cleans trailing whitespace from all untracked files in a Git repository.

3. **Full Codebase Cleanup:**
   - Offers to clean trailing whitespace from all files in the codebase when not in a Git repository.

4. **Supported Extensions:**
   - Python (`.py`), JavaScript (`.js`), TypeScript (`.ts`), Java (`.java`), Go (`.go`), C (`.c`), C++ (`.cpp`), Ruby (`.rb`), Shell (`.sh`), Rust (`.rs`), HTML (`.html`), CSS (`.css`).

---

## Installation

Install TWSC using pip:

```bash
pip install twsc
```

---

## Usage

### Command-Line Interface

Run `twsc` from the root of your project directory:

```bash
twsc
```

### Options

1. **Force Full Cleanup:**
   Use the `--force-clean-all` flag to clean the entire codebase, even if it’s a Git repository:

   ```bash
   twsc --force-clean-all
   ```

2. **Version Information:**
   Check the package version:

   ```bash
   twsc --version
   ```

---

## How It Works

### In a Git Repository:
1. **Tracked Files:**
   - Identifies lines changed since the last commit and cleans up only those lines.
2. **Untracked Files:**
   - Cleans up all lines in untracked files.

### Outside a Git Repository:
- Prompts the user to clean the entire codebase, targeting supported file types.

---

## Example

**Before Cleanup:**
```python
def example_function():     
    print("Hello, World!")      
    
```

**After Cleanup:**
```python
def example_function():
    print("Hello, World!")
```

---

## Logging

TWSC uses Python's `logging` module to provide detailed logs during execution. Logs are printed to the console in the following format:

```
2024-11-19 10:45:23 - INFO - Cleaning recently changed files.
2024-11-19 10:45:23 - INFO - Cleaned trailing whitespace in: file1.py
```

---

## For contribution and development

### Run Tests

Clone the repository and install dependencies:

```bash
git clone https://github.com/letsgogeeky/twsc.git
cd twsc
pip install -r requirements.txt
python -m unittest discover -s tests
```

---

## Contributing

Contributions are welcome! Feel free to:
1. Open an issue for bug reports or feature requests.
2. Submit pull requests for improvements.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Known Limitations

- **Unsupported Extensions:**
  - `.php` files are not supported for cleanup.
  
- **Non-Git Directories:**
  - Requires confirmation to clean the entire codebase.

---

Feel free to reach out if you have questions or issues with TWSC!