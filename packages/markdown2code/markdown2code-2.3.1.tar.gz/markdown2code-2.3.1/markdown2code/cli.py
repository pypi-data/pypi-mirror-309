"""
Command-line interface for markdown2code
"""
import argparse
import sys
import logging
from . import __version__
from .converter import MarkdownConverter
from .config import Config
from .backup import GitBackup
from .web import run_server

def setup_logging(config):
    """Setup logging based on configuration and CLI options."""
    log_config = config.get_logging_config()
    logging.basicConfig(
        level=getattr(logging, log_config['level'].upper()),
        format=log_config['format']
    )
    return logging.getLogger(__name__)

def restore_last_backup(directory, logger):
    """Restore the most recent backup."""
    backup = GitBackup(directory)
    last_backup = backup.get_last_backup()
    
    if not last_backup:
        logger.error("No backups found")
        return 1
        
    try:
        files = backup.restore_backup(last_backup)
        logger.info(f"Restored {len(files)} files from last backup: {last_backup}")
        logger.info("\nRestored files:")
        for file in files:
            logger.info(f"- {file}")
        return 0
    except Exception as e:
        logger.error(f"Failed to restore backup: {str(e)}")
        return 1

def handle_backup_commands(args, logger):
    """Handle backup-related commands."""
    backup = GitBackup(args.directory)

    try:
        if args.backup_command == 'create':
            branch = backup.create_backup(
                files=args.files,
                message=args.message
            )
            logger.info(f"Created backup branch: {branch}")
            return 0

        elif args.backup_command == 'list':
            backups = backup.list_backups()
            if backups:
                logger.info("\nAvailable backups:")
                for b in backups:
                    info = backup.get_backup_info(b)
                    logger.info(f"- {b} ({info['date']}): {info['message']}")
            else:
                logger.info("No backups found")
            return 0

        elif args.backup_command == 'restore':
            if not args.name:
                logger.error("Backup name is required for restore")
                return 1
            files = backup.restore_backup(args.name)
            logger.info(f"Restored {len(files)} files from backup: {args.name}")
            return 0

        elif args.backup_command == 'delete':
            if not args.name:
                logger.error("Backup name is required for delete")
                return 1
            if backup.delete_backup(args.name):
                logger.info(f"Deleted backup: {args.name}")
                return 0
            return 1

        elif args.backup_command == 'info':
            if not args.name:
                logger.error("Backup name is required for info")
                return 1
            info = backup.get_backup_info(args.name)
            logger.info("\nBackup Information:")
            logger.info(f"Branch: {info['branch']}")
            logger.info(f"Date: {info['date']}")
            logger.info(f"Commit: {info['hash']}")
            logger.info(f"Message: {info['message']}")
            logger.info("\nFiles:")
            for file in info['files']:
                logger.info(f"- {file}")
            return 0

    except Exception as e:
        logger.error(f"Backup operation failed: {str(e)}")
        if args.verbose:
            logger.exception("Detailed error information:")
        return 1

def main():
    parser = argparse.ArgumentParser(description='Generate project structure from Markdown file.')
    parser.add_argument('--version', action='version', version=f'markdown2code {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert markdown to code files')
    convert_parser.add_argument('markdown_file', help='Path to Markdown file')
    convert_parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')
    convert_parser.add_argument('--preview', '-p', action='store_true', help='Preview files to be created without making changes')
    convert_parser.add_argument('--force', '-f', action='store_true', help='Force overwrite of existing files')
    convert_parser.add_argument('--backup', '-b', action='store_true', help='Create backup before making changes')
    convert_parser.add_argument('--restore', '-r', action='store_true', help='Restore from last backup')
    convert_parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    convert_parser.add_argument('--config', '-c', help='Path to custom configuration file')
    convert_parser.add_argument('--create-config', action='store_true', help='Create default configuration file')

    # Server command
    server_parser = subparsers.add_parser('server', help='Start web interface')
    server_parser.add_argument('--host', default='localhost', help='Host to bind to (default: localhost)')
    server_parser.add_argument('--port', type=int, default=5000, help='Port to listen on (default: 5000)')
    server_parser.add_argument('--output', '-o', default='uploads', help='Output directory for converted files (default: uploads)')

    # Backup commands
    backup_parser = subparsers.add_parser('backup', help='Backup operations')
    backup_subparsers = backup_parser.add_subparsers(dest='backup_command', help='Backup commands')

    # Create backup
    create_parser = backup_subparsers.add_parser('create', help='Create a new backup')
    create_parser.add_argument('--files', nargs='*', help='Specific files to backup')
    create_parser.add_argument('--message', '-m', help='Backup message')
    create_parser.add_argument('--directory', '-d', default='.', help='Working directory')

    # List backups
    list_parser = backup_subparsers.add_parser('list', help='List all backups')
    list_parser.add_argument('--directory', '-d', default='.', help='Working directory')

    # Restore backup
    restore_parser = backup_subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('name', help='Backup name to restore')
    restore_parser.add_argument('--directory', '-d', default='.', help='Working directory')

    # Delete backup
    delete_parser = backup_subparsers.add_parser('delete', help='Delete a backup')
    delete_parser.add_argument('name', help='Backup name to delete')
    delete_parser.add_argument('--directory', '-d', default='.', help='Working directory')

    # Backup info
    info_parser = backup_subparsers.add_parser('info', help='Show backup information')
    info_parser.add_argument('name', help='Backup name')
    info_parser.add_argument('--directory', '-d', default='.', help='Working directory')

    args = parser.parse_args()

    try:
        # Handle configuration
        config = Config()
        if hasattr(args, 'create_config') and args.create_config:
            path = config.create_default_config()
            print(f"Created default configuration file at: {path}")
            return 0

        if hasattr(args, 'config') and args.config:
            config.load_user_config()

        # Update logging level if verbose flag is set
        if hasattr(args, 'verbose') and args.verbose:
            config.config['logging']['level'] = 'DEBUG'

        logger = setup_logging(config)

        # Handle server command
        if args.command == 'server':
            logger.info(f"Starting web interface at http://{args.host}:{args.port}")
            logger.info(f"Output directory: {args.output}")
            run_server(host=args.host, port=args.port, output_dir=args.output)
            return 0

        # Handle backup commands
        elif args.command == 'backup':
            return handle_backup_commands(args, logger)

        # Handle convert command
        elif args.command == 'convert':
            # Handle restore flag first
            if args.restore:
                return restore_last_backup(args.output, logger)
            
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
            
            converter.convert(force=args.force, backup=args.backup)
            return 0
        
        else:
            parser.print_help()
            return 1
            
    except FileExistsError as e:
        logger.error(f"Error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if hasattr(args, 'verbose') and args.verbose:
            logger.exception("Detailed error information:")
        return 1

if __name__ == '__main__':
    sys.exit(main())
