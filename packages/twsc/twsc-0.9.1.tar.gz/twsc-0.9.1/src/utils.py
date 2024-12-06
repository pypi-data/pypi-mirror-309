import os

excluded_dirs = [
    "venv",            # Python virtual environment
    "node_modules",    # Node.js
    ".git",            # Git repository
    "__pycache__",     # Python bytecode cache
    ".mvn",            # Maven (Java)
    "target",          # Maven/Gradle build output (Java)
    ".gradle",         # Gradle (Java)
    ".idea",           # IntelliJ IDEA project files
    ".vscode",         # Visual Studio Code project files
    "Rproj.user",      # RStudio project files
    ".Rhistory",       # R history files
    ".RData",          # R data files
    ".Rproj.user",     # RStudio project files
    "renv",            # R environment
    "env",             # Python virtual environment
    ".env",            # Python virtual environment
    "envs",            # Python virtual environment
    "Lib",             # Python virtual environment (Windows)
    "Include",         # Python virtual environment (Windows)
    "Scripts",         # Python virtual environment (Windows)
    "bin",             # Python virtual environment (Unix)
    "lib",             # Python virtual environment (Unix)
    "share",           # Python virtual environment (Unix)
    ".bundle",         # Bundler (Ruby)
    ".gem",            # RubyGems (Ruby)
    ".rbenv",          # rbenv (Ruby)
    ".rvm",            # RVM (Ruby)
    "vendor",          # Composer (PHP)
    "composer",        # Composer (PHP)
    "packages",        # Go modules
    "pkg",             # Go modules
    "Cargo.lock",      # Cargo (Rust)
    "Cargo.toml",      # Cargo (Rust)
    "nuget",           # NuGet (.NET)
    ".nuget",          # NuGet (.NET)
    "obj",             # .NET build output
    "bin",             # .NET build output
]

def is_virtualenv(directory):
    """For whoever decides to call their python virtual env: tommy or whatever
    I wrote this specially for you.
    """
    return (
        os.path.isfile(os.path.join(directory, 'pyvenv.cfg')) and
        (os.path.isdir(
            os.path.join(directory, 'bin')
            ) or
         os.path.isdir(
             os.path.join(directory, 'Scripts'))
        )
    )


def should_ignore_directory(directory):
    base_name = os.path.basename(directory)
    return base_name in excluded_dirs or is_virtualenv(directory)
