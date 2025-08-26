#!/usr/bin/env python3
"""Scan all templates for missing endblock tags"""

import os
import re

def scan_template_files():
    """Scan all HTML template files for block/endblock mismatches"""
    template_dirs = ["app/templates", "templates"]
    issues_found = []
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Find block starts and ends
                            block_starts = re.findall(r'{%\s*block\s+(\w+)', content)
                            endblocks = re.findall(r'{%\s*endblock\s*%}', content)
                            
                            if len(block_starts) != len(endblocks):
                                issues_found.append({
                                    'file': file_path,
                                    'block_starts': len(block_starts),
                                    'endblocks': len(endblocks),
                                    'blocks': block_starts
                                })
                                
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
    
    return issues_found

if __name__ == "__main__":
    print("🔍 Scanning all template files for block/endblock issues...")
    issues = scan_template_files()
    
    if issues:
        print(f"❌ Found {len(issues)} files with block/endblock mismatches:")
        for issue in issues:
            print(f"   📄 {issue['file']}")
            print(f"      - Block starts: {issue['block_starts']}")
            print(f"      - Endblocks: {issue['endblocks']}")
            print(f"      - Block names: {issue['blocks']}")
            print()
    else:
        print("✅ No block/endblock issues found in any template files!")
