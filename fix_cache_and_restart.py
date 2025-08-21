#!/usr/bin/env python3
"""
Flask Server Cache Clearer and Restart Script
This script will clear template cache and restart the Flask server properly
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def clear_flask_cache():
    """Clear Flask template and bytecode cache"""
    print("🧹 Clearing Flask cache...")
    
    # Clear Python bytecode cache
    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_dirs.append(os.path.join(root, dir_name))
    
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"✅ Removed: {cache_dir}")
        except Exception as e:
            print(f"❌ Failed to remove {cache_dir}: {e}")
    
    # Clear any Flask session cache files
    for cache_file in Path('.').glob('**/.flask_cache*'):
        try:
            cache_file.unlink()
            print(f"✅ Removed: {cache_file}")
        except Exception as e:
            print(f"❌ Failed to remove {cache_file}: {e}")
    
    # Clear Python compiled files
    for pyc_file in Path('.').rglob('*.pyc'):
        try:
            pyc_file.unlink()
            print(f"✅ Removed: {pyc_file}")
        except Exception as e:
            print(f"❌ Failed to remove {pyc_file}: {e}")

def kill_flask_processes():
    """Kill any running Flask processes"""
    print("🔥 Killing Flask processes...")
    try:
        # On Windows
        if os.name == 'nt':
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
            subprocess.run(['taskkill', '/f', '/im', 'python3.exe'], 
                         capture_output=True, text=True)
        else:
            # On Unix/Linux
            subprocess.run(['pkill', '-f', 'flask'], capture_output=True)
            subprocess.run(['pkill', '-f', 'main.py'], capture_output=True)
        print("✅ Flask processes killed")
    except Exception as e:
        print(f"❌ Error killing processes: {e}")

def start_flask():
    """Start Flask server with fresh environment"""
    print("🚀 Starting Flask server...")
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = '1'
    env['TEMPLATES_AUTO_RELOAD'] = '1'
    
    try:
        # Start Flask
        subprocess.Popen([sys.executable, 'main.py'], env=env)
        print("✅ Flask server started on http://localhost:5002")
        print("📋 Check the terminal for any BuildError messages")
    except Exception as e:
        print(f"❌ Failed to start Flask: {e}")

def main():
    """Main function"""
    print("🔧 Flask Cache Clearer & Restart Tool")
    print("=====================================")
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Please run this script from the project root.")
        return
    
    # 1. Kill running processes
    kill_flask_processes()
    
    # 2. Clear cache
    clear_flask_cache()
    
    # 3. Start Flask with template auto-reload
    start_flask()
    
    print("\n🎉 Process complete!")
    print("💡 If you still see BuildError, check:")
    print("   1. All templates use correct URL endpoints:")
    print("      - 'analysis.index' not 'analysis.analysis'")
    print("      - 'portfolio.view_portfolio' not 'portfolio.portfolio'") 
    print("      - 'forum.index' not 'forum.forum'")
    print("   2. No Python code redirects to incorrect endpoints")
    print("   3. Browser cache is cleared (Ctrl+Shift+R)")
    print("   4. Run builderror_scanner.py to find remaining issues")

if __name__ == '__main__':
    main()
