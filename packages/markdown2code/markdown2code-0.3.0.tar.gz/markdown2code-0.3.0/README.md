# markdown2code

Convert markdown files into organized project structures with code files. This tool extracts code blocks from markdown files and creates a proper directory structure with the corresponding source files.

## Features

- Extracts code blocks from markdown files
- Automatically detects programming languages
- Creates directory structures based on markdown content
- Supports filename detection from comments
- Handles multiple programming languages
- Maintains file permissions (executable for shell scripts)
- Preview mode to check files before creation
- File conflict detection and handling

## Installation

```bash
pip install markdown2code
```

## Usage

Basic usage:
```bash
markdown2code input.md
```

Preview files to be created:
```bash
markdown2code input.md --preview
```

Specify output directory:
```bash
markdown2code input.md --output ./my-project
```

Force overwrite existing files:
```bash
markdown2code input.md --force
```

## File Conflict Handling

By default, markdown2code will not overwrite existing files. When a file conflict is detected:

1. In normal mode:
   - Shows which files would be overwritten
   - Stops execution without making changes
   - Suggests using --force or a different output directory

2. With --preview:
   - Shows all files and directories that would be created
   - Indicates which files already exist
   - No changes are made to the filesystem

3. With --force:
   - Proceeds with file creation
   - Overwrites any existing files
   - Creates new directories as needed

## Markdown Format

### Code Blocks

Code blocks should be marked with triple backticks and the language identifier:

````markdown
```python
def hello():
    print("Hello, World!")
```
````

### File Names

File names can be specified in three ways:

1. In the code block header:
````markdown
```python
# main.py
def hello():
    print("Hello, World!")
```
````

2. In comments within the code:
````markdown
```python
# filename: main.py
def hello():
    print("Hello, World!")
```
````

3. Automatically assigned based on language (if no name is specified):
- Python -> script.py
- JavaScript -> script.js
- HTML -> index.html
- etc.

### Directory Structure

Project structure can be defined using a markdown code block:

````markdown
```markdown
my-project/
├── src/
│   ├── main.py
│   └── utils/
│       └── helpers.py
├── tests/
│   └── test_main.py
└── README.md
```
````

## Default File Names

When no filename is specified, the following defaults are used:

- JavaScript: script.js
- Python: script.py
- CSS: styles.css
- HTML: index.html
- Java: Main.java
- C++: main.cpp
- C: main.c
- SQL: query.sql
- PHP: index.php
- Ruby: script.rb
- Go: main.go
- Rust: main.rs
- TypeScript: script.ts
- YAML: config.yml
- JSON: config.json
- XML: config.xml
- Markdown: README.md
- Shell: script.sh
- Dockerfile: Dockerfile

## Example

Input markdown file (`project.md`):
````markdown
# My Project

Project structure:
```markdown
my-project/
├── src/
│   └── main.py
└── README.md
```

Main Python script:
```python
# src/main.py
def main():
    print("Hello from my project!")

if __name__ == '__main__':
    main()
```

Project README:
```markdown
# My Project
A simple example project.
```
````

Preview what will be created:
```bash
markdown2code project.md --preview --output my-project
```

Create the project structure:
```bash
markdown2code project.md --output my-project
```

This will create:
```
my-project/
├── src/
│   └── main.py
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.
