#!/usr/bin/env python3
"""
Clear all application caches
"""
import os
import shutil
import tempfile
from pathlib import Path

def clear_cache():
    """Clear all caches"""
    cache_dirs = [
        '__pycache__',
        '.pytest_cache', 
        'app/__pycache__',
        'app/routes/__pycache__',
        'app/services/__pycache__',
        'app/models/__pycache__',
        'app/utils/__pycache__'
    ]
    
    removed_count = 0
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"✅ Removed cache directory: {cache_dir}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {cache_dir}: {e}")
    
    # Clear Python bytecode files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                try:
                    os.remove(os.path.join(root, file))
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Failed to remove {file}: {e}")
    
    print(f"🧹 Cache clearing complete! Removed {removed_count} items")
    
    # Update cache busting timestamp
    import datetime
    cache_bust = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"🔄 New cache bust timestamp: {cache_bust}")

if __name__ == "__main__":
    clear_cache()
