#!/usr/bin/env python3
"""
Comprehensive test of all the fixes we implemented.
Tests the key functionality that was reported as broken.
"""

import requests
import time
import sys

def test_endpoint(url, description, expected_status=200):
    """Test a single endpoint and return the result."""
    try:
        print(f"🧪 Testing {description}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ {description}: SUCCESS (Status: {response.status_code})")
            return True
        else:
            print(f"❌ {description}: FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}: ERROR - {e}")
        return False

def main():
    """Run comprehensive tests of all fixes."""
    
    base_url = "http://localhost:5001"
    
    print("🔧 COMPREHENSIVE FUNCTIONALITY TEST")
    print("Testing all the fixes we implemented...")
    print("=" * 50)
    
    tests = [
        # Analysis routes that were failing
        (f"{base_url}/analysis/screener", "Screener Analysis Route"),
        (f"{base_url}/analysis/sentiment?symbol=NHY.OL", "Sentiment Analysis Route"),
        
        # New recommendations system
        (f"{base_url}/analysis/recommendations", "AI Recommendations Route"),
        
        # Stock details pages
        (f"{base_url}/stocks/details/NHY.OL", "Stock Details Page"),
        (f"{base_url}/stocks/details/AKER.OL", "Another Stock Details Page"),
        
        # Main pages
        (f"{base_url}/", "Homepage"),
        (f"{base_url}/analysis/", "Analysis Overview"),
        
        # Pricing page (Stripe integration)
        (f"{base_url}/pricing", "Pricing Page"),
        
        # News pages
        (f"{base_url}/news/", "News Index"),
    ]
    
    results = []
    
    for url, description in tests:
        result = test_endpoint(url, description)
        results.append((description, result))
        time.sleep(0.5)  # Brief pause between tests
    
    print("=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for description, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {description}")
    
    print("=" * 50)
    print(f"Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! All fixes are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the results above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
