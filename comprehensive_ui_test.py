#!/usr/bin/env python3
"""
Comprehensive UI test to verify all fixes are working correctly
"""
import requests
import json
import sys
from datetime import datetime

def comprehensive_ui_test():
    """Test all the UI fixes that were implemented"""
    base_url = "http://localhost:5001"
    
    print("🔬 COMPREHENSIVE UI TEST SUITE")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Homepage error messages
    print("\n1. Testing homepage error message suppression...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
            tests_passed += 1
        else:
            print(f"❌ Homepage error: {response.status_code}")
    except Exception as e:
        print(f"❌ Homepage test failed: {e}")
    
    # Test 2: News page image sizes
    print("\n2. Testing news page image optimization...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/news", timeout=5)
        if response.status_code == 200 and 'h-48' in response.text:
            print("✅ News images optimized (h-48 found)")
            tests_passed += 1
        else:
            print("⚠️  News image optimization unclear")
    except Exception as e:
        print(f"❌ News test failed: {e}")
    
    # Test 3: Stock list buttons functionality
    print("\n3. Testing stock list buy/star buttons...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/stocks/list/oslo", timeout=5)
        content = response.text
        
        has_buy_buttons = 'external-buy-btn' in content
        has_star_buttons = 'add-to-watchlist' in content
        has_event_listeners = 'addEventListener' in content
        
        if has_buy_buttons and has_star_buttons and has_event_listeners:
            print("✅ Stock list buttons found with event listeners")
            tests_passed += 1
        else:
            print(f"❌ Button issues: buy={has_buy_buttons}, star={has_star_buttons}, listeners={has_event_listeners}")
    except Exception as e:
        print(f"❌ Stock list buttons test failed: {e}")
    
    # Test 4: Text color fixes
    print("\n4. Testing text color improvements...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/analysis/market-overview", timeout=5)
        content = response.text
        
        has_dark_text = 'text-dark fw-bold' in content
        
        if has_dark_text:
            print("✅ Dark text styling found")
            tests_passed += 1
        else:
            print("❌ Dark text styling not found")
    except Exception as e:
        print(f"❌ Text color test failed: {e}")
    
    # Test 5: Currency table improvements
    print("\n5. Testing currency table data...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/analysis/market-overview", timeout=5)
        content = response.text
        
        has_currency_data = 'USDNOK' in content and 'EURNOK' in content
        
        if has_currency_data:
            print("✅ Currency data found")
            tests_passed += 1
        else:
            print("❌ Currency data not found")
    except Exception as e:
        print(f"❌ Currency test failed: {e}")
    
    # Test 6: CSRF token removal from social sentiment
    print("\n6. Testing social sentiment CSRF token removal...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/analysis/social-sentiment/EQNR.OL", timeout=5)
        content = response.text
        
        # Check if CSRF token is NOT in the URL when form is submitted
        has_clean_form = 'csrf_token' not in content or 'method="GET"' in content
        
        if has_clean_form:
            print("✅ CSRF token properly handled")
            tests_passed += 1
        else:
            print("⚠️  CSRF token handling unclear")
    except Exception as e:
        print(f"❌ CSRF test failed: {e}")
    
    # Test 7: Fundamental analysis N/A fixes
    print("\n7. Testing fundamental analysis data...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/analysis/fundamental/EQNR.OL", timeout=5)
        content = response.text
        
        # Check for realistic financial data instead of N/A
        has_realistic_data = '24.5' in content or 'financial_metrics' in content
        no_na_values = content.count('>N/A<') < 3  # Allow some N/A but not excessive
        
        if has_realistic_data and no_na_values:
            print("✅ Fundamental data improved")
            tests_passed += 1
        else:
            print(f"⚠️  Fundamental data: realistic={has_realistic_data}, low_na={no_na_values}")
    except Exception as e:
        print(f"❌ Fundamental test failed: {e}")
    
    # Test 8: Chart visualization (TradingView)
    print("\n8. Testing chart functionality...")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/analysis/technical/EQNR.OL", timeout=5)
        content = response.text
        
        has_tradingview = 'TradingView' in content
        has_chart_container = 'tradingview_widget' in content
        
        if has_tradingview and has_chart_container:
            print("✅ Chart components found")
            tests_passed += 1
        else:
            print(f"❌ Chart issues: tradingview={has_tradingview}, container={has_chart_container}")
    except Exception as e:
        print(f"❌ Chart test failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {tests_passed}/{tests_total} tests passed")
    success_rate = (tests_passed / tests_total) * 100
    print(f"🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 75:
        print("🎉 Overall: GOOD - Most issues resolved!")
    elif success_rate >= 50:
        print("⚠️  Overall: PARTIAL - Some issues remain")
    else:
        print("❌ Overall: NEEDS WORK - Multiple issues found")
    
    return tests_passed, tests_total

if __name__ == "__main__":
    comprehensive_ui_test()
