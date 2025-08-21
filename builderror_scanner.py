#!/usr/bin/env python3
"""
BuildError Fixer - Finds and fixes all BuildError issues
Detects incorrect URL references and provides fixes
"""
import os
import re
from pathlib import Path

def scan_for_builderrors():
    """Scan all templates for potential BuildError issues"""
    print("🔍 Scanning for BuildError issues...")
    print("="*50)
    
    # Define common incorrect patterns and their fixes
    incorrect_patterns = {
        "url_for('analysis.analysis')": "url_for('analysis.index')",
        "url_for('portfolio.portfolio')": "url_for('portfolio.view_portfolio')",
        "url_for('forum.forum')": "url_for('forum.index')",
        "url_for('stocks.stocks')": "url_for('stocks.index')",
        "url_for('main.main')": "url_for('main.index')",
        "url_for('pricing.pricing')": "url_for('pricing.index')",
        "url_for('auth.auth')": "url_for('auth.login')",
    }
    
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
                
            # Check for each incorrect pattern
            for incorrect, correct in incorrect_patterns.items():
                if incorrect in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if incorrect in line:
                            issues_found.append({
                                'file': str(template_file),
                                'line': i,
                                'content': line.strip(),
                                'incorrect': incorrect,
                                'correct': correct
                            })
                            print(f"❌ {template_file}:{i}")
                            print(f"   Found: {line.strip()}")
                            print(f"   Should be: {line.replace(incorrect, correct).strip()}")
                            print()
        
        except Exception as e:
            print(f"⚠️  Error reading {template_file}: {e}")
    
    # Check Python files too for redirect issues
    print(f"\n🐍 Scanning Python files...")
    python_files = list(Path('.').glob('**/*.py'))
    
    for py_file in python_files:
        if 'test_builderror_fix.py' in str(py_file):
            continue  # Skip test file
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for incorrect patterns in Python redirects
            for incorrect, correct in incorrect_patterns.items():
                if incorrect in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if incorrect in line:
                            issues_found.append({
                                'file': str(py_file),
                                'line': i,
                                'content': line.strip(),
                                'incorrect': incorrect,
                                'correct': correct
                            })
                            print(f"❌ {py_file}:{i}")
                            print(f"   Found: {line.strip()}")
                            print(f"   Should be: {line.replace(incorrect, correct).strip()}")
                            print()
        
        except Exception as e:
            print(f"⚠️  Error reading {py_file}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Template files scanned: {len(template_files)}")
    print(f"   Python files scanned: {len(python_files)}")
    print(f"   Issues found: {len(issues_found)}")
    
    if not issues_found:
        print("✅ No BuildError issues found!")
        print("🎉 All URL references appear to be correct!")
    else:
        print("\n🛠️  To fix these issues:")
        print("1. Replace each 'Found' line with the 'Should be' version")
        print("2. Clear Flask cache and restart server")
        print("3. Test navigation thoroughly")
    
    return issues_found

def check_blueprint_registrations():
    """Check that all blueprints are properly registered"""
    print(f"\n🔗 Checking blueprint registrations...")
    
    try:
        # Look for blueprint registrations in __init__.py
        init_files = list(Path('.').glob('**/app/__init__.py'))
        
        for init_file in init_files:
            print(f"📄 Checking {init_file}")
            
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for blueprint registrations
            blueprint_patterns = [
                r'app\.register_blueprint\((\w+)',
                r'from.*routes.*import\s+(\w+)',
            ]
            
            registered_blueprints = []
            for pattern in blueprint_patterns:
                matches = re.findall(pattern, content)
                registered_blueprints.extend(matches)
            
            if registered_blueprints:
                print(f"✅ Found registered blueprints: {', '.join(set(registered_blueprints))}")
            else:
                print(f"⚠️  No blueprint registrations found")
                
    except Exception as e:
        print(f"❌ Error checking blueprints: {e}")

def main():
    """Main function"""
    print("🔧 BuildError Scanner & Fixer")
    print("=============================")
    
    # Check if we're in the right directory
    if not os.path.exists('app'):
        print("❌ Error: 'app' directory not found. Please run this script from the project root.")
        return
    
    # 1. Scan for BuildError issues
    issues = scan_for_builderrors()
    
    # 2. Check blueprint registrations
    check_blueprint_registrations()
    
    print(f"\n🎯 Next steps:")
    if issues:
        print("   1. Fix the issues listed above")
        print("   2. Run this script again to verify")
        print("   3. Clear Flask cache and restart server")
        print("   4. Test all navigation links")
    else:
        print("   1. Clear Flask cache: python fix_cache_and_restart.py")
        print("   2. Restart Flask server")
        print("   3. Test the application thoroughly")
        print("   4. Check browser console for any remaining errors")

if __name__ == '__main__':
    main()
