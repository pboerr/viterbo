# Viterbo

A tool to collect and document Python code from multiple files.

## Installation

```bash
pip install viterbo
```

## Usage

```bash
viterbo source_directory output_file [--include-docstrings] [--add-line-numbers]
```

### Options

-   `--include-docstrings`: Extract and include docstrings from modules, classes, and functions
-   `--add-line-numbers`: Add line numbers to the code

### Example

```bash
viterbo ./my_project ./project_documentation.txt --include-docstrings
```

## Features

-   Collects Python code from all files within a directory (including subdirectories)
-   Organizes code with clear section headers showing file paths
-   Optionally extracts and includes docstrings from modules, classes, and functions
-   Offers line numbering for easier reference
-   Creates a well-formatted documentation file that's easy to read and share

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/deinnovatie/viterbo.git
cd viterbo

# Install development dependencies
poetry install
```

### Running tests

```bash
poetry run pytest
```

### Building the package

```bash
poetry build
```

## License

MIT
