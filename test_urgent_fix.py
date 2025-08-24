#!/usr/bin/env python3
"""
URGENT DEPLOYMENT FIX TEST
Test critical deployment errors that are blocking the app
"""

import os
import sys
import traceback

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_critical_syntax_fix():
    """Test that the critical syntax error in stocks.py has been fixed"""
    print("🚨 CRITICAL: Testing syntax fix in stocks.py")
    try:
        import ast
        with open('app/routes/stocks.py', 'r') as f:
            content = f.read()
        
        # Try to parse the file
        ast.parse(content)
        print("✅ CRITICAL FIX SUCCESS: stocks.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ CRITICAL ERROR: Syntax error still exists: {e}")
        print(f"   Line {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return False

def test_imports():
    """Test that all the problematic routes can be imported without errors"""
    
    print("\n🔧 Testing critical route imports...")
    
    try:
        print("📦 Testing main app import...")
        from app import create_app
        print("✅ Main app import successful")
        
        print("📦 Testing Flask app creation...")
        app = create_app('development')
        print("✅ Flask app creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL IMPORT FAILED: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚨 URGENT DEPLOYMENT FIX VERIFICATION")
    print("Testing critical errors that block deployment")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Critical syntax fix
    syntax_ok = test_critical_syntax_fix()
    all_tests_passed = all_tests_passed and syntax_ok
    
    # Test 2: Import test
    import_ok = test_imports()
    all_tests_passed = all_tests_passed and import_ok
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("✅ ALL CRITICAL DEPLOYMENT TESTS PASSED!")
        print("🚀 APPLICATION SHOULD DEPLOY SUCCESSFULLY NOW!")
        print()
        print("📋 Summary of fixes:")
        print("   ✅ Fixed syntax error in app/routes/stocks.py line 381")
        print()
        print("🎯 Ready to continue with 500 error endpoint testing")
    else:
        print("❌ CRITICAL DEPLOYMENT TESTS FAILED!")
        print("🛑 Fix these errors before attempting deployment")
        sys.exit(1)
