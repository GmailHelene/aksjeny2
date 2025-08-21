#!/usr/bin/env python3
"""
Comprehensive Template Scanner
Finds ALL template files and checks for incorrect analysis.analysis references
"""
import os
import re
from pathlib import Path

def scan_for_analysis_references():
    """Scan all template files for analysis references"""
    print("🔍 Scanning for analysis.analysis references...")
    print("="*50)
    
    # Find all template files
    template_patterns = ['**/*.html', '**/*.htm', '**/*.jinja', '**/*.jinja2', '**/*.j2']
    template_files = []
    
    for pattern in template_patterns:
        template_files.extend(Path('.').glob(pattern))
    
    print(f"📁 Found {len(template_files)} template files")
    
    # Check each file
    issues_found = []
    for template_file in template_files:
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for analysis.analysis
            if 'analysis.analysis' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'analysis.analysis' in line:
                        issues_found.append({
                            'file': str(template_file),
                            'line': i,
                            'content': line.strip()
                        })
                        print(f"❌ {template_file}:{i} - {line.strip()}")
        
        except Exception as e:
            print(f"⚠️  Error reading {template_file}: {e}")
    
    # Check Python files too
    print(f"\n🐍 Scanning Python files...")
    python_files = list(Path('.').glob('**/*.py'))
    
    for py_file in python_files:
        if 'test_builderror_fix.py' in str(py_file):
            continue  # Skip test file
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for analysis.analysis in url_for calls
            if "url_for('analysis.analysis')" in content:
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if "url_for('analysis.analysis')" in line:
                        issues_found.append({
                            'file': str(py_file),
                            'line': i,
                            'content': line.strip()
                        })
                        print(f"❌ {py_file}:{i} - {line.strip()}")
        
        except Exception as e:
            print(f"⚠️  Error reading {py_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Template files scanned: {len(template_files)}")
    print(f"   Python files scanned: {len(python_files)}")
    print(f"   Issues found: {len(issues_found)}")
    
    if not issues_found:
        print("✅ No analysis.analysis references found!")
        print("💡 The error might be caused by:")
        print("   1. Template cache")
        print("   2. Browser cache")
        print("   3. Server-side cache")
        print("   4. Generated templates")
    
    return issues_found

def check_template_inheritance():
    """Check which base template is actually being used"""
    print(f"\n🏗️  Checking template inheritance...")
    
    # Find demo.html and see which base it extends
    demo_files = list(Path('.').glob('**/demo.html'))
    for demo_file in demo_files:
        try:
            with open(demo_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for extends statement
            extends_match = re.search(r'{%\s*extends\s+["\']([^"\']+)["\']', content)
            if extends_match:
                base_template = extends_match.group(1)
                print(f"📄 {demo_file} extends: {base_template}")
                
                # Find the actual base template file
                base_files = list(Path('.').glob(f'**/{base_template}'))
                for base_file in base_files:
                    print(f"   ↳ Found: {base_file}")
                    
                    # Check if this base file has issues
                    try:
                        with open(base_file, 'r', encoding='utf-8') as f:
                            base_content = f.read()
                        
                        if 'analysis.analysis' in base_content:
                            print(f"   ❌ This base template contains analysis.analysis!")
                        else:
                            print(f"   ✅ This base template looks clean")
                    except Exception as e:
                        print(f"   ⚠️  Error reading base template: {e}")
            
        except Exception as e:
            print(f"⚠️  Error reading {demo_file}: {e}")

def main():
    """Main function"""
    print("🔍 Comprehensive Template Scanner")
    print("=================================")
    
    # Scan for issues
    issues = scan_for_analysis_references()
    
    # Check template inheritance
    check_template_inheritance()
    
    print(f"\n🎯 Next steps:")
    if issues:
        print("   1. Fix the issues listed above")
        print("   2. Clear Flask cache")
        print("   3. Restart server")
    else:
        print("   1. Run fix_cache_and_restart.py")
        print("   2. Clear browser cache")
        print("   3. Test the application")

if __name__ == '__main__':
    main()
