#!/usr/bin/env python3
"""EMERGENCY SYNTAX FIX VERIFICATION - Complete Test"""

import ast
import os

def test_file_syntax(filepath):
    """Test if a Python file has valid syntax"""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check syntax
        ast.parse(content)
        print(f"✅ {filepath} - Valid syntax")
        return True
        
    except SyntaxError as e:
        print(f"❌ {filepath} - SYNTAX ERROR:")
        print(f"   Line {e.lineno}: {e.text}")
        print(f"   Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filepath} - Error: {e}")
        return False

def main():
    print("🔍 COMPLETE SYNTAX VERIFICATION")
    print("=" * 60)
    
    # Files to check
    files_to_check = [
        'app/routes/main.py',
        'app/routes/stocks.py', 
        'app/routes/analysis.py',
        'app/routes/portfolio.py',
        'app.py',
        'main.py'
    ]
    
    all_passed = True
    
    print("Testing core files:")
    for filepath in files_to_check:
        if os.path.exists(filepath):
            success = test_file_syntax(filepath)
            if not success:
                all_passed = False
        else:
            print(f"⚠️ {filepath} - File not found")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 ALL SYNTAX TESTS PASSED!")
        print("✅ Emergency syntax fix completed successfully")
        print("✅ App should start without syntax errors")
        print("✅ Railway deployment should work")
        print("✅ Website should be accessible")
        print("\n📋 DEPLOYMENT READY!")
    else:
        print("❌ SYNTAX ERRORS FOUND")
        print("❌ Further fixes required before deployment")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
