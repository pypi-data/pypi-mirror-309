"""
Tests for the GitBackup class
"""
import os
import time
import pytest
import tempfile
from pathlib import Path
from markdown2code.backup import GitBackup

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Initialize git repo
        os.system(f"cd {tmpdirname} && git init")
        os.system(f"cd {tmpdirname} && git config user.email 'test@example.com'")
        os.system(f"cd {tmpdirname} && git config user.name 'Test User'")
        os.system(f"cd {tmpdirname} && git commit --allow-empty -m 'Initial commit'")
        yield tmpdirname

@pytest.fixture
def git_backup(temp_dir):
    return GitBackup(temp_dir)

@pytest.fixture
def sample_files(temp_dir):
    # Create some sample files
    files = ['test1.txt', 'test2.txt']
    for file in files:
        path = Path(temp_dir) / file
        path.write_text(f"Content of {file}")
        os.system(f"cd {temp_dir} && git add {file}")
    os.system(f"cd {temp_dir} && git commit -m 'Add sample files'")
    return files

def test_init_repo(temp_dir):
    backup = GitBackup(temp_dir)
    assert backup.is_git_repo()

def test_list_backups(git_backup, sample_files):
    # Create multiple backups
    backup1 = git_backup.create_backup([sample_files[0]])
    os.system(f"cd {git_backup.working_dir} && git checkout main")
    time.sleep(0.1)  # Ensure different timestamps
    backup2 = git_backup.create_backup([sample_files[1]])
    
    backups = git_backup.list_backups()
    assert len(backups) == 2
    assert backup1 in backups
    assert backup2 in backups

def test_get_last_backup(git_backup, sample_files):
    backup1 = git_backup.create_backup([sample_files[0]])
    os.system(f"cd {git_backup.working_dir} && git checkout main")
    time.sleep(0.1)  # Ensure different timestamps
    backup2 = git_backup.create_backup([sample_files[1]])
    
    # Get timestamps from backup names
    _, date1, time1, micro1 = backup1.split('_')
    _, date2, time2, micro2 = backup2.split('_')
    timestamp1 = int(date1 + time1 + micro1)
    timestamp2 = int(date2 + time2 + micro2)
    
    # Verify backup2 is newer than backup1
    assert timestamp2 > timestamp1
    
    # Verify get_last_backup returns a newer backup than backup1
    last_backup = git_backup.get_last_backup()
    _, date_last, time_last, micro_last = last_backup.split('_')
    last_timestamp = int(date_last + time_last + micro_last)
    assert last_timestamp > timestamp1

def test_restore_backup(git_backup, sample_files, temp_dir):
    # Create initial content
    file_path = Path(temp_dir) / sample_files[0]
    initial_content = "Initial content"
    file_path.write_text(initial_content)
    os.system(f"cd {temp_dir} && git add {sample_files[0]}")
    os.system(f"cd {temp_dir} && git commit -m 'Initial content'")
    
    # Create backup
    backup_name = git_backup.create_backup([sample_files[0]])
    os.system(f"cd {temp_dir} && git checkout main")
    
    # Modify file
    modified_content = "Modified content"
    file_path.write_text(modified_content)
    os.system(f"cd {temp_dir} && git add {sample_files[0]}")
    os.system(f"cd {temp_dir} && git commit -m 'Modified content'")
    
    # Restore backup
    restored_files = git_backup.restore_backup(backup_name)
    assert sample_files[0] in restored_files
    
    # Verify content was restored
    assert file_path.read_text() == initial_content

def test_delete_backup(git_backup, sample_files):
    backup_name = git_backup.create_backup(sample_files)
    os.system(f"cd {git_backup.working_dir} && git checkout main")
    assert backup_name in git_backup.list_backups()
    
    # Delete backup
    assert git_backup.delete_backup(backup_name)
    assert backup_name not in git_backup.list_backups()

def test_get_backup_info(git_backup, sample_files):
    backup_name = git_backup.create_backup(sample_files, "Test backup message")
    info = git_backup.get_backup_info(backup_name)
    
    assert info['branch'] == backup_name
    assert 'hash' in info
    assert 'date' in info
    assert 'Test backup message' in info['message']
    assert all(file in info['files'] for file in sample_files)

def test_error_handling_no_repo():
    with tempfile.TemporaryDirectory() as tmpdirname:
        backup = GitBackup(tmpdirname)
        with pytest.raises(ValueError):
            backup.restore_backup("nonexistent_backup")
        
        with pytest.raises(ValueError):
            backup.delete_backup("nonexistent_backup")
        
        with pytest.raises(ValueError):
            backup.get_backup_info("nonexistent_backup")

def test_error_handling_invalid_backup(git_backup):
    with pytest.raises(Exception):
        git_backup.restore_backup("nonexistent_backup")
    
    with pytest.raises(Exception):
        git_backup.get_backup_info("nonexistent_backup")

def test_backup_with_no_files(git_backup):
    # Test creating backup with no files
    backup_name = git_backup.create_backup()
    assert backup_name in git_backup.list_backups()

def test_backup_with_nonexistent_files(git_backup):
    # Test creating backup with nonexistent files
    backup_name = git_backup.create_backup(['nonexistent.txt'])
    assert backup_name in git_backup.list_backups()

def test_restore_with_uncommitted_changes(git_backup, sample_files, temp_dir):
    # Create and backup a file
    file_path = Path(temp_dir) / sample_files[0]
    initial_content = "Initial content"
    file_path.write_text(initial_content)
    os.system(f"cd {temp_dir} && git add {sample_files[0]}")
    os.system(f"cd {temp_dir} && git commit -m 'Initial content'")
    
    backup_name = git_backup.create_backup([sample_files[0]])
    os.system(f"cd {temp_dir} && git checkout main")
    
    # Create an uncommitted change
    new_file = Path(temp_dir) / "uncommitted.txt"
    new_file.write_text("Uncommitted content")
    
    # Restore should work by stashing changes
    restored_files = git_backup.restore_backup(backup_name)
    assert sample_files[0] in restored_files
    assert file_path.read_text() == initial_content
