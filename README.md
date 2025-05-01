# Viterbo

A tool for collecting and documenting code files for LLM context.

## Overview

Viterbo helps collect source code files from various languages and compile them into a readable format for inclusion in LLM prompts. It scans directories for code files, extracts structured information like docstrings and comments, and generates comprehensive documentation in text or markdown format.

## Features

-   **Multi-language support**: Python, C/C++, R, JavaScript, TypeScript, and many other languages
-   **Directory tree visualization**: Shows the structure of your codebase
-   **Documentation extraction**: Extracts docstrings, comments, and code structure
-   **Output formats**: Generate documentation in plain text or markdown
-   **README inclusion**: Optionally include README.md files in the documentation
-   **Line numbering**: Add line numbers to code for easy reference
-   **Organized output**: Collects code with clear section headers showing file paths

## Installation

```bash
# Install with Poetry
poetry install

# Or using pip
pip install viterbo
```

## Usage

### Command Line

```bash
# Basic usage (Python files only)
viterbo source_directory output_file [--include-docstrings] [--add-line-numbers]

# Enhanced usage with multi-language support
viterbo /path/to/source output.txt --extensions .py .cpp .h .R

# Include README.md files
viterbo /path/to/source output.txt --include-readme

# Extract and include docstrings/comments
viterbo /path/to/source output.txt --include-docstrings

# Add line numbers to code
viterbo /path/to/source output.txt --add-line-numbers

# Generate markdown output
viterbo /path/to/source output.md --format md
```

### Python API

```python
from viterbo import document_files

# Document Python and C++ files in markdown format
document_files(
    source_dir="/path/to/source",
    output_file="output.md",
    file_extensions=[".py", ".cpp", ".h"],
    include_readme=True,
    include_docstrings=True,
    add_line_numbers=True,
    output_format="md"
)

# For backward compatibility, the original function is still available
from viterbo import document_python_files

document_python_files(
    source_dir="/path/to/source",
    output_file="output.txt",
    include_docstrings=True,
    add_line_numbers=True
)
```

## Output Examples

### Text Output

```
# Code Documentation
# Generated on: 2025-05-01 10:21:33
# Source: /path/to/source

# Directory Structure:
/path/to/source/
├── README.md
├── src/
│   ├── main.py
│   └── utils.py
└── tests/
    └── test_main.py
...
```

### Markdown Output

The markdown output includes syntax highlighting and better formatting for documentation.

## Development

```bash
# Clone the repository
git clone https://github.com/pboerr/viterbo.git
cd viterbo

# Install development dependencies
poetry install

# Running tests
poetry run pytest

# Building the package
poetry build
```

## License

MIT
