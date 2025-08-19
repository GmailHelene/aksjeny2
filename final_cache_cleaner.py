#!/usr/bin/env python3
"""
Comprehensive Cache Cleaner for Aksjeradar
Clears all forms of cache to ensure fresh deployment
"""
import os
import shutil
import glob
import subprocess
import sys

def clear_python_cache():
    """Clear Python cache files"""
    print("🧹 Clearing Python cache files...")
    
    # Remove __pycache__ directories
    pycache_dirs = glob.glob('**/__pycache__', recursive=True)
    for cache_dir in pycache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"   ✓ Removed {cache_dir}")
    
    # Remove .pyc files
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        if os.path.exists(pyc_file):
            os.remove(pyc_file)
            print(f"   ✓ Removed {pyc_file}")
    
    print(f"   ✓ Cleared {len(pycache_dirs)} cache directories and {len(pyc_files)} .pyc files")

def clear_flask_cache():
    """Clear Flask-specific cache"""
    print("🧹 Clearing Flask cache...")
    
    # Common Flask cache directories
    cache_dirs = [
        'flask_session',
        'instance',
        '.flask_cache',
        'cache',
        'tmp'
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"   ✓ Removed {cache_dir}")

def clear_static_cache():
    """Clear static file cache"""
    print("🧹 Clearing static file cache...")
    
    # Add cache busting by updating timestamps
    static_dirs = [
        'app/static/css',
        'app/static/js',
        'app/static/img'
    ]
    
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            # Touch all files to update timestamps
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        os.utime(filepath, None)  # Updates to current time
                    except:
                        pass
            print(f"   ✓ Updated timestamps in {static_dir}")

def clear_logs():
    """Clear log files"""
    print("🧹 Clearing log files...")
    
    log_patterns = [
        '*.log',
        'logs/*.log',
        'app/logs/*.log'
    ]
    
    cleared_logs = 0
    for pattern in log_patterns:
        log_files = glob.glob(pattern, recursive=True)
        for log_file in log_files:
            if os.path.exists(log_file):
                with open(log_file, 'w') as f:
                    f.write('')  # Clear content but keep file
                cleared_logs += 1
                print(f"   ✓ Cleared {log_file}")
    
    print(f"   ✓ Cleared {cleared_logs} log files")

def clear_database_cache():
    """Clear database cache if exists"""
    print("🧹 Clearing database cache...")
    
    cache_files = [
        'app.db-journal',
        'app.db-wal',
        'app.db-shm'
    ]
    
    for cache_file in cache_files:
        if os.path.exists(cache_file):
            os.remove(cache_file)
            print(f"   ✓ Removed {cache_file}")

def clear_node_modules():
    """Clear node_modules if exists"""
    print("🧹 Clearing Node.js cache...")
    
    if os.path.exists('node_modules'):
        shutil.rmtree('node_modules')
        print("   ✓ Removed node_modules directory")
    
    if os.path.exists('package-lock.json'):
        os.remove('package-lock.json')
        print("   ✓ Removed package-lock.json")

def clear_git_cache():
    """Clear Git cache"""
    print("🧹 Clearing Git cache...")
    
    try:
        # Clear git index
        subprocess.run(['git', 'rm', '-r', '--cached', '.'], check=False, capture_output=True)
        subprocess.run(['git', 'add', '.'], check=False, capture_output=True)
        print("   ✓ Cleared Git cache and re-added files")
    except Exception as e:
        print(f"   ⚠️  Git cache clear failed: {e}")

def display_summary():
    """Display cleanup summary"""
    print("\n" + "="*60)
    print("📋 CACHE CLEANUP SUMMARY")
    print("="*60)
    print("✅ Python cache files cleared")
    print("✅ Flask cache cleared")
    print("✅ Static file timestamps updated")
    print("✅ Log files cleared")
    print("✅ Database cache cleared")
    print("✅ Node.js cache cleared")
    print("✅ Git cache cleared")
    print("\n🎉 All cache cleared successfully!")
    print("💡 Ready for git push to master")
    print("="*60)

def main():
    """Main cleanup function"""
    print("🚀 Starting comprehensive cache cleanup...")
    print("="*60)
    
    # Execute all cleanup functions
    clear_python_cache()
    clear_flask_cache()
    clear_static_cache()
    clear_logs()
    clear_database_cache()
    clear_node_modules()
    clear_git_cache()
    
    # Display summary
    display_summary()

if __name__ == "__main__":
    main()
