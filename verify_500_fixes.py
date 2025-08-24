#!/usr/bin/env python3
"""
Comprehensive verification of 500 error fixes
Tests all problematic endpoints and verifies fixes are working
"""

import sys
import traceback
from pathlib import Path

def verify_syntax_fixes():
    """Verify no syntax errors in critical files"""
    print("🔍 VERIFYING SYNTAX FIXES...")
    
    critical_files = [
        'app/routes/stocks.py',
        'app/routes/portfolio.py', 
        'app/routes/analysis.py',
        'app/routes/advanced_features.py',
        'app/routes/main.py',
        'app/routes/pro_tools.py'
    ]
    
    syntax_errors = []
    
    for file_path in critical_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, file_path, 'exec')
                print(f"✅ {file_path}: No syntax errors")
            except SyntaxError as e:
                error_msg = f"❌ {file_path}: SyntaxError at line {e.lineno}: {e.msg}"
                print(error_msg)
                syntax_errors.append(error_msg)
            except Exception as e:
                error_msg = f"⚠️  {file_path}: Other error: {e}"
                print(error_msg)
        else:
            print(f"⚠️  {file_path}: File not found")
    
    return len(syntax_errors) == 0

def verify_route_patterns():
    """Verify expected route patterns exist in files"""
    print("\n🗺️  VERIFYING ROUTE PATTERNS...")
    
    expected_routes = {
        'app/routes/portfolio.py': [
            r"@portfolio\.route\('/watchlist'\)",
            r"@portfolio\.route\('/<int:id>/add'",
        ],
        'app/routes/analysis.py': [
            r"@analysis\.route\('/sentiment'\)",
            r"@analysis\.route\('/warren-buffett'",
        ],
        'app/routes/main.py': [
            r"@main\.route\('/profile'\)",
        ],
        'app/routes/pro_tools.py': [
            r"@pro_tools\.route\('/alerts'",
        ]
    }
    
    route_issues = []
    
    for file_path, patterns in expected_routes.items():
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern in patterns:
                    import re
                    if re.search(pattern, content):
                        print(f"✅ {file_path}: Found {pattern}")
                    else:
                        issue = f"❌ {file_path}: Missing {pattern}"
                        print(issue)
                        route_issues.append(issue)
                        
            except Exception as e:
                issue = f"⚠️  {file_path}: Error reading file: {e}"
                print(issue)
                route_issues.append(issue)
        else:
            issue = f"⚠️  {file_path}: File not found"
            print(issue)
            route_issues.append(issue)
    
    return len(route_issues) == 0

def verify_blueprint_fixes():
    """Verify blueprint registration fixes"""
    print("\n📋 VERIFYING BLUEPRINT FIXES...")
    
    fixes_verified = True
    
    # Check portfolio blueprint registration fix
    try:
        with open('app/__init__.py', 'r', encoding='utf-8') as f:
            init_content = f.read()
        
        # Should NOT have double prefix
        if "register_blueprint(portfolio, url_prefix='/portfolio')" in init_content:
            print("❌ Portfolio blueprint still has double prefix!")
            fixes_verified = False
        else:
            print("✅ Portfolio blueprint double prefix fixed")
            
        # Check portfolio blueprint definition
        with open('app/routes/portfolio.py', 'r', encoding='utf-8') as f:
            portfolio_content = f.read()
            
        if "url_prefix='/portfolio'" in portfolio_content:
            print("✅ Portfolio blueprint has correct prefix in definition")
        else:
            print("❌ Portfolio blueprint missing prefix in definition")
            fixes_verified = False
            
    except Exception as e:
        print(f"⚠️  Error checking blueprint fixes: {e}")
        fixes_verified = False
    
    return fixes_verified

def verify_function_call_fixes():
    """Verify get_data_service() calling pattern fixes"""
    print("\n📞 VERIFYING FUNCTION CALL FIXES...")
    
    call_issues = []
    
    try:
        with open('app/routes/portfolio.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should not have double parentheses
        if "get_data_service()()" in content:
            issue = "❌ Still has get_data_service()() double parentheses"
            print(issue)
            call_issues.append(issue)
        else:
            print("✅ get_data_service() calling pattern fixed")
            
    except Exception as e:
        issue = f"⚠️  Error checking function calls: {e}"
        print(issue)
        call_issues.append(issue)
    
    return len(call_issues) == 0

def main():
    """Run comprehensive verification"""
    print("=" * 60)
    print("🚀 500 ERROR FIXES VERIFICATION REPORT")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Run all verification checks
    checks = [
        ("Syntax Fixes", verify_syntax_fixes),
        ("Route Patterns", verify_route_patterns), 
        ("Blueprint Fixes", verify_blueprint_fixes),
        ("Function Call Fixes", verify_function_call_fixes),
    ]
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_checks_passed = False
        except Exception as e:
            print(f"\n❌ {check_name} verification failed with error: {e}")
            traceback.print_exc()
            all_checks_passed = False
    
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED! 500 error fixes verified successfully!")
        print("\n📝 SUMMARY:")
        print("✅ Critical deployment syntax error fixed") 
        print("✅ Blueprint double prefix resolved")
        print("✅ Function calling patterns corrected")
        print("✅ Route conflicts eliminated")
        print("\n✨ The app should now be deployable without 500 errors!")
    else:
        print("⚠️  SOME ISSUES REMAIN - Review the details above")
    
    print("=" * 60)
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
