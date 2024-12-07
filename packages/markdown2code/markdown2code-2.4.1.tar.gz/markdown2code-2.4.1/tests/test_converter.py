import os
import pytest
from pathlib import Path
from markdown2code.converter import MarkdownConverter

def test_extract_filename_from_direct_comments():
    """Test extracting filenames from direct comments."""
    converter = MarkdownConverter("test.md")
    
    # Test JavaScript-style comment
    content = "// manifest.json\nsome content"
    assert converter.extract_filename_from_comments(content) == "manifest.json"
    
    # Test Python-style comment
    content = "# config.py\nsome content"
    assert converter.extract_filename_from_comments(content) == "config.py"
    
    # Test C-style comment
    content = "/* styles.css */\nsome content"
    assert converter.extract_filename_from_comments(content) == "styles.css"
    
    # Test HTML-style comment
    content = "<!-- index.html -->\nsome content"
    assert converter.extract_filename_from_comments(content) == "index.html"

def test_extract_content_from_direct_comments(tmp_path):
    """Test extracting content from files marked with direct comments."""
    input_content = """// manifest.json
{
  "manifest_version": 2,
  "name": "Test Extension",
  "version": "1.0"
}

// content.js
const hello = 'world';
console.log(hello);
"""
    
    input_file = tmp_path / "test.md"
    input_file.write_text(input_content)
    
    converter = MarkdownConverter(str(input_file), str(tmp_path))
    files_content = converter.extract_file_content(input_content)
    
    assert "manifest.json" in files_content
    assert "content.js" in files_content
    
    # Verify manifest.json content
    manifest_content = files_content["manifest.json"]
    assert '"manifest_version": 2' in manifest_content
    assert '"name": "Test Extension"' in manifest_content
    
    # Verify content.js content
    content_js = files_content["content.js"]
    assert "const hello = 'world';" in content_js
    assert "console.log(hello);" in content_js

def test_convert_files_with_direct_comments(tmp_path):
    """Test full conversion of files marked with direct comments."""
    input_content = """// manifest.json
{
  "manifest_version": 2,
  "name": "Test Extension",
  "version": "1.0"
}

// content.js
const hello = 'world';
console.log(hello);
"""
    
    input_file = tmp_path / "test.md"
    input_file.write_text(input_content)
    
    output_dir = tmp_path / "output"
    converter = MarkdownConverter(str(input_file), str(output_dir))
    
    created_files = converter.convert()
    
    assert "manifest.json" in created_files
    assert "content.js" in created_files
    
    # Verify files were created
    assert (output_dir / "manifest.json").exists()
    assert (output_dir / "content.js").exists()
    
    # Verify manifest.json content
    manifest_content = (output_dir / "manifest.json").read_text()
    assert '"manifest_version": 2' in manifest_content
    assert '"name": "Test Extension"' in manifest_content
    
    # Verify content.js content
    content_js = (output_dir / "content.js").read_text()
    assert "const hello = 'world';" in content_js
    assert "console.log(hello);" in content_js
