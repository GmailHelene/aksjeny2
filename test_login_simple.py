#!/usr/bin/env python3
"""
Simple test script to verify authentication flow
"""
import requests
import re

def test_login_flow():
    print("🔐 Testing authentication flow...")
    
    # Create session
    session = requests.Session()
    
    # Step 1: Get login page and extract CSRF token
    print("Step 1: Getting login page...")
    login_page = session.get('http://localhost:5002/login')
    print(f"Login page status: {login_page.status_code}")
    
    # Extract CSRF token
    csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', login_page.text)
    if not csrf_match:
        print("❌ Could not extract CSRF token")
        return False
        
    csrf_token = csrf_match.group(1)
    print(f"✅ CSRF Token extracted: {csrf_token[:20]}...")
    
    # Step 2: Attempt login
    print("\nStep 2: Attempting login...")
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'csrf_token': csrf_token,
        'remember_me': False
    }
    
    response = session.post('http://localhost:5002/login', data=login_data, allow_redirects=False)
    print(f"Login response status: {response.status_code}")
    
    if response.status_code == 302:
        location = response.headers.get('Location', 'Unknown')
        print(f"✅ Redirected to: {location}")
        
        # Step 3: Test protected routes
        print("\nStep 3: Testing protected routes...")
        
        # Test profile
        profile_response = session.get('http://localhost:5002/profile', allow_redirects=False)
        print(f"Profile access: {profile_response.status_code}")
        
        # Test Warren Buffett analysis
        warren_response = session.get('http://localhost:5002/analysis/warren_buffett', allow_redirects=False)  
        print(f"Warren Buffett access: {warren_response.status_code}")
        
        # Test portfolio
        portfolio_response = session.get('http://localhost:5002/portfolio', allow_redirects=False)
        print(f"Portfolio access: {portfolio_response.status_code}")
        
        # If any return 200, authentication worked
        if any(r.status_code == 200 for r in [profile_response, warren_response, portfolio_response]):
            print("✅ Authentication working! At least one protected route returned 200")
            return True
        else:
            print("❌ Authentication failed - all protected routes redirected")
            return False
            
    else:
        print(f"❌ Login failed with status {response.status_code}")
        print(f"Response text: {response.text[:200]}...")
        return False

if __name__ == "__main__":
    test_login_flow()
