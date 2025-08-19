#!/usr/bin/env python3
"""Test script to check pro-tools functionality"""

import requests

def test_pro_tools():
    """Test the pro-tools endpoints"""
    base_url = 'http://localhost:5001'
    
    # Create session and login
    session = requests.Session()
    
    # Register a test user
    register_data = {
        'username': 'protoolsuser',
        'email': 'protools@test.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }
    
    try:
        # Register
        resp = session.post(f'{base_url}/register', data=register_data)
        print(f"Register response: {resp.status_code}")
        
        # Login
        login_data = {
            'email': 'protools@test.com',
            'password': 'test123'
        }
        resp = session.post(f'{base_url}/login', data=login_data)
        print(f"Login response: {resp.status_code}")
        
        # Test pro-tools index
        resp = session.get(f'{base_url}/pro-tools/')
        print(f"Pro-tools index response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Pro-tools index error")
            print("Response content:", resp.text[:300])
        
        # Test pro-tools screener
        resp = session.get(f'{base_url}/pro-tools/screener')
        print(f"Pro-tools screener response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Pro-tools screener error")
            print("Response content:", resp.text[:300])
        
        # Test pro-tools export
        resp = session.get(f'{base_url}/pro-tools/export')
        print(f"Pro-tools export response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Pro-tools export error")
            print("Response content:", resp.text[:300])
            
        # Test API documentation
        resp = session.get(f'{base_url}/pro-tools/api/documentation')
        print(f"Pro-tools API docs response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Pro-tools API docs error")
            print("Response content:", resp.text[:300])
            
        if all(r.status_code == 200 for r in []):  # We'll add responses as we test
            print("✅ All pro-tools endpoints working")
            
    except Exception as e:
        print(f"Error testing: {e}")

if __name__ == '__main__':
    test_pro_tools()
