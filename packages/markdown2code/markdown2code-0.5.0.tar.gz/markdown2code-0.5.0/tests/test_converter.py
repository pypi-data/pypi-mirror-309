"""
Tests for the MarkdownConverter class
"""
import os
import pytest
import tempfile
from pathlib import Path
from markdown2code.converter import MarkdownConverter

@pytest.fixture
def sample_markdown():
    return '''# Test Project

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

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_extract_filename_from_comments():
    converter = MarkdownConverter("dummy.md")
    
    # Test Python style comments
    content = "# filename: test.py\ndef main():\n    pass"
    assert converter.extract_filename_from_comments(content) == "test.py"
    
    # Test JavaScript style comments
    content = "// script.js\nconsole.log('test');"
    assert converter.extract_filename_from_comments(content) == "script.js"
    
    # Test C-style comments
    content = "/* main.cpp */\nint main() {}"
    assert converter.extract_filename_from_comments(content) == "main.cpp"
    
    # Test HTML comments
    content = "<!-- index.html -->\n<html></html>"
    assert converter.extract_filename_from_comments(content) == "index.html"

def test_extract_file_content(sample_markdown):
    converter = MarkdownConverter("dummy.md")
    files = converter.extract_file_content(sample_markdown)
    
    assert "src/main.py" in files
    assert "README.md" in files
    
    assert "def main():" in files["src/main.py"]
    assert "# Test Project" in files["README.md"]

def test_create_directory_structure():
    converter = MarkdownConverter("dummy.md")
    structure = '''
test-project/
├── src/
│   └── main.py
└── README.md
'''
    paths = converter.create_directory_structure(structure)
    assert "test-project/" in paths
    assert "src/" in paths

def test_preview(temp_dir, sample_markdown):
    # Create a temporary markdown file
    md_file = Path(temp_dir) / "test.md"
    md_file.write_text(sample_markdown)
    
    converter = MarkdownConverter(str(md_file), temp_dir)
    preview_info = converter.preview()
    
    # Check directories
    assert any(d['path'].endswith('src') for d in preview_info['directories'])
    
    # Check files
    expected_files = {
        "src/main.py",
        "README.md"
    }
    actual_files = {Path(f['path']).name for f in preview_info['files']}
    assert expected_files == actual_files
    
    # Check no conflicts initially
    assert len(preview_info['conflicts']) == 0

def test_convert(temp_dir, sample_markdown):
    # Create a temporary markdown file
    md_file = Path(temp_dir) / "test.md"
    md_file.write_text(sample_markdown)
    
    converter = MarkdownConverter(str(md_file), temp_dir)
    created_files = converter.convert()
    
    # Check if files were created
    assert "src/main.py" in created_files
    assert "README.md" in created_files
    
    # Check file contents
    with open(os.path.join(temp_dir, "src/main.py")) as f:
        content = f.read()
        assert "def main():" in content
    
    with open(os.path.join(temp_dir, "README.md")) as f:
        content = f.read()
        assert "# Test Project" in content

def test_file_conflict_handling(temp_dir, sample_markdown):
    # Create a temporary markdown file
    md_file = Path(temp_dir) / "test.md"
    md_file.write_text(sample_markdown)
    
    # Create a file that would conflict
    os.makedirs(os.path.join(temp_dir, "src"))
    with open(os.path.join(temp_dir, "src/main.py"), "w") as f:
        f.write("# Existing file")
    
    converter = MarkdownConverter(str(md_file), temp_dir)
    
    # Check preview shows conflict
    preview_info = converter.preview()
    assert any(p.endswith("main.py") for p in preview_info['conflicts'])
    
    # Check conversion raises error without force
    with pytest.raises(FileExistsError):
        converter.convert(force=False)
    
    # Check force option allows overwrite
    created_files = converter.convert(force=True)
    assert "src/main.py" in created_files
    
    # Verify content was overwritten
    with open(os.path.join(temp_dir, "src/main.py")) as f:
        content = f.read()
        assert "def main():" in content

def test_executable_permissions(temp_dir):
    markdown_content = '''
```bash
# script.sh
#!/bin/bash
echo "Hello"
```
'''
    md_file = Path(temp_dir) / "test.md"
    md_file.write_text(markdown_content)
    
    converter = MarkdownConverter(str(md_file), temp_dir)
    converter.convert()
    
    script_path = os.path.join(temp_dir, "script.sh")
    assert os.path.exists(script_path)
    assert os.access(script_path, os.X_OK)
