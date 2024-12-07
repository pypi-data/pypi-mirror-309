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
    parser.add_argument('--preview', '-p', action='store_true', help='Preview files to be created without making changes')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite of existing files')
    parser.add_argument(
        '--version',
        action='version',
        version=f'markdown2code {__version__}'
    )

    args = parser.parse_args()
    
    try:
        converter = MarkdownConverter(args.markdown_file, args.output)
        
        if args.preview:
            preview_info = converter.preview()
            
            print("\nPreview of files to be created:")
            print("\nDirectories:")
            for dir_info in preview_info['directories']:
                status = "exists" if dir_info['exists'] else "will be created"
                print(f"- {dir_info['path']} ({status})")
            
            print("\nFiles:")
            for file_info in preview_info['files']:
                status = "exists" if file_info['exists'] else "will be created"
                print(f"- {file_info['path']} ({status})")
            
            if preview_info['conflicts']:
                print("\nWarning: The following files already exist:")
                for conflict in preview_info['conflicts']:
                    print(f"- {conflict}")
                print("\nUse --force to overwrite existing files")
            return 0
        
        converter.convert(force=args.force)
        return 0
        
    except FileExistsError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
