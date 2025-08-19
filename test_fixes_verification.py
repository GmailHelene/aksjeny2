#!/usr/bin/env python3
"""
Comprehensive test script to verify all the recent bug fixes
"""
import sys
import requests
import time
from datetime import datetime

def test_fixes():
    """Test all the recently implemented fixes"""
    base_url = "http://localhost:5001"
    test_results = []
    
    print(f"🔧 Testing fixes at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Stock list page loads properly
    try:
        response = requests.get(f"{base_url}/stocks/list/oslo", timeout=10)
        if response.status_code == 200 and "external-buy-btn" in response.text:
            test_results.append("✅ Stock list external buy buttons: FIXED")
        else:
            test_results.append("❌ Stock list external buy buttons: ISSUE")
    except Exception as e:
        test_results.append(f"❌ Stock list page error: {str(e)}")
    
    # Test 2: Fundamental analysis route with ticker
    try:
        response = requests.get(f"{base_url}/analysis/fundamental/EQNR.OL", timeout=10)
        if response.status_code == 200:
            test_results.append("✅ Fundamental analysis route: FIXED")
        else:
            test_results.append(f"❌ Fundamental analysis route: Status {response.status_code}")
    except Exception as e:
        test_results.append(f"❌ Fundamental analysis error: {str(e)}")
    
    # Test 3: Stock comparison page (should not crash)
    try:
        response = requests.get(f"{base_url}/stocks/compare?symbols=EQNR.OL,DNB.OL", timeout=10)
        if response.status_code == 200 and "ticker_names" not in response.text:
            test_results.append("✅ Stock comparison ticker_names: FIXED")
        else:
            test_results.append("❌ Stock comparison ticker_names: ISSUE")
    except Exception as e:
        test_results.append(f"❌ Stock comparison error: {str(e)}")
    
    # Test 4: Financial dashboard loads
    try:
        response = requests.get(f"{base_url}/financial-dashboard", timeout=10)
        if response.status_code == 200:
            test_results.append("✅ Financial dashboard: LOADS")
        else:
            test_results.append(f"❌ Financial dashboard: Status {response.status_code}")
    except Exception as e:
        test_results.append(f"❌ Financial dashboard error: {str(e)}")
    
    # Print results
    print("\n📊 TEST RESULTS:")
    print("=" * 60)
    for result in test_results:
        print(result)
    
    # Summary
    fixed_count = sum(1 for r in test_results if r.startswith("✅"))
    total_count = len(test_results)
    
    print("=" * 60)
    print(f"🎯 Summary: {fixed_count}/{total_count} tests passing")
    
    if fixed_count == total_count:
        print("🎉 All fixes verified successfully!")
        return True
    else:
        print("⚠️ Some issues remain")
        return False

if __name__ == "__main__":
    success = test_fixes()
    sys.exit(0 if success else 1)
