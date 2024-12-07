"""
Command-line interface for markdown2code
"""
import argparse
import sys
import logging
from . import __version__
from .converter import MarkdownConverter
from .config import Config

def setup_logging(config):
    """Setup logging based on configuration and CLI options."""
    log_config = config.get_logging_config()
    logging.basicConfig(
        level=getattr(logging, log_config['level'].upper()),
        format=log_config['format']
    )
    return logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Generate project structure from Markdown file.')
    parser.add_argument('markdown_file', help='Path to Markdown file')
    parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')
    parser.add_argument('--preview', '-p', action='store_true', help='Preview files to be created without making changes')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite of existing files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--config', '-c', help='Path to custom configuration file')
    parser.add_argument('--create-config', action='store_true', help='Create default configuration file')
    parser.add_argument(
        '--version',
        action='version',
        version=f'markdown2code {__version__}'
    )

    args = parser.parse_args()

    try:
        # Handle configuration
        config = Config()
        if args.create_config:
            path = config.create_default_config()
            print(f"Created default configuration file at: {path}")
            return 0

        if args.config:
            config.load_user_config()

        # Update logging level if verbose flag is set
        if args.verbose:
            config.config['logging']['level'] = 'DEBUG'

        logger = setup_logging(config)
        
        converter = MarkdownConverter(args.markdown_file, args.output, config)
        
        if args.preview:
            preview_info = converter.preview()
            
            logger.info("\nPreview of files to be created:")
            logger.info("\nDirectories:")
            for dir_info in preview_info['directories']:
                status = "exists" if dir_info['exists'] else "will be created"
                logger.info(f"- {dir_info['path']} ({status})")
            
            logger.info("\nFiles:")
            for file_info in preview_info['files']:
                status = "exists" if file_info['exists'] else "will be created"
                logger.info(f"- {file_info['path']} ({status})")
            
            if preview_info['conflicts']:
                logger.warning("\nWarning: The following files already exist:")
                for conflict in preview_info['conflicts']:
                    logger.warning(f"- {conflict}")
                logger.info("\nUse --force to overwrite existing files")
            return 0
        
        converter.convert(force=args.force)
        return 0
        
    except FileExistsError as e:
        logger.error(f"Error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if args.verbose:
            logger.exception("Detailed error information:")
        return 1

if __name__ == '__main__':
    sys.exit(main())
