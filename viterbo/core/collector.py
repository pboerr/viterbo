"""
Core functionality for collecting and documenting code files.
"""

import sys
from pathlib import Path
from collections import defaultdict

from .docstring import extract_docstrings
from .formatter import get_formatter
from .utils import (
    generate_directory_structure,
    get_language_from_extension,
    is_binary_file,
)


def document_files(
    source_dir,
    output_file,
    file_extensions=None,
    include_readme=False,
    include_docstrings=False,
    add_line_numbers=False,
    output_format="txt",
):
    """
    Process code files and generate documentation

    Args:
        source_dir: Directory containing source files
        output_file: Output file to write documentation
        file_extensions: List of file extensions to include (default: ['.py'])
        include_readme: Whether to include README.md files
        include_docstrings: Whether to extract and include docstrings from code files
        add_line_numbers: Whether to add line numbers to code
        output_format: Output format, either 'txt' or 'md'

    Returns:
        Boolean indicating success
    """
    try:
        # Set default file extensions if not provided
        if file_extensions is None:
            file_extensions = [".py"]

        # Ensure all file extensions are strings with leading dots
        clean_extensions = []
        for ext in file_extensions:
            ext_str = str(ext)
            if not ext_str.startswith("."):
                ext_str = f".{ext_str}"
            clean_extensions.append(ext_str)

        file_extensions = clean_extensions

        # Convert to absolute path if it's a relative path
        source_path = Path(source_dir).resolve()

        # Verify the directory exists and is accessible
        if not source_path.exists():
            print(
                f"Error: Source directory '{source_dir}' does not exist",
                file=sys.stderr,
            )
            return False

        if not source_path.is_dir():
            print(f"Error: '{source_dir}' is not a directory", file=sys.stderr)
            return False

        # Test directory read permissions explicitly
        try:
            next(source_path.iterdir(), None)
        except PermissionError:
            print(
                f"Error: Permission denied when accessing directory '{source_dir}'",
                file=sys.stderr,
            )
            print(
                "Please check that you have read permissions for this directory",
                file=sys.stderr,
            )
            return False

        # Create formatter based on output format
        formatter = get_formatter(output_format, output_file, source_path)

        # Create or clear the output file
        try:
            with open(output_file, "w", encoding="utf-8") as out:
                # Write header
                formatter.write_header(out)

                # Generate and write directory structure
                dir_structure = generate_directory_structure(
                    source_path, file_extensions, include_readme
                )
                formatter.write_directory_structure(out, dir_structure)

                # Find all relevant files
                code_files = []
                readme_files = []

                for ext in file_extensions:
                    try:
                        ext_str = str(ext)
                        found_files = sorted(source_path.glob(f"**/*{ext_str}"))
                        code_files.extend(found_files)
                    except PermissionError:
                        print(
                            f"Error: Permission denied when reading {ext} files in '{source_dir}'",
                            file=sys.stderr,
                        )
                        print(
                            "Please check directory and file permissions",
                            file=sys.stderr,
                        )

                # Add README files if requested
                if include_readme:
                    try:
                        readme_files = sorted(source_path.glob("**/README.md"))
                    except PermissionError:
                        print(
                            f"Error: Permission denied when reading README.md files in '{source_dir}'",
                            file=sys.stderr,
                        )

                # Combine and sort all files by path
                all_files = sorted(code_files + readme_files)
                language_stats = defaultdict(int)

                for file_path in all_files:
                    try:
                        rel_path = file_path.relative_to(source_path)

                        # Skip binary files
                        if is_binary_file(file_path):
                            print(f"Skipping binary file: {rel_path}", file=sys.stderr)
                            continue

                        # Determine language based on file extension
                        file_ext = str(file_path.suffix)
                        language = get_language_from_extension(file_ext)
                        language_stats[language] += 1

                        # Write file header
                        formatter.write_file_header(out, rel_path)

                        # Extract docstrings if requested
                        docstrings = {}
                        if include_docstrings:
                            docstrings = extract_docstrings(file_path)

                            # Write module docstring if present
                            if "module" in docstrings:
                                formatter.write_module_docstring(
                                    out, docstrings["module"]
                                )
                            elif "file" in docstrings:
                                formatter.write_module_docstring(
                                    out, docstrings["file"]
                                )

                        # Write file content with optional line numbers
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                if output_format.lower() == "md":
                                    formatter.write_code(
                                        out, content, add_line_numbers, language
                                    )
                                else:
                                    formatter.write_code(out, content, add_line_numbers)

                        except UnicodeDecodeError:
                            # Try with a different encoding
                            try:
                                with open(file_path, "r", encoding="latin-1") as f:
                                    content = f.read()
                                    if output_format.lower() == "md":
                                        formatter.write_code(
                                            out, content, add_line_numbers, language
                                        )
                                    else:
                                        formatter.write_code(
                                            out, content, add_line_numbers
                                        )
                            except Exception as e:
                                out.write(
                                    f"Error reading file with alternate encoding: {e}\n"
                                )
                        except PermissionError:
                            out.write(
                                f"Error: Permission denied when reading file {file_path}\n"
                            )
                        except Exception as e:
                            out.write(f"Error reading file: {e}\n")

                        # Write extracted docstrings
                        if include_docstrings and docstrings:
                            # Check if we have non-module docstrings
                            non_module_docstrings = {
                                k: v
                                for k, v in docstrings.items()
                                if k not in ["module", "file"]
                            }
                            if non_module_docstrings:
                                formatter.write_docstrings(out, docstrings)

                    except PermissionError:
                        print(
                            f"Skipping file {file_path} due to permission error",
                            file=sys.stderr,
                        )
                        continue
                    except Exception as e:
                        print(
                            f"Error processing file {file_path}: {e}", file=sys.stderr
                        )
                        continue

                # Write summary
                formatter.write_summary(out, language_stats)

            print(
                f"Documentation complete! {sum(language_stats.values())} files documented in '{output_file}'"
            )

            # Print language breakdown if multiple languages
            if len(language_stats) > 1:
                print("\nFiles by language:")
                for lang, count in sorted(
                    language_stats.items(), key=lambda x: x[1], reverse=True
                ):
                    print(f"- {lang}: {count}")

            return True

        except PermissionError:
            print(
                f"Error: Permission denied when writing to output file '{output_file}'",
                file=sys.stderr,
            )
            return False

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False


def document_python_files(
    source_dir, output_file, include_docstrings=False, add_line_numbers=False
):
    """
    Legacy wrapper for document_files that only processes Python files.

    Args:
        source_dir: Directory containing Python files
        output_file: Output file to write documentation
        include_docstrings: Whether to extract and include docstrings
        add_line_numbers: Whether to add line numbers to code

    Returns:
        Boolean indicating success
    """
    return document_files(
        source_dir=source_dir,
        output_file=output_file,
        file_extensions=[".py"],
        include_readme=False,
        include_docstrings=include_docstrings,
        add_line_numbers=add_line_numbers,
        output_format="txt",
    )
