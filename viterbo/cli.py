"""
Command-line interface for Viterbo.
"""

import argparse
import sys
from pathlib import Path
from .core.collector import document_files


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Document code files from a directory into a consolidated file"
    )
    parser.add_argument("source_dir", help="Source directory containing code files")
    parser.add_argument("output_file", help="Output file to write documentation")

    # File selection options
    file_group = parser.add_argument_group("File Selection")
    file_group.add_argument(
        "--extensions",
        nargs="+",
        default=[".py"],
        help="File extensions to include (e.g., .py .cpp .r)",
    )
    file_group.add_argument(
        "--include-readme",
        action="store_true",
        help="Include README.md files in the documentation",
    )

    # Content options
    content_group = parser.add_argument_group("Content Options")
    content_group.add_argument(
        "--include-docstrings",
        action="store_true",
        help="Extract and include docstrings and comments",
    )
    content_group.add_argument(
        "--add-line-numbers", action="store_true", help="Add line numbers to the code"
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "--format",
        choices=["txt", "md"],
        default="txt",
        help="Output format: text or markdown",
    )

    args = parser.parse_args()

    # Normalize file extensions to include the dot if missing
    extensions = []
    for ext in args.extensions:
        ext_str = str(ext)
        if ext_str.startswith("."):
            extensions.append(ext_str)
        else:
            extensions.append(f".{ext_str}")

    success = document_files(
        source_dir=args.source_dir,
        output_file=args.output_file,
        file_extensions=extensions,
        include_readme=args.include_readme,
        include_docstrings=args.include_docstrings,
        add_line_numbers=args.add_line_numbers,
        output_format=args.format,
    )

    if not success:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
