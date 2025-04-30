import os
import tempfile
from pathlib import Path
from viterbo.collector import extract_docstrings, document_python_files


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


def test_document_python_files():
    """Test document generation"""
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
        result = document_python_files(temp_dir, output_file, True, True)
        assert result is True
        assert output_file.exists()

        # Check content
        content = output_file.read_text()
        assert "FILE: test_file.py" in content
        assert "MODULE DOCSTRING:" in content
        assert "Test module." in content
        assert "hello:" in content
        assert "Say hello." in content
