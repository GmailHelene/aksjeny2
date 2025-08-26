#!/usr/bin/env python3
"""
Test script to verify that the reported 500 error routes are now fixed
"""
import requests
import sys
from datetime import datetime

def test_route(url, expected_status=200):
    """Test a single route and return the result"""
    try:
        print(f"Testing: {url}")
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"✅ SUCCESS: {url} is working correctly")
            return True
        else:
            print(f"❌ FAILED: {url} returned status {response.status_code}")
            if response.status_code == 500:
                print("500 Internal Server Error detected!")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Could not connect to {url}")
        print(f"Error details: {e}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR testing {url}: {e}")
        return False

def main():
    """Test the two reported problematic URLs"""
    print("Testing for 500 errors on reported URLs")
    print("=" * 50)
    print(f"Test Time: {datetime.now()}")
    print()
    
    # URLs that were reported to have 500 errors
    test_urls = [
        "https://aksjeradar.trade/market-intel/sector-analysis",
        "https://aksjeradar.trade/settings"
    ]
    
    results = []
    
    for url in test_urls:
        result = test_route(url)
        results.append((url, result))
        print()
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY:")
    print("=" * 50)
    
    all_passed = True
    for url, result in results:
        status = "✅ WORKING" if result else "❌ FAILED"
        print(f"{status}: {url}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED! Both routes are now working correctly.")
        print("The 500 errors have been fixed.")
    else:
        print("⚠️  Some routes are still failing.")
        print("Additional investigation may be needed.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
