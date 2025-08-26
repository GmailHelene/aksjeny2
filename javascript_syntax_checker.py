#!/usr/bin/env python3
"""
JavaScript Syntax Error Detector
Identifies potential JavaScript syntax issues in HTML templates
"""

import os
import re
import glob

def check_javascript_syntax():
    """Check for common JavaScript syntax issues in templates"""
    
    template_dir = "app/templates"
    issues_found = []
    
    # Pattern for Jinja2 expressions in JavaScript contexts
    jinja_in_js_patterns = [
        r'fetch\([^)]*\{\{[^}]*\}\}[^)]*\)',  # Jinja2 in fetch calls
        r'addEventListener\([^)]*\{\{[^}]*\}\}[^)]*\)',  # Jinja2 in event listeners  
        r'console\.[a-z]+\([^)]*\{\{[^}]*\}\}[^)]*\)',  # Jinja2 in console calls
        r'\.innerHTML\s*=\s*[^;]*\{\{[^}]*\}\}[^;]*;',  # Jinja2 in innerHTML
        r'document\.getElementById\([^)]*\{\{[^}]*\}\}[^)]*\)',  # Jinja2 in getElementById
    ]
    
    # Find all HTML template files
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                        lines = content.split('\n')
                        
                        # Check for patterns that could cause syntax errors
                        for i, line in enumerate(lines, 1):
                            for pattern in jinja_in_js_patterns:
                                if re.search(pattern, line):
                                    issues_found.append({
                                        'file': filepath,
                                        'line': i,
                                        'issue': f'Potential JavaScript syntax issue: {line.strip()[:100]}...',
                                        'pattern': pattern
                                    })
                                    
                            # Check for unclosed braces in script sections
                            if '<script>' in line.lower():
                                script_section = True
                                brace_count = 0
                                
                            if '</script>' in line.lower():
                                script_section = False
                                
                    except Exception as e:
                        issues_found.append({
                            'file': filepath,
                            'line': 0,
                            'issue': f'Could not read file: {str(e)}',
                            'pattern': 'file_error'
                        })
    
    return issues_found

if __name__ == "__main__":
    print("🔍 Checking for JavaScript syntax issues in templates...")
    issues = check_javascript_syntax()
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} potential issues:")
        for issue in issues:
            print(f"\n📄 {issue['file']}:{issue['line']}")
            print(f"   {issue['issue']}")
    else:
        print("\n✅ No obvious JavaScript syntax issues found!")
    
    print(f"\n📊 Checked templates in app/templates directory")
