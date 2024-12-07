"""
Tests for the command-line interface
"""
import os
import sys
import pytest
import logging
from pathlib import Path
from io import StringIO
from markdown2code.cli import main

@pytest.fixture
def sample_markdown_file(tmp_path):
    content = '''# Test Project

Project structure:
```markdown
test-project/
├── src/
│   └── main.py
└── README.md
```

Main Python script:
```python
# filename: src/main.py
def main():
    print("Hello, World!")

if __name__ == '__main__':
    main()
```

README file:
```markdown
# filename: README.md
# Test Project
A test project
```
'''
    md_file = tmp_path / "test.md"
    md_file.write_text(content)
    return str(md_file)

@pytest.fixture(autouse=True)
def setup_logging():
    # Configure logging to use StringIO for testing
    log_stream = StringIO()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    root.handlers = [handler]  # Remove any existing handlers
    yield log_stream
    root.handlers = []  # Clean up

def test_main_basic(sample_markdown_file, tmp_path, monkeypatch, capsys, setup_logging):
    # Simulate command line arguments
    output_dir = tmp_path / "output"
    monkeypatch.setattr("sys.argv", ["markdown2code", "convert", sample_markdown_file, "--output", str(output_dir)])
    
    # Run CLI
    assert main() == 0
    
    # Check if files were created
    assert (output_dir / "src" / "main.py").exists()
    assert (output_dir / "README.md").exists()
    
    # Check output messages
    log_output = setup_logging.getvalue()
    assert "Created files:" in log_output

def test_main_preview(sample_markdown_file, tmp_path, monkeypatch, capsys, setup_logging):
    # Simulate preview command
    output_dir = tmp_path / "output"
    monkeypatch.setattr("sys.argv", ["markdown2code", "convert", sample_markdown_file, "--output", str(output_dir), "--preview"])
    
    # Run CLI in preview mode
    assert main() == 0
    
    # Check preview output
    log_output = setup_logging.getvalue()
    assert "Preview of files to be created:" in log_output
    assert "main.py" in log_output
    assert "README.md" in log_output
    
    # Verify no files were actually created
    assert not (output_dir / "src" / "main.py").exists()
    assert not (output_dir / "README.md").exists()

def test_main_file_conflict(sample_markdown_file, tmp_path, monkeypatch, capsys, setup_logging):
    output_dir = tmp_path / "output"
    
    # Create conflicting file
    os.makedirs(output_dir / "src")
    (output_dir / "src" / "main.py").write_text("existing content")
    
    # Try without force flag
    monkeypatch.setattr("sys.argv", ["markdown2code", "convert", sample_markdown_file, "--output", str(output_dir)])
    assert main() == 1  # Should fail
    
    # Check output messages
    log_output = setup_logging.getvalue()
    assert "Warning: The following files already exist:" in log_output
    
    # Try with force flag
    monkeypatch.setattr("sys.argv", ["markdown2code", "convert", sample_markdown_file, "--output", str(output_dir), "--force"])
    assert main() == 0  # Should succeed
    
    # Check if file was overwritten
    with open(output_dir / "src" / "main.py") as f:
        content = f.read()
        assert "def main():" in content

def test_main_invalid_input(tmp_path, monkeypatch, capsys, setup_logging):
    # Test with non-existent input file
    monkeypatch.setattr("sys.argv", ["markdown2code", "convert", "nonexistent.md"])
    assert main() == 1
    
    # Check output messages
    log_output = setup_logging.getvalue()
    assert "Error" in log_output

def test_main_version(monkeypatch, capsys):
    from markdown2code import __version__
    
    # Test --version flag
    monkeypatch.setattr("sys.argv", ["markdown2code", "--version"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out

def test_main_help(monkeypatch, capsys):
    # Test --help flag
    monkeypatch.setattr("sys.argv", ["markdown2code", "--help"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "convert" in captured.out
    assert "backup" in captured.out

def test_backup_commands(tmp_path, monkeypatch, capsys, setup_logging):
    # Initialize git repo
    os.chdir(tmp_path)
    os.system("git init")
    os.system('git config --global user.email "test@example.com"')
    os.system('git config --global user.name "Test User"')
    
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    # Test backup create
    monkeypatch.setattr("sys.argv", ["markdown2code", "backup", "create", "--directory", str(tmp_path)])
    assert main() == 0
    
    # Test backup list
    monkeypatch.setattr("sys.argv", ["markdown2code", "backup", "list", "--directory", str(tmp_path)])
    assert main() == 0
    
    # Check output messages
    log_output = setup_logging.getvalue()
    assert "Available backups:" in log_output
