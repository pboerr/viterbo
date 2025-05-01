"""
Tests for the Viterbo collector functionality.
"""

import os
import tempfile
from pathlib import Path

import pytest
from viterbo.core.collector import document_files
from viterbo.core.docstring import extract_docstrings


def test_extract_docstrings():
    """Test docstring extraction"""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(
            b'''"""Module docstring."""

def test_function():
    """Function docstring."""
    pass

class TestClass:
    """Class docstring."""
    pass
'''
        )

    try:
        docstrings = extract_docstrings(f.name)
        assert "module" in docstrings
        assert docstrings["module"] == "Module docstring."
        assert "test_function" in docstrings
        assert docstrings["test_function"] == "Function docstring."
        assert "TestClass" in docstrings
        assert docstrings["TestClass"] == "Class docstring."
    finally:
        os.unlink(f.name)


def test_document_files_python():
    """Test document generation for Python files"""
    # Create a temporary directory with Python files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file
        test_file = Path(temp_dir) / "test_file.py"
        with open(test_file, "w") as f:
            f.write(
                '''"""Test module."""

def hello():
    """Say hello."""
    print("Hello, world!")
'''
            )

        # Create output file
        output_file = Path(temp_dir) / "output.txt"

        # Test function
        result = document_files(
            source_dir=temp_dir,
            output_file=output_file,
            file_extensions=[".py"],
            include_docstrings=True,
            add_line_numbers=True,
        )
        assert result is True
        assert output_file.exists()

        # Check content
        content = output_file.read_text()
        assert "FILE: test_file.py" in content
        assert "MODULE DOCSTRING:" in content
        assert "Test module." in content
        assert "hello:" in content
        assert "Say hello." in content


def test_document_files_multiple_languages():
    """Test document generation for multiple file types"""
    # Create a temporary directory with multiple file types
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a Python file
        py_file = Path(temp_dir) / "test.py"
        with open(py_file, "w") as f:
            f.write('print("Hello from Python")\n')

        # Create a C++ file
        cpp_file = Path(temp_dir) / "test.cpp"
        with open(cpp_file, "w") as f:
            f.write(
                '#include <iostream>\n\nint main() {\n    std::cout << "Hello from C++" << std::endl;\n    return 0;\n}\n'
            )

        # Create an R file
        r_file = Path(temp_dir) / "test.R"
        with open(r_file, "w") as f:
            f.write('print("Hello from R")\n')

        # Create a README file
        readme_file = Path(temp_dir) / "README.md"
        with open(readme_file, "w") as f:
            f.write("# Test Project\n\nThis is a test project.\n")

        # Create output file
        output_file = Path(temp_dir) / "output.md"

        # Test function with multiple extensions and README
        result = document_files(
            source_dir=temp_dir,
            output_file=output_file,
            file_extensions=[".py", ".cpp", ".R"],
            include_readme=True,
            include_docstrings=False,
            add_line_numbers=False,
            output_format="md",
        )
        assert result is True
        assert output_file.exists()

        # Check content
        content = output_file.read_text()
        assert "## test.py" in content
        assert "## test.cpp" in content
        assert "## test.R" in content
        assert "## README.md" in content
        assert "Hello from Python" in content
        assert "Hello from C++" in content
        assert "Hello from R" in content
        assert "# Test Project" in content
        assert "Files by language" in content


def test_document_files_with_errors():
    """Test document generation with errors"""
    # Test with non-existent directory
    result = document_files(
        source_dir="/path/that/does/not/exist", output_file="output.txt"
    )
    assert result is False

    # Test with file instead of directory
    with tempfile.NamedTemporaryFile() as temp_file:
        result = document_files(source_dir=temp_file.name, output_file="output.txt")
        assert result is False
