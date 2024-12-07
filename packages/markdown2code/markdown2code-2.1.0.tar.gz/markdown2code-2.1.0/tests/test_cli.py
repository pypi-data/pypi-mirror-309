"""
Tests for the command-line interface
"""
import os
import pytest
from pathlib import Path
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
# src/main.py
def main():
    print("Hello, World!")

if __name__ == '__main__':
    main()
```

README file:
```markdown
# Test Project
A test project
```
'''
    md_file = tmp_path / "test.md"
    md_file.write_text(content)
    return str(md_file)

def test_main_basic(sample_markdown_file, tmp_path, monkeypatch, capsys):
    # Simulate command line arguments
    output_dir = tmp_path / "output"
    monkeypatch.setattr("sys.argv", ["markdown2code", sample_markdown_file, "--output", str(output_dir)])
    
    # Run CLI
    assert main() == 0
    
    # Check if files were created
    assert (output_dir / "src" / "main.py").exists()
    assert (output_dir / "README.md").exists()
    
    # Check output messages
    captured = capsys.readouterr()
    assert "Project structure created successfully!" in captured.out

def test_main_preview(sample_markdown_file, tmp_path, monkeypatch, capsys):
    # Simulate preview command
    output_dir = tmp_path / "output"
    monkeypatch.setattr("sys.argv", ["markdown2code", sample_markdown_file, "--output", str(output_dir), "--preview"])
    
    # Run CLI in preview mode
    assert main() == 0
    
    # Check preview output
    captured = capsys.readouterr()
    assert "Preview of files to be created:" in captured.out
    assert "main.py" in captured.out
    assert "README.md" in captured.out
    
    # Verify no files were actually created
    assert not (output_dir / "src" / "main.py").exists()
    assert not (output_dir / "README.md").exists()

def test_main_file_conflict(sample_markdown_file, tmp_path, monkeypatch, capsys):
    output_dir = tmp_path / "output"
    
    # Create conflicting file
    os.makedirs(output_dir / "src")
    (output_dir / "src" / "main.py").write_text("existing content")
    
    # Try without force flag
    monkeypatch.setattr("sys.argv", ["markdown2code", sample_markdown_file, "--output", str(output_dir)])
    assert main() == 1  # Should fail
    
    captured = capsys.readouterr()
    assert "Error" in captured.err
    
    # Try with force flag
    monkeypatch.setattr("sys.argv", ["markdown2code", sample_markdown_file, "--output", str(output_dir), "--force"])
    assert main() == 0  # Should succeed
    
    # Check if file was overwritten
    with open(output_dir / "src" / "main.py") as f:
        content = f.read()
        assert "def main():" in content

def test_main_invalid_input(tmp_path, monkeypatch, capsys):
    # Test with non-existent input file
    monkeypatch.setattr("sys.argv", ["markdown2code", "nonexistent.md"])
    assert main() == 1
    
    captured = capsys.readouterr()
    assert "Error" in captured.err

def test_main_version(monkeypatch, capsys):
    from markdown2code import __version__
    
    # Test --version flag
    with pytest.raises(SystemExit) as exc_info:
        monkeypatch.setattr("sys.argv", ["markdown2code", "--version"])
        main()
    
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out

def test_main_help(monkeypatch, capsys):
    # Test --help flag
    with pytest.raises(SystemExit) as exc_info:
        monkeypatch.setattr("sys.argv", ["markdown2code", "--help"])
        main()
    
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "--preview" in captured.out
    assert "--force" in captured.out
