#!/usr/bin/env python3
"""
Script to fix blueprint conflict in app/__init__.py
Run this to automatically fix the duplicate blueprint registration
"""

import re

def fix_blueprint_conflict():
    # Read the current app/__init__.py
    with open('app/__init__.py', 'r') as f:
        content = f.read()
    
    # Find and remove duplicate external_data_bp registrations
    # Keep only the first one or the one with url_prefix
    
    # Pattern to find blueprint registrations
    pattern = r'app\.register_blueprint\(external_data_bp[^)]*\)'
    matches = re.findall(pattern, content)
    
    if len(matches) > 1:
        # Found duplicates, keep only the first one with proper config
        # Replace all occurrences with a single proper registration
        content = re.sub(pattern, '', content)
        
        # Add single proper registration at the right place
        insert_point = content.find('# Register blueprints')
        if insert_point == -1:
            insert_point = content.find('app.register_blueprint')
        
        # Insert the proper registration
        registration = """
    # External data blueprint (fixed)
    try:
        from app.external_data import external_data_bp
        app.register_blueprint(external_data_bp, url_prefix='/external-data')
    except (ImportError, ValueError) as e:
        # Blueprint might already be registered or module doesn't exist
        print(f"Warning: Could not register external_data blueprint: {e}")
        pass
"""
        
        # Insert after the marker
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Register blueprints' in line:
                lines.insert(i + 1, registration)
                break
        
        content = '\n'.join(lines)
    
    # Write back the fixed content
    with open('app/__init__.py', 'w') as f:
        f.write(content)
    
    print("Blueprint conflict fixed!")

if __name__ == '__main__':
    fix_blueprint_conflict()
