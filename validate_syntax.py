#!/usr/bin/env python3
"""
Quick syntax validation script to catch Python errors before deployment
"""
import ast
import sys
import os

def validate_python_file(file_path):
    """Validate Python syntax in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the file to check for syntax errors
        ast.parse(content, filename=file_path)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error in {file_path}: {e}"
    except Exception as e:
        return False, f"Error reading {file_path}: {e}"

def main():
    """Validate critical Python files"""
    critical_files = [
        "app/routes/main.py",
        "app/routes/analysis.py", 
        "app/routes/portfolio.py",
        "app/routes/achievements.py",
        "app/__init__.py"
    ]
    
    print("🔍 Validating Python syntax before deployment...")
    all_valid = True
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            valid, error = validate_python_file(file_path)
            if valid:
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path}: {error}")
                all_valid = False
        else:
            print(f"⚠️ {file_path}: File not found")
    
    if all_valid:
        print("\n🎉 All files have valid Python syntax!")
        print("✅ Safe to deploy")
        return 0
    else:
        print("\n💥 Syntax errors found!")
        print("❌ Do not deploy until fixed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
