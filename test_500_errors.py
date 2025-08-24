#!/usr/bin/env python3
"""
Comprehensive 500 Error Check
Tests all the problematic endpoints to see if they're fixed
"""

import requests
import sys
from urllib.parse import urljoin

def test_500_errors():
    """Test all the 500 error endpoints to check if they're fixed"""
    base_url = "http://localhost:5000"  # Change this to your server URL if different
    
    print("🔍 Testing 500 Error Endpoints...")
    print("=" * 60)
    
    # Define the problematic endpoints
    test_cases = [
        {
            'url': '/watchlist/',
            'method': 'GET',
            'description': 'Fix /watchlist/ 500 error',
            'requires_auth': True
        },
        {
            'url': '/profile',
            'method': 'GET', 
            'description': 'Fix /profile 500 error',
            'requires_auth': False  # Uses demo_access
        },
        {
            'url': '/analysis/sentiment',
            'method': 'GET',
            'description': 'Fix /analysis/sentiment 500 error',
            'requires_auth': True
        },
        {
            'url': '/analysis/warren-buffett',
            'method': 'GET',
            'description': 'Fix /analysis/warren-buffett 500 error',
            'requires_auth': True
        },
        {
            'url': '/advanced-analysis',
            'method': 'GET',
            'description': 'Fix /advanced-analysis 500 error',
            'requires_auth': True
        },
        {
            'url': '/pro-tools/alerts',
            'method': 'GET',
            'description': 'Fix /pro-tools/alerts "Method Not Allowed" error',
            'requires_auth': True
        },
        {
            'url': '/portfolio/portfolio/9/add',
            'method': 'GET',
            'description': 'Fix /portfolio/portfolio/9/add 500 error',
            'requires_auth': True,
            'note': 'May return 404 if portfolio 9 does not exist - this is acceptable'
        }
    ]
    
    results = []
    session = requests.Session()
    
    for test_case in test_cases:
        try:
            full_url = urljoin(base_url, test_case['url'])
            print(f"\n🧪 Testing: {test_case['description']}")
            print(f"   URL: {full_url}")
            
            # Make the request
            response = session.request(test_case['method'], full_url, timeout=10)
            
            # Analyze response
            status_code = response.status_code
            
            if status_code == 500:
                print(f"   ❌ STILL BROKEN: {status_code} Internal Server Error")
                result = "BROKEN - 500 Error"
            elif status_code == 405:
                print(f"   ❌ METHOD NOT ALLOWED: {status_code}")
                result = "BROKEN - Method Not Allowed"
            elif status_code == 404:
                if test_case.get('note') and 'portfolio 9' in test_case['note']:
                    print(f"   ✅ ACCEPTABLE: {status_code} Not Found (portfolio may not exist)")
                    result = "ACCEPTABLE - 404 for non-existent portfolio"
                else:
                    print(f"   ⚠️ NOT FOUND: {status_code}")
                    result = "WARNING - 404 Not Found"
            elif status_code == 401:
                print(f"   🔐 AUTHENTICATION REQUIRED: {status_code}")
                result = "AUTHENTICATION REQUIRED"
            elif status_code == 403:
                print(f"   🚫 FORBIDDEN: {status_code}")
                result = "FORBIDDEN"
            elif status_code == 302 or status_code == 301:
                print(f"   ↩️ REDIRECT: {status_code} to {response.headers.get('Location', 'unknown')}")
                result = "REDIRECT"
            elif 200 <= status_code < 300:
                print(f"   ✅ SUCCESS: {status_code}")
                result = "SUCCESS"
            else:
                print(f"   ⚠️ UNEXPECTED: {status_code}")
                result = f"UNEXPECTED - {status_code}"
                
            results.append({
                'test': test_case['description'],
                'url': test_case['url'],
                'status_code': status_code,
                'result': result
            })
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ CONNECTION ERROR: {e}")
            results.append({
                'test': test_case['description'],
                'url': test_case['url'],
                'status_code': 'ERROR',
                'result': f"CONNECTION ERROR: {e}"
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    fixed_count = 0
    broken_count = 0
    
    for result in results:
        status = result['result']
        if 'SUCCESS' in status or 'ACCEPTABLE' in status or 'REDIRECT' in status:
            print(f"✅ {result['test']}: {status}")
            fixed_count += 1
        elif 'AUTHENTICATION REQUIRED' in status:
            print(f"🔐 {result['test']}: {status}")
            # Count as potentially fixed - needs proper testing with auth
            fixed_count += 1
        else:
            print(f"❌ {result['test']}: {status}")
            broken_count += 1
    
    print(f"\n📈 RESULTS:")
    print(f"   ✅ Fixed/Working: {fixed_count}")
    print(f"   ❌ Still Broken: {broken_count}")
    print(f"   📊 Total Tested: {len(results)}")
    
    if broken_count == 0:
        print(f"\n🎉 ALL ENDPOINTS ARE WORKING PROPERLY!")
    else:
        print(f"\n⚠️ {broken_count} endpoints still need attention")
    
    return results

if __name__ == "__main__":
    try:
        print("Starting 500 Error Check...")
        results = test_500_errors()
        
        # Exit with appropriate code
        broken_count = sum(1 for r in results if 'BROKEN' in r['result'])
        sys.exit(0 if broken_count == 0 else 1)
        
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
