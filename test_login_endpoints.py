#!/usr/bin/env python3

import requests
import sys

def test_authenticated_endpoints():
    """Test endpoints that require authentication"""
    
    base_url = "https://aksjeradar.trade"
    session = requests.Session()
    
    print("🔐 Testing authenticated endpoints...")
    
    # Get CSRF token from login page
    login_page = session.get(f"{base_url}/auth/login")
    if login_page.status_code != 200:
        print(f"❌ Can't access login page: {login_page.status_code}")
        return False
    
    # Extract CSRF token from login form
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = None
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    if csrf_input:
        csrf_token = csrf_input.get('value')
    
    if not csrf_token:
        print("❌ Could not find CSRF token")
        return False
    
    print(f"✅ Got CSRF token: {csrf_token[:20]}...")
    
    # Login with test user credentials
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'csrf_token': csrf_token
    }
    
    login_response = session.post(f"{base_url}/auth/login", data=login_data)
    
    if login_response.status_code == 302:
        print("✅ Login successful (redirected)")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text[:500]}")
        return False
    
    # Test the problematic endpoints
    endpoints_to_test = [
        "/",
        "/stocks/list/currency", 
        "/stocks/list/crypto",
        "/stocks/details/EQNR.OL",
        "/analysis/warren-buffett?ticker=KO"
    ]
    
    results = {}
    
    for endpoint in endpoints_to_test:
        print(f"\n🧪 Testing {endpoint}...")
        response = session.get(f"{base_url}{endpoint}")
        results[endpoint] = {
            'status_code': response.status_code,
            'content_length': len(response.text),
            'has_error': '500' in response.text or 'Error' in response.text[:500]
        }
        
        if response.status_code == 200:
            print(f"✅ {endpoint}: {response.status_code} (Content: {len(response.text)} chars)")
            if 'Error' in response.text[:500] or '500' in response.text:
                print(f"⚠️  Warning: Error content detected in response")
        else:
            print(f"❌ {endpoint}: {response.status_code}")
    
    # Summary
    print("\n📊 Summary:")
    successful = 0
    for endpoint, result in results.items():
        status = "✅" if result['status_code'] == 200 and not result['has_error'] else "❌"
        print(f"{status} {endpoint}: {result['status_code']} ({result['content_length']} chars)")
        if result['status_code'] == 200 and not result['has_error']:
            successful += 1
    
    print(f"\n✅ {successful}/{len(endpoints_to_test)} endpoints working correctly")
    
    return successful == len(endpoints_to_test)

if __name__ == "__main__":
    try:
        success = test_authenticated_endpoints()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
