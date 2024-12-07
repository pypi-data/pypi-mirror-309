"""
Git-based backup and restore functionality for source code files
"""
import os
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

class GitBackup:
    def __init__(self, working_dir='.'):
        self.working_dir = working_dir
        self.logger = logging.getLogger(__name__)

    def _run_git_command(self, command, check=True):
        """Run a git command and return its output."""
        try:
            result = subprocess.run(
                command,
                cwd=self.working_dir,
                check=check,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git command failed: {e.stderr}")
            raise

    def is_git_repo(self):
        """Check if the working directory is a git repository."""
        try:
            self._run_git_command(['git', 'rev-parse', '--git-dir'])
            return True
        except subprocess.CalledProcessError:
            return False

    def init_repo(self):
        """Initialize a new git repository if one doesn't exist."""
        if not self.is_git_repo():
            self._run_git_command(['git', 'init'])
            # Create initial commit to allow branch creation
            try:
                self._run_git_command(['git', 'add', '.'])
                self._run_git_command(['git', 'commit', '-m', 'Initial commit'])
            except subprocess.CalledProcessError:
                # If nothing to commit, create empty commit
                self._run_git_command(['git', 'commit', '--allow-empty', '-m', 'Initial commit'])
            self.logger.info("Initialized new git repository")

    def get_last_backup(self):
        """Get the most recent backup branch."""
        if not self.is_git_repo():
            return None

        try:
            # List all backup branches sorted by commit date
            output = self._run_git_command([
                'git', 'branch', '--list', 'backup_*',
                '--sort=-committerdate', '--format=%(refname:short)'
            ])
            branches = output.split('\n')
            return branches[0] if branches and branches[0] else None
        except Exception as e:
            self.logger.error(f"Failed to get last backup: {str(e)}")
            return None

    def create_backup(self, files=None, message=None):
        """Create a backup of the current state."""
        if not self.is_git_repo():
            self.init_repo()

        # Create backup branch name with microseconds to avoid collisions
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        branch_name = f'backup_{timestamp}'

        try:
            # Create new branch for backup
            self._run_git_command(['git', 'checkout', '-b', branch_name])
            
            # Stage specific files or all files
            if files:
                for file in files:
                    try:
                        self._run_git_command(['git', 'add', file])
                    except subprocess.CalledProcessError:
                        # File might not exist, continue with other files
                        continue
            else:
                self._run_git_command(['git', 'add', '.'])

            # Create commit
            commit_message = message or f'Backup created at {timestamp}'
            try:
                self._run_git_command(['git', 'commit', '-m', commit_message])
            except subprocess.CalledProcessError:
                # If nothing to commit, create empty commit
                self._run_git_command(['git', 'commit', '--allow-empty', '-m', commit_message])
            
            self.logger.info(f"Created backup in branch: {branch_name}")
            return branch_name

        except Exception as e:
            self.logger.error(f"Failed to create backup: {str(e)}")
            # Cleanup if something went wrong
            try:
                self._run_git_command(['git', 'checkout', '-'])
                self._run_git_command(['git', 'branch', '-D', branch_name])
            except:
                pass
            raise

    def list_backups(self):
        """List all backup branches."""
        if not self.is_git_repo():
            return []

        try:
            output = self._run_git_command(['git', 'branch'])
            branches = [b.strip() for b in output.split('\n')]
            return [b.replace('* ', '') for b in branches if 'backup_' in b]
        except Exception as e:
            self.logger.error(f"Failed to list backups: {str(e)}")
            return []

    def restore_backup(self, backup_name):
        """Restore files from a backup branch."""
        if not self.is_git_repo():
            raise ValueError("Not a git repository")

        try:
            # Store current branch
            current = self._run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
            
            # Check if there are uncommitted changes
            status = self._run_git_command(['git', 'status', '--porcelain'])
            if status:
                # Try to stash changes
                try:
                    self._run_git_command(['git', 'stash', 'save', 'Temporary stash before restore'])
                except:
                    raise ValueError("Working directory is not clean. Commit or stash changes first.")

            try:
                # Get list of files in the backup
                files = self._run_git_command(['git', 'ls-tree', '-r', '--name-only', backup_name]).split('\n')
                files = [f for f in files if f]  # Filter out empty strings

                # Force checkout files from backup branch
                for file in files:
                    try:
                        # Force checkout to overwrite any local changes
                        self._run_git_command(['git', 'checkout', backup_name, '--', file])
                        self.logger.info(f"Restored: {file}")
                    except subprocess.CalledProcessError:
                        self.logger.warning(f"Failed to restore: {file}")

                # Add restored files to index
                for file in files:
                    try:
                        self._run_git_command(['git', 'add', file])
                    except subprocess.CalledProcessError:
                        pass

                # Commit changes
                try:
                    self._run_git_command(['git', 'commit', '-m', f'Restored files from {backup_name}'])
                except subprocess.CalledProcessError:
                    pass  # No changes to commit

                self.logger.info(f"Restored files from backup: {backup_name}")
                return files

            finally:
                # Always try to get back to the original branch
                try:
                    self._run_git_command(['git', 'checkout', current])
                    # Try to restore stashed changes
                    if status:
                        try:
                            self._run_git_command(['git', 'stash', 'pop'])
                        except:
                            self.logger.warning("Could not restore stashed changes")
                except:
                    pass

        except Exception as e:
            self.logger.error(f"Failed to restore backup: {str(e)}")
            raise

    def delete_backup(self, backup_name):
        """Delete a backup branch."""
        if not self.is_git_repo():
            raise ValueError("Not a git repository")

        try:
            current = self._run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
            if current == backup_name:
                # Try to switch to main/master or create a new branch
                try:
                    self._run_git_command(['git', 'checkout', 'main'])
                except:
                    try:
                        self._run_git_command(['git', 'checkout', 'master'])
                    except:
                        self._run_git_command(['git', 'checkout', '-b', 'main'])
            
            self._run_git_command(['git', 'branch', '-D', backup_name])
            self.logger.info(f"Deleted backup: {backup_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete backup: {str(e)}")
            return False

    def get_backup_info(self, backup_name):
        """Get information about a specific backup."""
        if not self.is_git_repo():
            raise ValueError("Not a git repository")

        try:
            # Get commit information
            commit_info = self._run_git_command([
                'git', 'show', '-s', '--format=%h %ci %s', backup_name
            ])
            
            # Get list of files
            files = self._run_git_command([
                'git', 'ls-tree', '-r', '--name-only', backup_name
            ]).split('\n')

            # Parse commit info
            hash_id, date, *message_parts = commit_info.split(' ')
            message = ' '.join(message_parts)

            return {
                'branch': backup_name,
                'hash': hash_id,
                'date': date,
                'message': message,
                'files': [f for f in files if f]  # Filter out empty strings
            }

        except Exception as e:
            self.logger.error(f"Failed to get backup info: {str(e)}")
            raise
