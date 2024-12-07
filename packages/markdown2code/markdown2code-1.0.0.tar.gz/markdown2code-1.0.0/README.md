# markdown2code
```bash
                       _       _                     ___               _      
                      | |     | |                   |__ \             | |     
  _ __ ___   __ _ _ __| | ____| | _____      ___ __    ) |___ ___   __| | ___ 
 | '_ ` _ \ / _` | '__| |/ / _` |/ _ \ \ /\ / / '_ \  / // __/ _ \ / _` |/ _ \
 | | | | | | (_| | |  |   < (_| | (_) \ V  V /| | | |/ /| (_| (_) | (_| |  __/
 |_| |_| |_|\__,_|_|  |_|\_\__,_|\___/ \_/\_/ |_| |_|____\___\___/ \__,_|\___|
```    

Convert markdown files into organized project structures with code files. 
This tool is particularly useful for converting code snippets from AI chat conversations (like ChatGPT, Claude, etc.) into actual project files.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Use Cases](#use-cases)
  - [AI Chat Development](#ai-chat-development-sessions)
  - [Documentation to Implementation](#documentation-to-implementation)
  - [Tutorial Creation](#tutorial-creation)
  - [Project Templates](#project-templates)
- [Configuration](#configuration)
  - [Default Configuration](#default-configuration)
  - [Custom Configuration](#custom-configuration)
  - [File Patterns](#file-patterns)
- [Command Line Options](#command-line-options)
- [Markdown Format](#markdown-format)
  - [Code Blocks](#code-blocks)
  - [File Names](#file-names)
  - [Directory Structure](#directory-structure)
- [Examples](#examples)
  - [React Todo App](#react-todo-app-example)
  - [Python Script](#python-script-from-chat)
  - [Configuration Files](#configuration-files-from-chat)
- [Development](#development)
  - [Setup](#development-setup)
  - [Testing](#running-tests)
  - [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Extracts code blocks from markdown files
- Automatically detects programming languages
- Creates directory structures based on markdown content
- Supports filename detection from comments
- Handles multiple programming languages
- Maintains file permissions (executable for shell scripts)
- Preview mode to check files before creation
- File conflict detection and handling
- Configuration system with YAML support
- Verbose logging options

## Installation

```bash
pip install markdown2code
```

## Quick Start

Basic usage:
```bash
# Convert markdown to code
markdown2code input.md

# Preview files to be created
markdown2code input.md --preview

# Specify output directory
markdown2code input.md --output ./my-project

# Force overwrite existing files
markdown2code input.md --force

# Enable verbose logging
markdown2code input.md --verbose

# Use custom configuration
markdown2code input.md --config my-config.yml

# Create default configuration
markdown2code --create-config
```

## Configuration

### Default Configuration

Create a default configuration file:
```bash
markdown2code --create-config
```

This creates `.markdown2code.yml` with default settings:
```yaml
file_patterns:
  javascript: ['script.js', 'index.js', 'main.js']
  python: ['script.py', 'main.py', 'app.py']
  # ... more patterns

logging:
  level: INFO
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

output:
  colored: false
  verbose: false
```

### Custom Configuration

Create a custom configuration file:
```yaml
# .markdown2code.yml
file_patterns:
  python:
    - main.py
    - app.py
    - script.py
  javascript:
    - index.js
    - app.js
    - client.js

logging:
  level: DEBUG
  format: '%(levelname)s: %(message)s'

output:
  colored: true
  verbose: true
```

### File Patterns

Default file patterns for common languages:
- JavaScript: script.js, index.js, main.js
- Python: script.py, main.py, app.py
- HTML: index.html, main.html, app.html
- CSS: styles.css, main.css, app.css
- And many more...

## Command Line Options

```
markdown2code [options] input.md

Options:
  --output, -o DIR    Output directory (default: current)
  --preview, -p       Preview files without creating
  --force, -f         Force overwrite existing files
  --verbose, -v       Enable verbose output
  --config, -c FILE   Use custom configuration file
  --create-config     Create default configuration file
  --version          Show version number
  --help             Show this help message
```

## Use Cases

[Previous use cases and examples content remains the same...]

## Development

### Development Setup

1. Clone and setup:
```bash
git clone https://github.com/plain-mark/markdown2code.git
cd markdown2code
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

2. Run tests:
```bash
pytest
pytest --cov=markdown2code
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## Troubleshooting

### Common Issues

1. File Conflicts
```bash
# Use preview to check conflicts
markdown2code input.md --preview

# Force overwrite if needed
markdown2code input.md --force
```

2. Configuration Issues
```bash
# Create fresh configuration
markdown2code --create-config

# Use verbose logging
markdown2code input.md --verbose
```

3. Permission Issues
```bash
# Check file permissions
ls -l output_dir

# Fix shell script permissions
chmod +x output_dir/*.sh
```

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.



## AI Chat Example

Here's an example of converting an AI chat into a working project:

1. Save this AI chat conversation as `chat.md`:

````markdown
# React Todo App Development Chat

Project structure suggested by AI:
```markdown
todo-app/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── TodoList.js
│   │   └── TodoItem.js
│   ├── App.js
│   └── index.js
└── package.json
```

The AI suggested this HTML:
```html
# public/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
```
...
````
[chat.md](chat.md)

2. Convert the chat to a project:

3. Preview what will be created
```bash
markdown2code chat.md --preview --output todo-app
```
Output:
```bash
Preview of files to be created:

Directories:
- todo-app/todo-app (will be created)
- todo-app/public (will be created)
- todo-app/src (will be created)
- todo-app/components (will be created)

Files:
- todo-app/README.md (will be created)
- todo-app/public/index.html (will be created)
- todo-app/src/App.js (will be created)
- todo-app/src/components/TodoList.js (will be created)
- todo-app/src/components/TodoItem.js (will be created)
- todo-app/src/index.js (will be created)
- todo-app/package.json (will be created)
```

# Create the project
```bash
markdown2code chat.md --output todo-app
```
```
2024-11-20 16:10:55,512 - markdown2code.converter - INFO - 
Files to be created:
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - Directory: todo-app/todo-app (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - Directory: todo-app/public (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - Directory: todo-app/src (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - Directory: todo-app/components (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - File: todo-app/README.md (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - File: todo-app/public/index.html (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - File: todo-app/src/App.js (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - File: todo-app/src/components/TodoList.js (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - File: todo-app/src/components/TodoItem.js (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - File: todo-app/src/index.js (will be created)
2024-11-20 16:10:55,513 - markdown2code.converter - INFO - File: todo-app/package.json (will be created)
2024-11-20 16:10:55,514 - markdown2code.converter - INFO - Creating file: todo-app/README.md
2024-11-20 16:10:55,514 - markdown2code.converter - INFO - Creating file: todo-app/public/index.html
2024-11-20 16:10:55,515 - markdown2code.converter - INFO - Creating file: todo-app/src/App.js
2024-11-20 16:10:55,515 - markdown2code.converter - INFO - Creating file: todo-app/src/components/TodoList.js
2024-11-20 16:10:55,515 - markdown2code.converter - INFO - Creating file: todo-app/src/components/TodoItem.js
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - Creating file: todo-app/src/index.js
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - Creating file: todo-app/package.json
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - 
Created files:
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - - README.md
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - - package.json
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - - public/index.html
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - - src/App.js
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - - src/components/TodoItem.js
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - - src/components/TodoList.js
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - - src/index.js
2024-11-20 16:10:55,516 - markdown2code.converter - INFO - 
Project structure created successfully!
```


3. Run the project:
```bash
cd todo-app
npm install
npm start
```