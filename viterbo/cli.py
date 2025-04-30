"""
Command-line interface for Viterbo.
"""

import argparse
import sys
from .collector import document_python_files


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Document Python files from a directory into a consolidated text file"
    )
    parser.add_argument("source_dir", help="Source directory containing Python files")
    parser.add_argument("output_file", help="Output file to write documentation")
    parser.add_argument(
        "--include-docstrings",
        action="store_true",
        help="Extract and include docstrings",
    )
    parser.add_argument(
        "--add-line-numbers", action="store_true", help="Add line numbers to the code"
    )

    args = parser.parse_args()

    success = document_python_files(
        args.source_dir,
        args.output_file,
        args.include_docstrings,
        args.add_line_numbers,
    )

    if not success:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
