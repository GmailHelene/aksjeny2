#!/usr/bin/env python3
"""
Force cache clearing script for Aksjeradar
"""
import time
import os
import hashlib
from datetime import datetime

def generate_version_hash():
    """Generate a unique version hash based on current time"""
    current_time = str(time.time())
    return hashlib.md5(current_time.encode()).hexdigest()[:8]

def update_template_with_cache_buster():
    """Add cache-busting parameters to all static assets in base template"""
    template_path = '/workspaces/aksjeny/app/templates/base.html'
    version = generate_version_hash()
    
    print(f"🔥 FORCE CACHE CLEAR - Version: {version}")
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add cache-busting to CSS and JS includes
    cache_buster_comment = f'<!-- CACHE BUSTER: {version} - {datetime.now().isoformat()} -->'
    
    # Find the head section and add cache buster
    if '<head>' in content and cache_buster_comment not in content:
        content = content.replace('<head>', f'<head>\n{cache_buster_comment}')
        
        # Update Bootstrap CSS
        content = content.replace(
            'bootstrap.min.css',
            f'bootstrap.min.css?v={version}'
        )
        
        # Update any custom CSS
        content = content.replace(
            'href="/static/css/',
            f'href="/static/css/'
        ).replace('.css"', f'.css?v={version}"')
        
        # Update Bootstrap JS
        content = content.replace(
            'bootstrap.bundle.min.js',
            f'bootstrap.bundle.min.js?v={version}'
        )
        
        # Update any custom JS
        content = content.replace(
            'src="/static/js/',
            f'src="/static/js/'
        ).replace('.js"', f'.js?v={version}"')
        
        print(f"✅ Added cache buster version {version} to template")
        
        # Write back to file
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    else:
        print("ℹ️ Template already has cache buster or no <head> found")
        return False

if __name__ == "__main__":
    success = update_template_with_cache_buster()
    if success:
        print("🚀 Cache cleared! Restart Flask server for changes to take effect.")
        print("🌍 Open URL with ?v=force_refresh to bypass browser cache")
    else:
        print("⚠️ No changes made to template")
