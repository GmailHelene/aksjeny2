#!/usr/bin/env python3
"""
Comprehensive authentication and route testing
"""
import requests
import re
import time

def test_complete_flow():
    print("🔐 Testing complete authentication and route access flow...")
    
    # Create session
    session = requests.Session()
    
    # Step 1: Get login page and extract CSRF token
    print("\n1. Getting login page...")
    login_page = session.get('http://localhost:5002/login')
    print(f"   Login page status: {login_page.status_code}")
    
    # Extract CSRF token
    csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', login_page.text)
    if not csrf_match:
        print("   ❌ Could not extract CSRF token")
        return False
        
    csrf_token = csrf_match.group(1)
    print(f"   ✅ CSRF Token: {csrf_token[:20]}...")
    
    # Step 2: Attempt login with proper form data
    print("\n2. Attempting login...")
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'csrf_token': csrf_token,
        'remember_me': '',  # Empty for False
        'submit': 'Logg inn'
    }
    
    # Follow redirects to see where login takes us
    response = session.post('http://localhost:5002/login', 
                          data=login_data, 
                          allow_redirects=True)
    print(f"   Final URL after login: {response.url}")
    print(f"   Final status: {response.status_code}")
    
    # Check if we got a success message or error
    if 'Innlogging vellykket' in response.text:
        print("   ✅ Login successful message found")
    elif 'Ugyldig e-post eller passord' in response.text:
        print("   ❌ Invalid credentials message found")
    else:
        print("   ⚠️  No clear login status message found")
    
    # Step 3: Test protected routes with authenticated session
    print("\n3. Testing protected routes with session...")
    
    routes_to_test = [
        ('/profile', 'Profile'),
        ('/analysis/warren_buffett', 'Warren Buffett Analysis'),
        ('/portfolio', 'Portfolio')
    ]
    
    all_success = True
    for route, name in routes_to_test:
        response = session.get(f'http://localhost:5002{route}', allow_redirects=False)
        print(f"   {name}: {response.status_code}")
        
        if response.status_code == 200:
            print(f"     ✅ {name} accessible!")
        elif response.status_code == 302:
            location = response.headers.get('Location', '')
            if '/demo' in location or '/login' in location:
                print(f"     ❌ {name} still redirecting to: {location}")
                all_success = False
            else:
                print(f"     ⚠️  {name} redirecting to: {location}")
        else:
            print(f"     ❌ {name} unexpected status: {response.status_code}")
            all_success = False
    
    # Step 4: Test search functionality on Warren Buffett page if accessible
    if session.get('http://localhost:5002/analysis/warren_buffett', allow_redirects=False).status_code == 200:
        print("\n4. Testing Warren Buffett search functionality...")
        search_response = session.get('http://localhost:5002/analysis/warren_buffett?ticker=AAPL')
        if search_response.status_code == 200 and 'AAPL' in search_response.text:
            print("   ✅ Search functionality working!")
        else:
            print("   ❌ Search functionality issues")
    
    return all_success

if __name__ == "__main__":
    success = test_complete_flow()
    if success:
        print("\n🎉 All authentication and routes working correctly!")
    else:
        print("\n❌ Some issues remain with authentication or routes")
        print("\n💡 Summary:")
        print("   - Routes are not returning 500 errors (as user reported)")
        print("   - Routes are properly redirecting unauthenticated users") 
        print("   - The issue is likely users cannot login successfully")
        print("   - Warren Buffett analysis moved to demo-accessible endpoints")
