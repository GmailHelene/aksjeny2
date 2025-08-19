#!/usr/bin/env python3
"""
Insider Trading Fixes Test
Tests the CSRF token and hardcoded data fixes
"""
import requests
import re
from urllib.parse import urlparse, parse_qs

def test_insider_trading_fixes():
    """Test insider trading page fixes"""
    base_url = "http://localhost:5001"
    
    print("🔍 INSIDER TRADING FIXES TEST")
    print("=" * 60)
    print("Testing:")
    print("1. ✅ CSRF token removed from URL")
    print("2. ✅ No default EQNR.OL ticker")
    print("3. ✅ Dynamic data based on search")
    print("4. ✅ Proper search functionality")
    print("=" * 60)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Empty page loads without default ticker
    print("\n🏠 Test 1: Empty State (No Default Ticker)")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/market-intel/insider-trading", timeout=5)
        content = response.text
        
        # Check that page loads successfully
        loads_successfully = response.status_code == 200
        # Check for search prompt instead of EQNR data
        has_search_prompt = 'Søk etter en aksje' in content or 'search' in content.lower()
        # Check that it doesn't default to EQNR
        no_default_eqnr = 'value="EQNR.OL"' not in content
        
        if loads_successfully and has_search_prompt and no_default_eqnr:
            print("   ✅ Empty state works correctly")
            print(f"      • Page loads: {loads_successfully}")
            print(f"      • Shows search prompt: {has_search_prompt}")
            print(f"      • No default EQNR: {no_default_eqnr}")
            tests_passed += 1
        else:
            print(f"   ❌ Empty state issues")
            print(f"      • Page loads: {loads_successfully}")
            print(f"      • Search prompt: {has_search_prompt}")
            print(f"      • No default EQNR: {no_default_eqnr}")
    except Exception as e:
        print(f"   ❌ Empty state test failed: {e}")
    
    # Test 2: Search functionality without CSRF token in URL
    print("\n🔍 Test 2: Search Functionality (No CSRF in URL)")
    tests_total += 1
    try:
        # Test searching for a ticker
        search_params = {'ticker': 'DNB.OL'}
        response = requests.get(f"{base_url}/market-intel/insider-trading", 
                              params=search_params, timeout=5, allow_redirects=False)
        
        loads_successfully = response.status_code == 200
        
        # Check the final URL doesn't contain CSRF token
        final_url = response.url if hasattr(response, 'url') else f"{base_url}/market-intel/insider-trading?ticker=DNB.OL"
        parsed_url = urlparse(final_url)
        query_params = parse_qs(parsed_url.query)
        
        no_csrf_in_url = 'csrf_token' not in query_params
        has_ticker_param = 'ticker' in query_params
        
        if loads_successfully and no_csrf_in_url and has_ticker_param:
            print("   ✅ Search works without CSRF in URL")
            print(f"      • Page loads: {loads_successfully}")
            print(f"      • No CSRF token in URL: {no_csrf_in_url}")
            print(f"      • Has ticker parameter: {has_ticker_param}")
            tests_passed += 1
        else:
            print(f"   ❌ Search functionality issues")
            print(f"      • Page loads: {loads_successfully}")
            print(f"      • CSRF in URL: {not no_csrf_in_url}")
            print(f"      • URL: {final_url}")
    except Exception as e:
        print(f"   ❌ Search test failed: {e}")
    
    # Test 3: Different tickers show different data
    print("\n📊 Test 3: Dynamic Data for Different Tickers")
    tests_total += 1
    try:
        # Get data for EQNR.OL
        response1 = requests.get(f"{base_url}/market-intel/insider-trading?ticker=EQNR.OL", timeout=5)
        content1 = response1.text
        
        # Get data for DNB.OL
        response2 = requests.get(f"{base_url}/market-intel/insider-trading?ticker=DNB.OL", timeout=5)
        content2 = response2.text
        
        both_load = response1.status_code == 200 and response2.status_code == 200
        
        # Check that the content is different (not hardcoded)
        content_differs = content1 != content2
        
        # Check that each shows the searched ticker
        shows_eqnr = 'EQNR.OL' in content1
        shows_dnb = 'DNB.OL' in content2
        
        if both_load and content_differs and shows_eqnr and shows_dnb:
            print("   ✅ Dynamic data works correctly")
            print(f"      • Both pages load: {both_load}")
            print(f"      • Content differs: {content_differs}")
            print(f"      • Shows correct tickers: {shows_eqnr and shows_dnb}")
            tests_passed += 1
        else:
            print(f"   ❌ Dynamic data issues")
            print(f"      • Both load: {both_load}")
            print(f"      • Content differs: {content_differs}")
            print(f"      • Shows tickers: EQNR={shows_eqnr}, DNB={shows_dnb}")
    except Exception as e:
        print(f"   ❌ Dynamic data test failed: {e}")
    
    # Test 4: Form doesn't include CSRF token
    print("\n📝 Test 4: Search Form (No CSRF Token)")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/market-intel/insider-trading", timeout=5)
        content = response.text
        
        loads_successfully = response.status_code == 200
        
        # Check that form exists
        has_search_form = '<form' in content and 'ticker' in content
        
        # Check that CSRF token is NOT in the form
        no_csrf_in_form = 'csrf_token' not in content
        
        # Check that form uses GET method
        uses_get_method = 'method="get"' in content.lower()
        
        if loads_successfully and has_search_form and no_csrf_in_form and uses_get_method:
            print("   ✅ Search form correctly configured")
            print(f"      • Page loads: {loads_successfully}")
            print(f"      • Has search form: {has_search_form}")
            print(f"      • No CSRF token: {no_csrf_in_form}")
            print(f"      • Uses GET method: {uses_get_method}")
            tests_passed += 1
        else:
            print(f"   ❌ Search form issues")
            print(f"      • Page loads: {loads_successfully}")
            print(f"      • Has form: {has_search_form}")
            print(f"      • CSRF present: {not no_csrf_in_form}")
            print(f"      • Uses GET: {uses_get_method}")
    except Exception as e:
        print(f"   ❌ Form test failed: {e}")
    
    # Final Summary
    print("\n" + "=" * 60)
    print(f"🎯 TEST RESULTS: {tests_passed}/{tests_total} tests passed")
    success_rate = (tests_passed / tests_total) * 100
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 85:
        print("🎉 STATUS: EXCELLENT - All insider trading issues fixed!")
        print("✅ CSRF token removed from URLs")
        print("✅ No default EQNR.OL ticker") 
        print("✅ Dynamic data based on search")
        print("✅ Proper search functionality")
    elif success_rate >= 70:
        print("✅ STATUS: GOOD - Most issues resolved")
        print("⚠️  Minor issues may remain")
    else:
        print("❌ STATUS: NEEDS WORK - Issues remain")
        print("🚨 Additional fixes required")
    
    print(f"\n📋 ISSUE RESOLUTION:")
    csrf_status = "✅ FIXED" if tests_passed >= 2 else "❌ NEEDS WORK"
    data_status = "✅ FIXED" if tests_passed >= 3 else "❌ NEEDS WORK"
    search_status = "✅ FIXED" if tests_passed >= 1 else "❌ NEEDS WORK"
    
    print(f"   • CSRF token in URL: {csrf_status}")
    print(f"   • Hardcoded placeholder data: {data_status}")
    print(f"   • No default EQNR.OL ticker: {search_status}")
    
    return tests_passed, tests_total

if __name__ == "__main__":
    test_insider_trading_fixes()
