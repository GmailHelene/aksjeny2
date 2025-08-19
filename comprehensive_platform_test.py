#!/usr/bin/env python3
"""
Comprehensive platform test to identify all remaining issues
"""

import requests
import json
import time
from urllib.parse import urljoin

def test_platform_endpoints():
    """Test all major platform endpoints to identify issues"""
    base_url = "http://localhost:5000"
    
    # Test cases with expected behavior
    test_cases = [
        # Portfolio tests
        {
            "name": "Portfolio Page",
            "url": "/portfolio",
            "expected_status": [200, 302],  # 302 if not logged in
            "check_content": ["portfolio", "portefølje"]
        },
        
        # Sentiment Analysis tests  
        {
            "name": "TSLA Sentiment Analysis", 
            "url": "/analysis/sentiment?symbol=TSLA",
            "expected_status": [200, 302],
            "check_content": ["sentiment", "TSLA"]
        },
        
        {
            "name": "EQNR.OL Sentiment Analysis",
            "url": "/analysis/sentiment?symbol=EQNR.OL", 
            "expected_status": [200, 302],
            "check_content": ["sentiment", "EQNR"]
        },
        
        # Watchlist tests
        {
            "name": "Watchlist Page",
            "url": "/watchlist",
            "expected_status": [200, 302],
            "check_content": ["watchlist", "overvåkning"]
        },
        
        # Screener tests
        {
            "name": "Screener Results",
            "url": "/analysis/screener",
            "expected_status": [200, 302], 
            "check_content": ["screener", "søk"]
        },
        
        # Stock Details tests
        {
            "name": "TSLA Stock Details",
            "url": "/stocks/TSLA",
            "expected_status": [200, 302],
            "check_content": ["TSLA", "Tesla"]
        },
        
        {
            "name": "EQNR.OL Stock Details",
            "url": "/stocks/EQNR.OL",
            "expected_status": [200, 302], 
            "check_content": ["EQNR", "Equinor"]
        },
        
        # Translation tests
        {
            "name": "Language Switch Norwegian",
            "url": "/set_language/no",
            "expected_status": [200, 302],
            "check_content": []
        },
        
        {
            "name": "Language Switch English", 
            "url": "/set_language/en",
            "expected_status": [200, 302],
            "check_content": []
        },
        
        # API tests
        {
            "name": "Stock Info API - TSLA",
            "url": "/api/stock-info/TSLA",
            "expected_status": [200, 404, 500],
            "check_content": []
        },
        
        {
            "name": "Stock Info API - EQNR.OL",
            "url": "/api/stock-info/EQNR.OL", 
            "expected_status": [200, 404, 500],
            "check_content": []
        }
    ]
    
    results = []
    
    print("🧪 Starting Comprehensive Platform Tests\n")
    
    for test in test_cases:
        print(f"Testing: {test['name']}")
        
        try:
            url = urljoin(base_url, test['url'])
            response = requests.get(url, timeout=10, allow_redirects=False)
            
            result = {
                "name": test['name'],
                "url": test['url'],
                "status_code": response.status_code,
                "success": response.status_code in test['expected_status'],
                "content_length": len(response.text),
                "errors": []
            }
            
            # Check for specific content if specified
            if test['check_content']:
                content_found = any(content.lower() in response.text.lower() 
                                  for content in test['check_content'])
                if not content_found and response.status_code == 200:
                    result['errors'].append(f"Expected content not found: {test['check_content']}")
            
            # Check for error indicators in response
            error_indicators = ['500', 'error', 'exception', 'traceback', 'internal server error']
            if any(indicator in response.text.lower() for indicator in error_indicators):
                result['errors'].append("Error indicators found in response")
            
            # Status reporting
            if result['success'] and not result['errors']:
                print(f"  ✅ PASS - Status: {response.status_code}")
            else:
                print(f"  ❌ FAIL - Status: {response.status_code}")
                if result['errors']:
                    for error in result['errors']:
                        print(f"    - {error}")
            
            results.append(result)
            
        except requests.RequestException as e:
            print(f"  💥 REQUEST ERROR: {e}")
            results.append({
                "name": test['name'],
                "url": test['url'], 
                "status_code": None,
                "success": False,
                "content_length": 0,
                "errors": [f"Request failed: {e}"]
            })
        
        except Exception as e:
            print(f"  🔥 UNEXPECTED ERROR: {e}")
            results.append({
                "name": test['name'],
                "url": test['url'],
                "status_code": None, 
                "success": False,
                "content_length": 0,
                "errors": [f"Unexpected error: {e}"]
            })
        
        time.sleep(0.5)  # Brief pause between requests
        
    # Summary report
    print(f"\n📊 TEST SUMMARY")
    print(f"=" * 50)
    
    passed = sum(1 for r in results if r['success'] and not r['errors'])
    failed = len(results) - passed
    
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print(f"\n❌ FAILED TESTS:")
        for result in results:
            if not result['success'] or result['errors']:
                print(f"  - {result['name']}: {result['url']}")
                if result['errors']:
                    for error in result['errors']:
                        print(f"    * {error}")
    
    return results

def test_authenticated_functionality():
    """Test functionality that requires authentication"""
    print(f"\n🔐 Testing Authenticated Functionality")
    print(f"=" * 50)
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # First try to access portfolio without login
    try:
        response = session.get(f"{base_url}/portfolio")
        if response.status_code == 302:
            print("✅ Portfolio redirects when not authenticated")
        elif response.status_code == 200:
            print("⚠️  Portfolio accessible without authentication")
        else:
            print(f"❌ Unexpected portfolio response: {response.status_code}")
    except Exception as e:
        print(f"❌ Portfolio test failed: {e}")
    
    # Test watchlist access
    try:
        response = session.get(f"{base_url}/watchlist")
        if response.status_code == 302:
            print("✅ Watchlist redirects when not authenticated")
        elif response.status_code == 200:
            print("⚠️  Watchlist accessible without authentication")  
        else:
            print(f"❌ Unexpected watchlist response: {response.status_code}")
    except Exception as e:
        print(f"❌ Watchlist test failed: {e}")

if __name__ == "__main__":
    # Run comprehensive tests
    results = test_platform_endpoints()
    
    # Run authentication tests
    test_authenticated_functionality()
    
    # Save results to file
    with open('platform_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Detailed results saved to platform_test_results.json")
