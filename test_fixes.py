#!/usr/bin/env python3
"""
Quick Test Script for Fixed Issues
=================================

Test the fixes applied to:
1. Stock details charts and styling
2. Price alerts creation

Author: GitHub Copilot
Date: August 29, 2025
"""

import requests
import sys
from datetime import datetime

def test_stock_details_page():
    """Test stock details page loading"""
    print("\n🔍 Testing Stock Details Page...")
    
    try:
        # Test the GOOGL details page
        response = requests.get('http://localhost:5002/stocks/details/GOOGL', timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            checks = {
                "Page loads successfully": True,
                "Contains TradingView chart container": 'tradingview_widget' in content,
                "Has key metrics card with ID": 'key-metrics-card' in content,
                "Contains chart loading indicator": 'chart-loading' in content or 'loading' in content,
                "Has technical analysis tab": 'technical-tab' in content,
                "Contains proper tab structure": 'nav-tabs' in content
            }
            
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"  {status} {check}")
            
            all_passed = all(checks.values())
            
            if all_passed:
                print("✅ Stock details page test PASSED")
            else:
                print("❌ Stock details page test FAILED")
            
            return all_passed
        else:
            print(f"❌ Stock details page returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing stock details page: {e}")
        return False

def test_price_alerts_page():
    """Test price alerts creation page"""
    print("\n🔍 Testing Price Alerts Page...")
    
    try:
        # Test the price alerts create page
        response = requests.get('http://localhost:5002/price-alerts/create', timeout=10)
        
        if response.status_code in [200, 302]:  # 302 might be redirect to login
            if response.status_code == 302:
                print("  ℹ️  Page redirects to login (expected for unauthenticated users)")
                return True
            
            content = response.text
            
            checks = {
                "Page loads successfully": True,
                "Contains create form": 'form' in content.lower(),
                "Has symbol input": 'symbol' in content.lower() and 'input' in content.lower(),
                "Has target price input": 'target' in content.lower() and 'price' in content.lower(),
                "Contains alert type options": 'alert' in content.lower() and ('option' in content.lower() or 'select' in content.lower()),
                "Has submit functionality": 'submit' in content.lower() or 'button' in content.lower()
            }
            
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"  {status} {check}")
            
            all_passed = all(checks.values())
            
            if all_passed:
                print("✅ Price alerts page test PASSED")
            else:
                print("❌ Price alerts page test FAILED")
            
            return all_passed
        else:
            print(f"❌ Price alerts page returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing price alerts page: {e}")
        return False

def test_server_health():
    """Test if Flask server is responding"""
    print("\n🔍 Testing Server Health...")
    
    try:
        response = requests.get('http://localhost:5002/', timeout=5)
        if response.status_code in [200, 302, 404]:  # Any valid response
            print("✅ Flask server is responding")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print("❌ Cannot connect to Flask server (is it running?)")
        return False

def main():
    """Run all tests"""
    print("🧪 Quick Test for Stock Details & Price Alerts Fixes")
    print("=" * 50)
    
    tests = [
        ("Server Health", test_server_health),
        ("Stock Details Page", test_stock_details_page),
        ("Price Alerts Page", test_price_alerts_page)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        print("\n📌 What to test manually:")
        print("1. Open /stocks/details/GOOGL and check chart loading")
        print("2. Switch tabs and verify 'Nøkkeltall' only shows on overview")
        print("3. Log in and test price alert creation")
        print("4. Verify no empty RSI/MACD sections on technical tab")
    else:
        print("\n⚠️ Some tests failed.")
        print("Check server status and retry.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
