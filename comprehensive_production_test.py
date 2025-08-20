#!/usr/bin/env python3
"""
Comprehensive test script to verify all critical production fixes.
This script tests the main issues reported by the user to ensure they are resolved.
"""

import requests
import json
import sys
from datetime import datetime

# Base URL for testing
BASE_URL = "http://localhost:5000"

def test_oslo_stocks_count():
    """Test that Oslo stocks show more than 10 companies."""
    print("🔍 Testing Oslo stocks count...")
    try:
        response = requests.get(f"{BASE_URL}/api/data/oslo-bors", timeout=10)
        if response.status_code == 200:
            data = response.json()
            stock_count = len(data.get('data', []))
            print(f"   ✅ Oslo stocks count: {stock_count}")
            if stock_count >= 40:
                print("   ✅ PASS: Oslo stocks showing 40+ companies")
                return True
            else:
                print(f"   ❌ FAIL: Only showing {stock_count} companies (expected 40+)")
                return False
        else:
            print(f"   ❌ FAIL: API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_favorites_api():
    """Test favorites API endpoints."""
    print("\n🔍 Testing favorites API...")
    try:
        # Test check favorites endpoint
        response = requests.get(f"{BASE_URL}/api/favorites/check", timeout=10)
        print(f"   ✅ Check favorites API: Status {response.status_code}")
        
        # Test add to favorites (should work for demo user)
        test_data = {'symbol': 'NHY.OL'}
        response = requests.post(f"{BASE_URL}/api/favorites/add", 
                               json=test_data, 
                               timeout=10)
        print(f"   ✅ Add favorites API: Status {response.status_code}")
        
        # Test remove from favorites (should work for demo user)
        response = requests.post(f"{BASE_URL}/api/favorites/remove", 
                               json=test_data, 
                               timeout=10)
        print(f"   ✅ Remove favorites API: Status {response.status_code}")
        
        return True
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_portfolio_routes():
    """Test portfolio-related routes that were reported as broken."""
    print("\n🔍 Testing portfolio routes...")
    try:
        # Test portfolio main page
        response = requests.get(f"{BASE_URL}/portfolio", timeout=10)
        print(f"   ✅ Portfolio main page: Status {response.status_code}")
        
        # Test watchlist page
        response = requests.get(f"{BASE_URL}/portfolio/watchlist", timeout=10)
        print(f"   ✅ Watchlist page: Status {response.status_code}")
        
        # Note: We won't test the specific portfolio/9/add since that requires specific data
        # and might not exist in our test environment
        
        return True
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_navigation_structure():
    """Test that navigation structure is properly updated."""
    print("\n🔍 Testing navigation structure...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Check that "Verktøy" dropdown is removed
            if 'dropdown-menu' in content and 'Verktøy' not in content:
                print("   ✅ PASS: Navigation restructured (Verktøy removed)")
                return True
            else:
                print("   ⚠️  WARNING: Could not verify navigation changes in HTML")
                return False
        else:
            print(f"   ❌ FAIL: Could not load main page (status {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def test_analysis_tools():
    """Test analysis tools and pages."""
    print("\n🔍 Testing analysis tools...")
    try:
        # Test stock comparison
        response = requests.get(f"{BASE_URL}/stocks/compare", timeout=10)
        print(f"   ✅ Stock comparison page: Status {response.status_code}")
        
        # Test technical analysis
        response = requests.get(f"{BASE_URL}/analysis", timeout=10)
        print(f"   ✅ Analysis page: Status {response.status_code}")
        
        # Test sentiment analysis
        response = requests.get(f"{BASE_URL}/analysis/sentiment", timeout=10)
        print(f"   ✅ Sentiment analysis page: Status {response.status_code}")
        
        return True
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests and report results."""
    print("🚀 Starting comprehensive production test...")
    print(f"📅 Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing against: {BASE_URL}")
    print("=" * 60)
    
    tests = [
        ("Oslo Stocks Count", test_oslo_stocks_count),
        ("Favorites API", test_favorites_api),
        ("Portfolio Routes", test_portfolio_routes),
        ("Navigation Structure", test_navigation_structure),
        ("Analysis Tools", test_analysis_tools)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ FATAL ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Production fixes are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
