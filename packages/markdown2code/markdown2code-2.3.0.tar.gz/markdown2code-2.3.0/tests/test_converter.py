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
    content = "// filename: script.js\nconsole.log('test');"
    assert converter.extract_filename_from_comments(content) == "script.js"
    
    # Test C-style comments
    content = "/* filename: main.cpp */\nint main() {}"
    assert converter.extract_filename_from_comments(content) == "main.cpp"
    
    # Test HTML comments
    content = "<!-- filename: index.html -->\n<html></html>"
    assert converter.extract_filename_from_comments(content) == "index.html"

def test_extract_file_content(sample_markdown):
    converter = MarkdownConverter("dummy.md")
    files = converter.extract_file_content(sample_markdown)
    
    assert "src/main.py" in files
    assert "README.md" in files
    
    assert "def main():" in files["src/main.py"]
    assert "# Test Project" in files["README.md"]
    assert "A test project" in files["README.md"]

def test_extract_file_content_with_header_paths():
    markdown_content = '''
```html
# public/index.html
<!DOCTYPE html>
<html></html>
```

```javascript
# src/App.js
function App() {
    return <div>Hello</div>;
}
```

```css
# ./src/styles/main.css
body { margin: 0; }
```
'''
    converter = MarkdownConverter("dummy.md")
    files = converter.extract_file_content(markdown_content)
    
    assert "public/index.html" in files
    assert "src/App.js" in files
    assert "src/styles/main.css" in files
    
    assert "<html></html>" in files["public/index.html"]
    assert "function App()" in files["src/App.js"]
    assert "body { margin: 0; }" in files["src/styles/main.css"]

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
    assert "test-project/src/" in paths
    assert "test-project/src/main.py" in paths
    assert "test-project/README.md" in paths

def test_preview(temp_dir, sample_markdown):
    # Create a temporary markdown file
    md_file = Path(temp_dir) / "test.md"
    md_file.write_text(sample_markdown)
    
    converter = MarkdownConverter(str(md_file), temp_dir)
    preview_info = converter.preview()
    
    # Check directories
    src_dir = str(Path(temp_dir) / "src")
    assert any(d['path'] == src_dir for d in preview_info['directories'])
    
    # Check files
    expected_files = {
        str(Path(temp_dir) / "src/main.py"),
        str(Path(temp_dir) / "README.md")
    }
    actual_files = {f['path'] for f in preview_info['files']}
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
        assert "A test project" in content

def test_convert_with_nested_directories(temp_dir):
    markdown_content = '''
```html
# public/index.html
<!DOCTYPE html>
<html></html>
```

```javascript
# src/components/App.js
function App() {
    return <div>Hello</div>;
}
```

```css
# src/styles/main.css
body { margin: 0; }
```
'''
    md_file = Path(temp_dir) / "test.md"
    md_file.write_text(markdown_content)
    
    converter = MarkdownConverter(str(md_file), temp_dir)
    created_files = converter.convert()
    
    # Check if files were created in correct directories
    assert "public/index.html" in created_files
    assert "src/components/App.js" in created_files
    assert "src/styles/main.css" in created_files
    
    # Verify directories were created
    assert os.path.exists(os.path.join(temp_dir, "public"))
    assert os.path.exists(os.path.join(temp_dir, "src/components"))
    assert os.path.exists(os.path.join(temp_dir, "src/styles"))
    
    # Check file contents
    with open(os.path.join(temp_dir, "public/index.html")) as f:
        content = f.read()
        assert "<html></html>" in content
    
    with open(os.path.join(temp_dir, "src/components/App.js")) as f:
        content = f.read()
        assert "function App()" in content
    
    with open(os.path.join(temp_dir, "src/styles/main.css")) as f:
        content = f.read()
        assert "body { margin: 0; }" in content

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
    assert any(str(Path(temp_dir) / "src/main.py") == p for p in preview_info['conflicts'])
    
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
# filename: script.sh
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
