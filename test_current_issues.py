#!/usr/bin/env python3
"""
Test script for current functionality issues mentioned by user
"""
import requests
import json
import time

base_url = "http://localhost:5000"

def test_endpoint(method, endpoint, description, data=None, headers=None):
    """Test an endpoint and return result"""
    try:
        url = f"{base_url}{endpoint}"
        if headers is None:
            headers = {}
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        return {
            'description': description,
            'status_code': response.status_code,
            'success': response.status_code < 400,
            'content_length': len(response.content),
            'url': url
        }
    except Exception as e:
        return {
            'description': description,
            'error': str(e),
            'success': False,
            'url': url
        }

def main():
    print("🔍 TESTING CURRENT FUNCTIONALITY ISSUES")
    print("=" * 50)
    
    tests = [
        # Test 1: Norwegian market intelligence verification
        ('GET', '/norwegian-intel/oil-correlation', 'Oil price correlation analysis'),
        
        # Test 2: ROI calculator 
        ('GET', '/roi-kalkulator', 'ROI calculator page'),
        
        # Test 3: Analysis overview with new cards
        ('GET', '/analysis/', 'Analysis overview page with new cards'),
        
        # Test 4: Watchlist functionality
        ('GET', '/watchlist/', 'Watchlist index page'),
        
        # Test 5: Notification settings
        ('GET', '/notifications/settings', 'Notification settings page'),
        
        # Test 6: Price alerts creation
        ('GET', '/price-alerts/create', 'Price alerts creation page'),
        
        # Test 7: Stock details page (example)
        ('GET', '/stocks/details/TSLA', 'Stock details page for TSLA'),
        
        # Test 8: Recommendations page
        ('GET', '/analysis/recommendations', 'Analysis recommendations page'),
        
        # Test 9: Comparison page
        ('GET', '/stocks/compare', 'Stock comparison page'),
        
        # Test 10: Settings page  
        ('GET', '/settings', 'Main settings page'),
    ]
    
    results = []
    for method, endpoint, description in tests:
        print(f"\n🧪 Testing: {description}")
        result = test_endpoint(method, endpoint, description)
        results.append(result)
        
        if result.get('success'):
            print(f"   ✅ {result['status_code']} - {description}")
        else:
            print(f"   ❌ {result.get('status_code', 'ERROR')} - {description}")
            if 'error' in result:
                print(f"      Error: {result['error']}")
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    successful = sum(1 for r in results if r.get('success'))
    total = len(results)
    print(f"✅ {successful}/{total} tests passed")
    
    print("\n🔍 FAILED TESTS:")
    for result in results:
        if not result.get('success'):
            print(f"❌ {result['description']} - Status: {result.get('status_code', 'ERROR')}")
    
    # Save detailed results
    with open('current_issues_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed results saved to: current_issues_test_results.json")

if __name__ == "__main__":
    main()
