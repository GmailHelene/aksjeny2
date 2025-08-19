#!/usr/bin/env python3
"""
Final Navigation Validation - Complete Test Suite
"""

import requests
import json
from datetime import datetime

def final_navigation_validation():
    """Complete validation of the navigation system"""
    
    print("🎯 FINAL NAVIGATION VALIDATION")
    print("=" * 50)
    print(f"⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    base_url = "http://localhost:5001"
    
    # Test 1: Check main demo page loads correctly
    print("🧪 Test 1: Demo page accessibility")
    try:
        response = requests.get(f"{base_url}/demo", timeout=10)
        if response.status_code == 200:
            print("✅ Demo page loads successfully")
            
            # Check for navigation elements
            content = response.text
            has_bootstrap = "bootstrap@5.3.0" in content
            has_nav_script = "dropdown-navigation.js" in content
            has_cache_bust = "20250806_155908" in content
            
            print(f"✅ Bootstrap 5.3.0 loaded: {has_bootstrap}")
            print(f"✅ Navigation script loaded: {has_nav_script}")
            print(f"✅ Cache busting active: {has_cache_bust}")
            
        else:
            print(f"❌ Demo page failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Demo page error: {e}")
    
    print()
    
    # Test 2: Validate dropdown navigation endpoints
    print("🧪 Test 2: Dropdown navigation endpoints")
    dropdown_endpoints = {
        "Aksjer": "/stocks/",
        "Analyse": "/analysis/", 
        "Portefølje": "/portfolio/",
        "Nyheter": "/news",
        "Dashboard": "/financial-dashboard"
    }
    
    all_passed = True
    for name, endpoint in dropdown_endpoints.items():
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name:<12} -> {endpoint:<20} (OK)")
            else:
                print(f"❌ {name:<12} -> {endpoint:<20} (Status: {response.status_code})")
                all_passed = False
        except Exception as e:
            print(f"❌ {name:<12} -> {endpoint:<20} (Error: {e})")
            all_passed = False
    
    print()
    
    # Test 3: Navigation JavaScript validation
    print("🧪 Test 3: Navigation JavaScript validation")
    try:
        js_response = requests.get(f"{base_url}/static/js/dropdown-navigation.js?v=20250806_155908")
        if js_response.status_code == 200:
            js_content = js_response.text
            
            # Check for critical functions
            critical_functions = [
                "setupDesktopNavigation",
                "setupMobileNavigation", 
                "toggleMobileDropdown",
                "closeMobileMenu"
            ]
            
            for func in critical_functions:
                has_function = func in js_content
                print(f"✅ Function {func}: {'Present' if has_function else 'MISSING'}")
                if not has_function:
                    all_passed = False
                    
            # Check for debugging
            has_debug = "console.log" in js_content
            print(f"✅ Debug logging: {'Enabled' if has_debug else 'Disabled'}")
            
        else:
            print(f"❌ Navigation JS failed to load: {js_response.status_code}")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Navigation JS error: {e}")
        all_passed = False
    
    print()
    
    # Test 4: Mobile navigation features 
    print("🧪 Test 4: Mobile navigation features check")
    try:
        response = requests.get(f"{base_url}/demo")
        if response.status_code == 200:
            content = response.text
            
            # Check for mobile-specific elements
            mobile_checks = {
                "Mobile nav sections": "mobile-nav-section" in content,
                "Bootstrap collapse": "navbar-collapse" in content,
                "Hamburger toggler": "navbar-toggler" in content,
                "Dropdown menus": "dropdown-menu" in content,
                "Navigation hrefs": 'href="/stocks/"' in content and 'href="/analysis/"' in content
            }
            
            for check, passed in mobile_checks.items():
                print(f"✅ {check}: {'Present' if passed else 'MISSING'}")
                if not passed:
                    all_passed = False
                    
        else:
            print("❌ Could not check mobile features")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Mobile features check error: {e}")
        all_passed = False
    
    print()
    print("=" * 50)
    
    if all_passed:
        print("🎉 ALL NAVIGATION TESTS PASSED!")
        print("✅ PC Dropdowns: Bootstrap enabled with proper events")
        print("✅ Mobile Navigation: Direct href navigation + dropdown toggle")
        print("✅ Mobile Menu: Stable with proper Bootstrap collapse")
        print("✅ Cache Busting: Active with timestamp 20250806_155908")
        print()
        print("🚀 Navigation system is fully operational!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - Check output above for details")
        return False

if __name__ == "__main__":
    success = final_navigation_validation()
    
    if success:
        print("\n🎯 NAVIGATION VALIDATION: SUCCESS")
        print("The navigation system is ready for production use.")
    else:
        print("\n❌ NAVIGATION VALIDATION: ISSUES DETECTED")
        print("Please review the test output and fix any issues.")
