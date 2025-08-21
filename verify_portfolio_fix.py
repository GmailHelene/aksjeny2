#!/usr/bin/env python3
"""
Portfolio Navigation Fix Verification
=====================================

This script verifies that the portfolio navigation BuildError has been fixed
by checking that all navigation templates use the correct endpoint.
"""

import os
import re

def verify_navigation_fixes():
    """Verify all navigation templates use correct portfolio endpoints"""
    
    print("🔍 Verifying Portfolio Navigation Fixes")
    print("=" * 50)
    
    # Files to check
    template_files = [
        "app/templates/base.html",
        "app/templates/base_clean.html"
    ]
    
    issues_found = []
    fixes_confirmed = []
    
    for template_file in template_files:
        if os.path.exists(template_file):
            print(f"\n📄 Checking: {template_file}")
            
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for problematic portfolio.view_portfolio in navigation
            problematic_patterns = [
                r"url_for\(['\"]portfolio\.view_portfolio['\"].*\)",
                r"href.*portfolio\.view_portfolio.*>.*Portefølje"
            ]
            
            for pattern in problematic_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    issues_found.append(f"{template_file}: Found problematic pattern: {matches}")
            
            # Check for correct portfolio.index usage
            correct_patterns = [
                r"url_for\(['\"]portfolio\.index['\"].*\)",
            ]
            
            for pattern in correct_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    fixes_confirmed.append(f"{template_file}: ✅ Uses portfolio.index: {len(matches)} instances")
                    
        else:
            issues_found.append(f"❌ Template file not found: {template_file}")
    
    # Check portfolio route exists
    portfolio_route_file = "app/routes/portfolio.py"
    if os.path.exists(portfolio_route_file):
        print(f"\n📄 Checking: {portfolio_route_file}")
        
        with open(portfolio_route_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for the index route
        if "@portfolio.route('/')" in content and "def index():" in content:
            fixes_confirmed.append("✅ Portfolio index route exists and is properly defined")
        else:
            issues_found.append("❌ Portfolio index route not found or improperly defined")
    else:
        issues_found.append("❌ Portfolio routes file not found")
    
    # Print results
    print("\n" + "=" * 50)
    print("🎯 VERIFICATION RESULTS")
    print("=" * 50)
    
    if fixes_confirmed:
        print("\n✅ FIXES CONFIRMED:")
        for fix in fixes_confirmed:
            print(f"   {fix}")
    
    if issues_found:
        print("\n❌ ISSUES FOUND:")
        for issue in issues_found:
            print(f"   {issue}")
    else:
        print("\n🎉 NO ISSUES FOUND!")
    
    # Overall status
    print(f"\n📊 SUMMARY:")
    print(f"   Fixes confirmed: {len(fixes_confirmed)}")
    print(f"   Issues remaining: {len(issues_found)}")
    
    if len(issues_found) == 0:
        print("\n🚀 PORTFOLIO NAVIGATION FIX: COMPLETE ✅")
        print("   → Users should now be able to log in without BuildError")
        print("   → Portfolio navigation should work from main menu")
        print("   → Ready for deployment")
    else:
        print("\n⚠️  PORTFOLIO NAVIGATION FIX: INCOMPLETE")
        print("   → Additional fixes needed before deployment")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    success = verify_navigation_fixes()
    exit(0 if success else 1)
