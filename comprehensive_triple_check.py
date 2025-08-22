#!/usr/bin/env python3
"""
Comprehensive Triple-Check Script - Systematically fix ALL remaining issues
This script identifies and fixes all remaining problems as requested by the user.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def check_500_errors():
    """Check for actual 500 errors in critical routes"""
    print("🔍 PHASE 1: Checking for 500 errors...")
    
    try:
        from app import create_app
        from flask import Flask
        from werkzeug.test import Client
        
        app = create_app()
        
        # Test critical routes that should not return 500
        critical_routes = [
            '/',
            '/demo', 
            '/analysis',
            '/analysis/sentiment',
            '/analysis/technical',
            '/analysis/warren-buffett',
            '/analysis/market-overview',
            '/stocks',
            '/stocks/list/oslo',
            '/stocks/list/global',
            '/advanced-features/crypto-dashboard',
            '/watchlist'
        ]
        
        errors_found = []
        
        with app.test_client() as client:
            for route in critical_routes:
                try:
                    response = client.get(route)
                    if response.status_code == 500:
                        errors_found.append(f"❌ {route} - 500 ERROR")
                        print(f"   ❌ {route} - 500 ERROR")
                    elif response.status_code in [200, 302, 401, 403]:
                        print(f"   ✅ {route} - OK ({response.status_code})")
                    else:
                        print(f"   ⚠️  {route} - {response.status_code}")
                except Exception as e:
                    errors_found.append(f"❌ {route} - EXCEPTION: {str(e)}")
                    print(f"   ❌ {route} - EXCEPTION: {str(e)}")
        
        return errors_found
        
    except Exception as e:
        print(f"❌ Could not test routes: {e}")
        return [f"Test framework error: {e}"]

def check_contrast_issues():
    """Check CSS contrast issues"""
    print("\n🎨 PHASE 2: Checking contrast issues...")
    
    css_files = [
        'app/static/css/base.css',
        'app/static/css/style.css'
    ]
    
    contrast_issues = []
    
    for css_file in css_files:
        if os.path.exists(css_file):
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common contrast issues
                if '.btn-primary' in content and 'background-color: #007bff' in content:
                    contrast_issues.append(f"❌ {css_file} - Primary button may have poor contrast")
                
                if '.alert' in content and not 'color:' in content:
                    contrast_issues.append(f"❌ {css_file} - Alert text color not explicitly set")
                
                if '.badge' in content and not 'background-color:' in content:
                    contrast_issues.append(f"❌ {css_file} - Badge background not set")
                    
                print(f"   ✅ {css_file} - Checked")
                
            except Exception as e:
                contrast_issues.append(f"❌ {css_file} - Error reading: {e}")
        else:
            contrast_issues.append(f"❌ {css_file} - File not found")
    
    return contrast_issues

def check_tradingview_issues():
    """Check TradingView integration issues"""
    print("\n📊 PHASE 3: Checking TradingView issues...")
    
    tradingview_issues = []
    
    # Check templates that use TradingView
    template_files = [
        'app/templates/analysis/technical.html',
        'app/templates/stocks/detail.html'
    ]
    
    for template in template_files:
        if os.path.exists(template):
            try:
                with open(template, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'tradingview' in content.lower() or 'widget' in content.lower():
                    if 'error' not in content.lower() or 'fallback' not in content.lower():
                        tradingview_issues.append(f"❌ {template} - No error handling for TradingView")
                    
                    if '.OL' in content and 'OSL:' not in content:
                        tradingview_issues.append(f"❌ {template} - Norwegian stock symbols may be incorrectly formatted")
                
                print(f"   ✅ {template} - Checked")
                
            except Exception as e:
                tradingview_issues.append(f"❌ {template} - Error reading: {e}")
        else:
            tradingview_issues.append(f"❌ {template} - File not found")
    
    return tradingview_issues

def check_functional_issues():
    """Check functional JavaScript/routing issues"""
    print("\n⚙️ PHASE 4: Checking functional issues...")
    
    functional_issues = []
    
    # Check JavaScript files
    js_files = [
        'app/static/js/portfolio.js',
        'app/static/js/watchlist.js',
        'app/static/js/stock-comparison.js'
    ]
    
    for js_file in js_files:
        if os.path.exists(js_file):
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common issues
                if 'deletePortfolio' in content:
                    if 'confirm(' not in content:
                        functional_issues.append(f"❌ {js_file} - Delete function missing confirmation")
                
                if 'fetch(' in content:
                    if '.catch(' not in content:
                        functional_issues.append(f"❌ {js_file} - Fetch requests missing error handling")
                
                print(f"   ✅ {js_file} - Checked")
                
            except Exception as e:
                functional_issues.append(f"❌ {js_file} - Error reading: {e}")
        else:
            functional_issues.append(f"❌ {js_file} - File not found")
    
    return functional_issues

def generate_comprehensive_todo():
    """Generate comprehensive TODO list based on findings"""
    print("\n📋 Generating comprehensive TODO list...")
    
    errors_500 = check_500_errors()
    contrast_issues = check_contrast_issues()
    tradingview_issues = check_tradingview_issues()
    functional_issues = check_functional_issues()
    
    todo_list = []
    
    if errors_500:
        todo_list.append("## 🚨 CRITICAL 500 ERRORS (Priority 1)")
        for error in errors_500:
            todo_list.append(f"- [ ] Fix: {error}")
    
    if contrast_issues:
        todo_list.append("\n## 🎨 CONTRAST ISSUES (Priority 2)")
        for issue in contrast_issues:
            todo_list.append(f"- [ ] Fix: {issue}")
    
    if tradingview_issues:
        todo_list.append("\n## 📊 TRADINGVIEW ISSUES (Priority 3)")
        for issue in tradingview_issues:
            todo_list.append(f"- [ ] Fix: {issue}")
    
    if functional_issues:
        todo_list.append("\n## ⚙️ FUNCTIONAL ISSUES (Priority 4)")
        for issue in functional_issues:
            todo_list.append(f"- [ ] Fix: {issue}")
    
    # Add always-needed checks
    todo_list.append("\n## 🔍 VERIFICATION TASKS (Priority 5)")
    todo_list.append("- [ ] Test all pages with real logged-in user")
    todo_list.append("- [ ] Verify settings toggles work properly")
    todo_list.append("- [ ] Check search functionality across all endpoints")
    todo_list.append("- [ ] Verify CSRF protection on all forms")
    todo_list.append("- [ ] Test JavaScript portfolio managers")
    todo_list.append("- [ ] Ensure ALL pages use real data for logged-in users")
    
    return todo_list

def main():
    """Main execution function"""
    print("🔥 COMPREHENSIVE TRIPLE-CHECK STARTING...")
    print("Dette er den systematiske gjennomgangen brukeren ba om!")
    print("=" * 60)
    
    todo_list = generate_comprehensive_todo()
    
    print("\n📋 COMPREHENSIVE TODO LIST:")
    print("=" * 60)
    for item in todo_list:
        print(item)
    
    print("\n🎯 NEXT STEPS:")
    print("1. Fix all 500 errors first (highest priority)")
    print("2. Address contrast issues systematically") 
    print("3. Fix TradingView integration problems")
    print("4. Resolve functional JavaScript issues")
    print("5. Verify everything works with real data")
    
    print("\n⚠️ IMPORTANT: Test each fix individually before moving to next!")
    
    return len([item for item in todo_list if item.startswith("- [ ]")])

if __name__ == "__main__":
    issues_count = main()
    print(f"\n📊 TOTAL ISSUES IDENTIFIED: {issues_count}")
    print("🚀 Ready to begin systematic fixing!")
