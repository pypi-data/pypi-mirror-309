"""
Tests for the Config class
"""
import os
import pytest
import yaml
import tempfile
from pathlib import Path
from markdown2code.config import Config, DEFAULT_CONFIG

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def custom_config():
    return {
        'file_patterns': {
            'python': ['custom.py'],
            'newlang': ['new.nl']
        },
        'logging': {
            'level': 'DEBUG'
        },
        'output': {
            'colored': True
        }
    }

def test_default_config():
    config = Config()
    assert config.config == DEFAULT_CONFIG
    
    # Test default file patterns
    patterns = config.get_file_patterns('python')
    assert 'main.py' in patterns
    assert 'script.py' in patterns

def test_get_file_patterns_unknown_language():
    config = Config()
    patterns = config.get_file_patterns('unknown_lang')
    assert patterns == ['file.unknown_lang']

def test_get_logging_config():
    config = Config()
    logging_config = config.get_logging_config()
    assert logging_config['level'] == 'INFO'
    assert 'format' in logging_config

def test_get_output_config():
    config = Config()
    output_config = config.get_output_config()
    assert 'colored' in output_config
    assert 'verbose' in output_config

def test_merge_config(temp_dir, custom_config):
    config_path = Path(temp_dir) / '.markdown2code.yml'
    
    # Write custom config
    with open(config_path, 'w') as f:
        yaml.dump(custom_config, f)
    
    # Create config instance with custom config path
    config = Config(config_dir=temp_dir)
    
    # Test merged file patterns
    python_patterns = config.get_file_patterns('python')
    assert 'custom.py' in python_patterns
    
    # Test new language patterns
    newlang_patterns = config.get_file_patterns('newlang')
    assert 'new.nl' in newlang_patterns
    
    # Test merged logging config
    assert config.get_logging_config()['level'] == 'DEBUG'
    
    # Test merged output config
    assert config.get_output_config()['colored'] is True

def test_create_default_config(temp_dir):
    config_path = Path(temp_dir) / 'config.yml'
    
    # Create default config file
    created_path = Config.create_default_config(config_path)
    assert created_path == config_path
    assert config_path.exists()
    
    # Verify content
    with open(config_path, 'r') as f:
        saved_config = yaml.safe_load(f)
        assert saved_config == DEFAULT_CONFIG

def test_multiple_config_locations(temp_dir):
    # Create configs in different locations
    configs = {
        '.markdown2code.yml': {
            'file_patterns': {'python': ['local.py']}
        },
        '.config/markdown2code/config.yml': {
            'file_patterns': {'python': ['global.py']}
        }
    }
    
    for path, content in configs.items():
        full_path = Path(temp_dir) / path
        os.makedirs(full_path.parent, exist_ok=True)
        with open(full_path, 'w') as f:
            yaml.dump(content, f)
    
    # Test config loading precedence
    config = Config(config_dir=temp_dir)
    patterns = config.get_file_patterns('python')
    assert 'local.py' in patterns  # Local config should take precedence

def test_invalid_config_handling(temp_dir):
    config_path = Path(temp_dir) / '.markdown2code.yml'
    
    # Write invalid YAML
    with open(config_path, 'w') as f:
        f.write('invalid: yaml: content:')
    
    # Should not raise exception and use default config
    config = Config(config_dir=temp_dir)
    assert config.config == DEFAULT_CONFIG

def test_empty_config_handling(temp_dir):
    config_path = Path(temp_dir) / '.markdown2code.yml'
    
    # Write empty file
    config_path.touch()
    
    # Should use default config
    config = Config(config_dir=temp_dir)
    assert config.config == DEFAULT_CONFIG

def test_partial_config_merge(temp_dir):
    partial_config = {
        'file_patterns': {
            'python': ['custom.py']
        }
    }
    
    config_path = Path(temp_dir) / '.markdown2code.yml'
    with open(config_path, 'w') as f:
        yaml.dump(partial_config, f)
    
    config = Config(config_dir=temp_dir)
    
    # Check merged python patterns
    assert 'custom.py' in config.get_file_patterns('python')
    
    # Check other config sections remain default
    assert config.get_logging_config() == DEFAULT_CONFIG['logging']
    assert config.get_output_config() == DEFAULT_CONFIG['output']
