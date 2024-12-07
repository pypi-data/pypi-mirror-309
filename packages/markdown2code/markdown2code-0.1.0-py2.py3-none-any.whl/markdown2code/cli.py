"""
Command-line interface for markdown2code
"""
import argparse
import sys
from . import __version__
from .converter import MarkdownConverter

def main():
    parser = argparse.ArgumentParser(description='Generate project structure from Markdown file.')
    parser.add_argument('markdown_file', help='Path to Markdown file')
    parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')
    parser.add_argument(
        '--version',
        action='version',
        version=f'markdown2code {__version__}'
    )

    args = parser.parse_args()
    
    try:
        converter = MarkdownConverter(args.markdown_file, args.output)
        converter.convert()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
