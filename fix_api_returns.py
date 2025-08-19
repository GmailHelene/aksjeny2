#!/usr/bin/env python3
"""
Fix API returns that use tuple syntax which is incompatible with security headers.
Replace: return jsonify(...), status_code
With: response = jsonify(...); response.status_code = status_code; return response
"""

import re

def fix_api_file():
    """Fix all tuple returns in api.py"""
    
    # Read the file
    with open('/workspaces/aksjeny/app/routes/api.py', 'r') as f:
        content = f.read()
    
    # Pattern to match: return jsonify({...}), status_code
    pattern = r'return jsonify\(([^)]+)\), (\d+)'
    
    def replacement(match):
        jsonify_content = match.group(1)
        status_code = match.group(2)
        return f"""response = jsonify({jsonify_content})
        response.status_code = {status_code}
        return response"""
    
    # Replace all occurrences
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    # Write back to file
    with open('/workspaces/aksjeny/app/routes/api.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Fixed API tuple returns")

if __name__ == "__main__":
    fix_api_file()
