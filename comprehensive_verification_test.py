#!/usr/bin/env python3
"""
Comprehensive verification test for all the user's reported issues.
This test checks that all fixes have been properly implemented.
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_css_fixes():
    """Test that CSS fixes are in place"""
    print("🎨 Testing CSS fixes...")
    
    css_file = os.path.join(current_dir, 'app', 'static', 'css', 'master-styling-fixes.css')
    
    if not os.path.exists(css_file):
        print("❌ master-styling-fixes.css not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Check for specific fixes
    checks = [
        ('Card header background fix', '.card-header' in css_content and 'background-color: #222222' in css_content),
        ('Gradient removal', '.bg-gradient' in css_content and 'background' in css_content),
        ('Bootstrap icon color fix', '.bi' in css_content and 'color: inherit' in css_content)
    ]
    
    all_passed = True
    for check_name, passed in checks:
        if passed:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ❌ {check_name}")
            all_passed = False
    
    return all_passed

def test_base_html_changes():
    """Test that base.html has been updated with CSS and homepage changes"""
    print("🏠 Testing base.html changes...")
    
    base_html = os.path.join(current_dir, 'app', 'templates', 'base.html')
    
    if not os.path.exists(base_html):
        print("❌ base.html not found")
        return False
    
    with open(base_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check for CSS inclusion
    css_included = 'master-styling-fixes.css' in html_content
    cache_busting = '?v=' in html_content or 'timestamp' in html_content.lower()
    
    print(f"  {'✓' if css_included else '❌'} master-styling-fixes.css included")
    print(f"  {'✓' if cache_busting else '❌'} Cache busting present")
    
    return css_included

def test_main_py_homepage_redirect():
    """Test that main.py has homepage redirect for logged-in users"""
    print("🔀 Testing homepage redirect...")
    
    main_py = os.path.join(current_dir, 'main.py')
    
    if not os.path.exists(main_py):
        print("❌ main.py not found")
        return False
    
    with open(main_py, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Check for redirect logic
    redirect_present = ('redirect' in main_content and 
                       'stocks' in main_content and 
                       'current_user.is_authenticated' in main_content)
    
    print(f"  {'✓' if redirect_present else '❌'} Homepage redirect for logged-in users")
    
    return redirect_present

def test_recommendation_template():
    """Test that star/bell buttons have been removed from recommendation.html"""
    print("⭐ Testing star/bell button removal...")
    
    rec_template = os.path.join(current_dir, 'app', 'templates', 'recommendation.html')
    
    if not os.path.exists(rec_template):
        print("❌ recommendation.html not found")
        return False
    
    with open(rec_template, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Check that star and bell buttons are NOT present
    star_removed = 'bi-star' not in template_content
    bell_removed = 'bi-bell' not in template_content
    
    print(f"  {'✓' if star_removed else '❌'} Star buttons removed")
    print(f"  {'✓' if bell_removed else '❌'} Bell buttons removed")
    
    return star_removed and bell_removed

def test_analysis_routes():
    """Test that all analysis routes exist"""
    print("📊 Testing analysis routes...")
    
    analysis_py = os.path.join(current_dir, 'app', 'routes', 'analysis.py')
    
    if not os.path.exists(analysis_py):
        print("❌ analysis.py not found")
        return False
    
    with open(analysis_py, 'r', encoding='utf-8') as f:
        routes_content = f.read()
    
    # Check for all the new routes
    required_routes = [
        'portfolio-tips',
        'risk-analysis', 
        'peer-comparison',
        'options-screener',
        'dividend-calendar',
        'earnings-calendar'
    ]
    
    all_routes_present = True
    for route in required_routes:
        if f"'{route}'" in routes_content or f'"{route}"' in routes_content:
            print(f"  ✓ {route} route found")
        else:
            print(f"  ❌ {route} route missing")
            all_routes_present = False
    
    return all_routes_present

def test_analysis_templates():
    """Test that all analysis templates exist"""
    print("📄 Testing analysis templates...")
    
    templates_dir = os.path.join(current_dir, 'app', 'templates', 'analysis')
    
    required_templates = [
        'portfolio_tips.html',
        'risk_analysis.html',
        'peer_comparison.html', 
        'options_screener.html',
        'dividend_calendar.html',
        'earnings_calendar.html'
    ]
    
    all_templates_present = True
    for template in required_templates:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"  ✓ {template} exists")
        else:
            print(f"  ❌ {template} missing")
            all_templates_present = False
    
    return all_templates_present

def main():
    """Run all tests and report results"""
    print("🧪 Running comprehensive verification test...")
    print("=" * 60)
    
    tests = [
        ("CSS fixes", test_css_fixes),
        ("Base HTML changes", test_base_html_changes),
        ("Homepage redirect", test_main_py_homepage_redirect),
        ("Recommendation template", test_recommendation_template),
        ("Analysis routes", test_analysis_routes),
        ("Analysis templates", test_analysis_templates)
    ]
    
    results = []
    for test_name, test_func in tests:
        print()
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📋 FINAL RESULTS:")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! All user issues have been resolved.")
    else:
        print("⚠️ Some tests failed. Please review the results above.")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
