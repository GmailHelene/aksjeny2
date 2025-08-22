#!/usr/bin/env python3
"""
Comprehensive Cache Clearing Tool for Aksjeradar
Clears all types of cache to ensure fresh content delivery
"""

import os
import shutil
import sys
import time
from pathlib import Path

def clear_flask_cache():
    """Clear Flask application cache"""
    print("🧹 Clearing Flask cache...")
    try:
        from app import create_app
        app = create_app('development')
        with app.app_context():
            from app.extensions import cache
            cache.clear()
            print("✅ Flask cache cleared")
    except Exception as e:
        print(f"⚠️ Could not clear Flask cache: {e}")

def clear_browser_cache_headers():
    """Update cache busting headers in templates"""
    print("🧹 Updating cache busting headers...")
    
    # Generate new cache bust timestamp
    cache_bust = int(time.time())
    
    # Find all HTML templates
    template_dirs = [
        "app/templates",
        "templates",
        "."
    ]
    
    updated_files = 0
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Update cache bust meta tag
                            if 'cache-bust' in content:
                                import re
                                updated_content = re.sub(
                                    r'<meta name="cache-bust" content="[^"]*">',
                                    f'<meta name="cache-bust" content="{cache_bust}">',
                                    content
                                )
                                if updated_content != content:
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        f.write(updated_content)
                                    updated_files += 1
                        except Exception as e:
                            print(f"⚠️ Could not update {file_path}: {e}")
    
    print(f"✅ Updated cache headers in {updated_files} files")

def clear_static_file_cache():
    """Add cache busting to static file URLs"""
    print("🧹 Adding cache busting to static files...")
    
    # Generate cache bust parameter
    cache_bust = int(time.time())
    
    # Create cache busting CSS file
    css_cache_bust = f"""
/* Cache Busting CSS - Generated {time.strftime('%Y-%m-%d %H:%M:%S')} */
/* Version: {cache_bust} */

/* Force refresh of all cached styles */
body {{ 
    --cache-version: "{cache_bust}"; 
}}

/* Ensure Hurtigtilgang text is white */
.card-header h5,
.card-header .fw-bold,
.card-header span {
    color: #ffffff !important;
}

/* Ensure icons stay visible on hover for quick action buttons */
.quick-action-btn:hover i,
.quick-action-btn:hover .bi {
    color: #ffffff !important;
}

.btn-outline-primary:hover i,
.btn-outline-primary:hover .bi,
.btn-outline-success:hover i,
.btn-outline-success:hover .bi,
.btn-outline-info:hover i,
.btn-outline-info:hover .bi,
.btn-outline-dark:hover i,
.btn-outline-dark:hover .bi {
    color: #ffffff !important;
}

/* Fix text contrast issues */
.bg-dark h5,
.bg-dark .fw-bold,
.bg-dark span {
    color: #ffffff !important;
}
"""
    
    # Write cache busting CSS
    cache_css_paths = [
        "app/static/css/cache-bust.css",
        "static/css/cache-bust.css"
    ]
    
    for css_path in cache_css_paths:
        os.makedirs(os.path.dirname(css_path), exist_ok=True)
        try:
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_cache_bust)
            print(f"✅ Created cache busting CSS: {css_path}")
        except Exception as e:
            print(f"⚠️ Could not create {css_path}: {e}")

def clear_python_cache():
    """Clear Python bytecode cache"""
    print("🧹 Clearing Python cache...")
    
    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_dirs.append(os.path.join(root, dir_name))
    
    removed = 0
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            removed += 1
        except Exception as e:
            print(f"⚠️ Could not remove {cache_dir}: {e}")
    
    print(f"✅ Removed {removed} __pycache__ directories")

def clear_temp_files():
    """Clear temporary files"""
    print("🧹 Clearing temporary files...")
    
    temp_patterns = [
        "*.pyc",
        "*.pyo",
        "*~",
        ".DS_Store",
        "Thumbs.db",
        "*.tmp",
        "*.log"
    ]
    
    removed = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            for pattern in temp_patterns:
                if file.endswith(pattern.replace('*', '')):
                    try:
                        os.remove(file_path)
                        removed += 1
                        break
                    except Exception as e:
                        print(f"⚠️ Could not remove {file_path}: {e}")
    
    print(f"✅ Removed {removed} temporary files")

def restart_suggestion():
    """Provide restart suggestions"""
    print("\n🚀 Cache clearing complete!")
    print("\n📋 Next steps to ensure changes take effect:")
    print("1. Restart your Flask development server")
    print("2. Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
    print("3. Clear browser cache/data for aksjeradar.trade")
    print("4. Try opening in incognito/private mode")
    print("\n💡 If issues persist, try:")
    print("   - Restart your browser completely")
    print("   - Clear DNS cache (ipconfig /flushdns on Windows)")
    print("   - Wait 5-10 minutes for CDN cache to expire")

def main():
    """Main cache clearing function"""
    print("🔥 COMPREHENSIVE CACHE CLEARING TOOL")
    print("=" * 50)
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all cache clearing operations
    clear_python_cache()
    clear_temp_files()
    clear_browser_cache_headers()
    clear_static_file_cache()
    clear_flask_cache()
    
    restart_suggestion()

if __name__ == "__main__":
    main()
