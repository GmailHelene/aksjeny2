#!/usr/bin/env python3
"""Clear all cache files and reset application state"""

import os
import shutil
import sys

def clear_cache():
    """Clear all cache directories and files"""
    
    cache_dirs = [
        '__pycache__',
        '.pytest_cache',
        'instance',
        'flask_session'
    ]
    
    # Clear Python cache files
    for root, dirs, files in os.walk('.'):
        # Skip virtual environments
        if 'venv' in root or 'env' in root:
            continue
            
        # Remove __pycache__ directories
        for dir_name in dirs:
            if dir_name in cache_dirs:
                cache_path = os.path.join(root, dir_name)
                print(f"Removing {cache_path}")
                shutil.rmtree(cache_path, ignore_errors=True)
        
        # Remove .pyc files
        for file_name in files:
            if file_name.endswith('.pyc'):
                file_path = os.path.join(root, file_name)
                print(f"Removing {file_path}")
                os.remove(file_path)
    
    print("Cache cleared successfully!")

if __name__ == "__main__":
    clear_cache()
