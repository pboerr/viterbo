"""
Core functionality for collecting and documenting Python code.
"""

import os
import sys
import ast
from pathlib import Path
from datetime import datetime


def extract_docstrings(file_path):
    """Extract docstrings from a Python file using the ast module"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source = file.read()

        parsed = ast.parse(source)
        docstrings = {}

        # Module docstring
        if (
            len(parsed.body) > 0
            and isinstance(parsed.body[0], ast.Expr)
            and isinstance(parsed.body[0].value, ast.Str)
        ):
            docstrings["module"] = parsed.body[0].value.s.strip()

        # Function and class docstrings
        for node in ast.walk(parsed):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node)
                if doc:
                    docstrings[node.name] = doc.strip()

        return docstrings
    except Exception as e:
        print(f"Error extracting docstrings from {file_path}: {e}", file=sys.stderr)
        return {}


def document_python_files(
    source_dir, output_file, include_docstrings=False, add_line_numbers=False
):
    """Process Python files and generate documentation"""
    try:
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

        # Create or clear the output file
        try:
            with open(output_file, "w", encoding="utf-8") as out:
                # Write header
                out.write(f"# Python Code Documentation\n")
                out.write(
                    f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                out.write(f"# Source: {source_path}\n\n")

                # Find all Python files - using try/except to catch permission errors
                python_files = []
                try:
                    python_files = sorted(source_path.glob("**/*.py"))
                except PermissionError:
                    print(
                        f"Error: Permission denied when reading files in '{source_dir}'",
                        file=sys.stderr,
                    )
                    print(
                        "Please check directory and file permissions", file=sys.stderr
                    )
                    return False

                file_count = 0

                for file_path in python_files:
                    try:
                        file_count += 1
                        rel_path = file_path.relative_to(source_path)

                        out.write(f"\n\n{'=' * 80}\n")
                        out.write(f"FILE: {rel_path}\n")
                        out.write(f"{'=' * 80}\n\n")

                        # Extract docstrings if requested
                        docstrings = {}
                        if include_docstrings:
                            docstrings = extract_docstrings(file_path)

                            # Write module docstring if present
                            if "module" in docstrings:
                                out.write("MODULE DOCSTRING:\n")
                                out.write(f"{docstrings['module']}\n\n")

                        # Write file content with optional line numbers
                        out.write("CODE:\n")
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                if add_line_numbers:
                                    for i, line in enumerate(f, 1):
                                        out.write(f"{i:4d} | {line}")
                                else:
                                    out.write(f.read())
                        except PermissionError:
                            out.write(
                                f"Error: Permission denied when reading file {file_path}\n"
                            )
                        except Exception as e:
                            out.write(f"Error reading file: {e}\n")

                        # Write extracted docstrings
                        if (
                            include_docstrings and len(docstrings) > 1
                        ):  # > 1 because we already handled module docstring
                            out.write("\nDOCSTRINGS:\n")
                            for name, doc in docstrings.items():
                                if (
                                    name != "module"
                                ):  # Skip module docstring as it's already written
                                    out.write(f"\n{name}:\n")
                                    out.write(f"{'-' * len(name)}\n")
                                    out.write(f"{doc}\n")
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
                out.write(f"\n\n{'=' * 80}\n")
                out.write(
                    f"SUMMARY: Documented {file_count} Python files from {source_path}\n"
                )

            print(
                f"Documentation complete! {file_count} files documented in '{output_file}'"
            )
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
