# markdown2code

Convert markdown files into organized project structures with code files. This tool is particularly useful for converting code snippets from AI chat conversations (like ChatGPT, Claude, etc.) into actual project files.

## Use Cases

### 1. AI Chat Development Sessions
- Save entire development sessions from AI chats as markdown
- Convert code snippets and project structures into actual files
- Maintain context and documentation alongside code
- Easily implement AI-suggested project structures

### 2. Documentation to Implementation
- Convert technical documentation into working code
- Transform architecture documents into project scaffolding
- Create boilerplate from markdown specifications

### 3. Tutorial Creation
- Convert markdown tutorials into ready-to-use projects
- Create example code from educational content
- Generate starter templates for workshops

### 4. Project Templates
- Maintain project templates in readable markdown
- Generate consistent project structures
- Share project setups in human-readable format

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
```bash
# Preview what will be created
markdown2code chat.md --preview --output todo-app

# Create the project
markdown2code chat.md --output todo-app
```

3. Run the project:
```bash
cd todo-app
npm install
npm start
```

## More AI Chat Examples

### Python Script from Chat
````markdown
The AI suggested this script:
```python
# data_processor.py
import pandas as pd

def process_data(input_file):
    df = pd.read_csv(input_file)
    processed = df.dropna().describe()
    return processed

if __name__ == '__main__':
    result = process_data('data.csv')
    print(result)
```
````

Convert it:
```bash
markdown2code script.md
```

### Configuration Files from Chat
````markdown
The AI recommended these configs:
```yaml
# config.yml
server:
  port: 8080
  host: localhost
```

```json
# settings.json
{
  "debug": true,
  "logLevel": "info"
}
```
````

Convert them:
```bash
markdown2code config.md
```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
