"""
Core functionality for converting markdown to code files
"""
import os
import re
import logging
from pathlib import Path
from .config import Config
from .backup import GitBackup

class MarkdownConverter:
    def __init__(self, input_file, output_dir='.', config=None):
        self.input_file = input_file
        self.output_dir = output_dir
        self.config = config or Config()
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging based on configuration."""
        log_config = self.config.get_logging_config()
        logging.basicConfig(
            level=getattr(logging, log_config['level'].upper()),
            format=log_config['format']
        )
        self.logger = logging.getLogger(__name__)

    def _create_backup(self):
        """Create a backup of the current state."""
        try:
            backup = GitBackup(self.output_dir)
            branch_name = backup.create_backup(
                message="Auto-backup before markdown2code conversion"
            )
            self.logger.info(f"Created backup in branch: {branch_name}")
            return branch_name
        except Exception as e:
            self.logger.error(f"Failed to create backup: {str(e)}")
            raise

    @staticmethod
    def extract_filename_from_comments(content):
        """Extract filename from various comment types."""
        patterns = [
            # Explicit filename patterns
            r'(?:^|\n)//\s*filename:\s*([^\n]*\.[\w]+)',  # JavaScript, C++
            r'(?:^|\n)#\s*filename:\s*([^\n]*\.[\w]+)',   # Python, Bash, Ruby
            r'/\*\s*filename:\s*(.*?\.[\w]+).*?\*/',       # C-style (/* */)
            r'<!--\s*filename:\s*(.*?\.[\w]+).*?-->',      # HTML/XML
            r'"""\s*filename:\s*(.*?\.[\w]+).*?"""',       # Python docstring
            r"'''\s*filename:\s*(.*?\.[\w]+).*?'''",       # Python docstring (single quotes)
            r'--\s*filename:\s*([^\n]*\.[\w]+)',          # SQL
            r'%\s*filename:\s*([^\n]*\.[\w]+)',           # LaTeX
            # Direct filename comment patterns
            r'(?:^|\n)//\s*([\w\-]+\.[a-zA-Z0-9]+)\s*$',  # // filename.ext
            r'(?:^|\n)#\s*([\w\-]+\.[a-zA-Z0-9]+)\s*$',   # # filename.ext
            r'/\*\s*([\w\-]+\.[a-zA-Z0-9]+)\s*\*/',       # /* filename.ext */
            r'<!--\s*([\w\-]+\.[a-zA-Z0-9]+)\s*-->',      # <!-- filename.ext -->
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1).strip()

        return None

    def extract_file_content(self, markdown_content):
        """Extract file content from markdown code blocks."""
        pattern = r'```(\w+)?\s*(?:#\s*(.*?)\n|\n)?(.*?)```'
        matches = re.finditer(pattern, markdown_content, re.DOTALL)

        files_content = {}
        file_counter = {}

        # First try to extract files from non-markdown content with filename comments
        content_parts = re.split(r'\n\s*(?://|#|/\*|\<\!--)\s*[\w\-]+\.[a-zA-Z0-9]+', markdown_content)
        if len(content_parts) > 1:  # If we found any filename comments
            # Reset to start of content to get the filenames too
            current_pos = 0
            current_file = None
            current_content = []
            
            for line in markdown_content.split('\n'):
                filename = self.extract_filename_from_comments(line)
                if filename:
                    if current_file:  # Save previous file content
                        files_content[current_file] = '\n'.join(current_content).strip()
                    current_file = filename
                    current_content = []
                elif current_file:  # Collect content for current file
                    if not line.strip().startswith('//') and not line.strip().startswith('#'):
                        current_content.append(line)
            
            # Save last file content
            if current_file:
                files_content[current_file] = '\n'.join(current_content).strip()

        # Then process markdown code blocks
        for match in matches:
            language = match.group(1)
            header = match.group(2)
            content = match.group(3).strip()

            # Skip markdown structure blocks
            if language == 'markdown' and any(s in content for s in ['├', '└', '│']):
                continue

            # First try to get filename from the header
            filename = None
            if header:
                # Remove "filename:" prefix if present
                if 'filename:' in header:
                    filename = header.split('filename:', 1)[1].strip()
                else:
                    filename = header.strip()

            # If no filename in header, try to get it from content comments
            if not filename:
                filename = self.extract_filename_from_comments(content)
                if filename:
                    # Remove "filename:" prefix if present in extracted filename
                    if filename.startswith('filename:'):
                        filename = filename.split('filename:', 1)[1].strip()

            # Use default patterns if no filename found
            if not filename and language:
                language = language.lower()
                patterns = self.config.get_file_patterns(language)
                if patterns:
                    base_name = patterns[0]  # Use first pattern as default
                    if base_name in file_counter:
                        file_counter[base_name] += 1
                        name, ext = os.path.splitext(base_name)
                        # Try other patterns if available
                        if len(patterns) > file_counter[base_name]:
                            filename = patterns[file_counter[base_name]]
                        else:
                            filename = f"{name}_{file_counter[base_name]}{ext}"
                    else:
                        file_counter[base_name] = 0
                        filename = base_name

            if filename:
                # Clean up the filename and normalize path separators
                clean_filename = filename.strip().replace('\\', '/').lstrip('./')
                self.logger.debug(f"Extracted file content for: {clean_filename}")
                files_content[clean_filename] = content

        return files_content

    @staticmethod
    def create_directory_structure(structure_text):
        """Create a list of paths from text directory structure."""
        paths = []
        current_path = []
        
        for line in structure_text.split('\n'):
            line = line.strip()
            if not line or '```' in line:
                continue

            # Count the depth by the number of │ or ├ or └ characters
            depth = len(re.findall(r'[│├└]', line))
            
            # Remove tree characters and spaces
            path = re.sub(r'^[│├└─\s]+', '', line)
            
            if path and not path.startswith('#'):
                # Adjust current path based on depth
                current_path = current_path[:depth]
                current_path.append(path)
                
                # Create full path
                full_path = '/'.join(p.rstrip('/') for p in current_path)
                if not ('.' in path):  # It's a directory
                    full_path += '/'
                paths.append(full_path)

        return paths

    @staticmethod
    def ensure_directory(file_path):
        """Create directories for the given file path."""
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def preview(self):
        """Preview what files will be generated without creating them."""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            output_path = Path(self.output_dir)
            preview_info = {
                'directories': [],
                'files': [],
                'conflicts': []
            }

            # Extract file content first to get actual files
            files_content = self.extract_file_content(content)
            
            # Get directories from file paths
            for filename in files_content.keys():
                dir_path = os.path.dirname(filename)
                if dir_path:
                    full_dir_path = output_path / dir_path
                    preview_info['directories'].append({
                        'path': str(full_dir_path),
                        'exists': full_dir_path.exists()
                    })

            # Check files
            for filename in files_content.keys():
                file_path = output_path / filename
                preview_info['files'].append({
                    'path': str(file_path),
                    'exists': file_path.exists()
                })
                if file_path.exists():
                    preview_info['conflicts'].append(str(file_path))

            return preview_info

        except Exception as e:
            self.logger.error(f"Preview failed: {str(e)}")
            raise

    def convert(self, force=False, backup=False):
        """Convert markdown file to code files."""
        backup_branch = None
        if backup:
            self.logger.info("Creating backup before proceeding...")
            backup_branch = self._create_backup()
            self.logger.info(f"Backup created successfully: {backup_branch}")

        preview_info = self.preview()
        
        if preview_info['conflicts'] and not force:
            self.logger.warning("\nWarning: The following files already exist:")
            for conflict in preview_info['conflicts']:
                self.logger.warning(f"- {conflict}")
            if backup_branch:
                self.logger.info(f"\nNote: These files have been backed up in branch: {backup_branch}")
            raise FileExistsError(
                "Some files already exist. Use --force to overwrite or choose a different output directory."
            )

        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()

            output_path = Path(self.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            files_content = self.extract_file_content(content)
            created_files = []

            for filename, file_content in files_content.items():
                file_path = output_path / filename
                self.ensure_directory(str(file_path))

                self.logger.info(f"Creating file: {file_path}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content + '\n')

                if filename.endswith('.sh'):
                    os.chmod(file_path, 0o755)

                created_files.append(filename)

            self.logger.info("\nCreated files:")
            for f in sorted(created_files):
                self.logger.info(f"- {f}")
            
            if backup_branch:
                self.logger.info(f"\nNote: Original state backed up in branch: {backup_branch}")
            self.logger.info("\nProject structure created successfully!")

            return created_files

        except Exception as e:
            self.logger.error(f"Conversion failed: {str(e)}")
            if backup_branch:
                self.logger.info(f"\nYou can restore the original state from backup: {backup_branch}")
            raise
