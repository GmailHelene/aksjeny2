#!/usr/bin/env python3
"""Test script to check portfolio functionality"""

import requests

def test_portfolio():
    """Test the portfolio endpoint"""
    base_url = 'http://localhost:5001'
    
    # Create session and login
    session = requests.Session()
    
    # Register a test user
    register_data = {
        'username': 'portfoliotestuser',
        'email': 'portfolio@test.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }
    
    try:
        # Register
        resp = session.post(f'{base_url}/register', data=register_data)
        print(f"Register response: {resp.status_code}")
        
        # Login
        login_data = {
            'email': 'portfolio@test.com',
            'password': 'test123'
        }
        resp = session.post(f'{base_url}/login', data=login_data)
        print(f"Login response: {resp.status_code}")
        
        # Now test the portfolio endpoint
        resp = session.get(f'{base_url}/portfolio')
        print(f"Portfolio response: {resp.status_code}")
        
        if resp.status_code == 500:
            print("❌ 500 Error occurred")
            print("Response content:", resp.text[:500])
        elif resp.status_code == 200:
            print("✅ Portfolio endpoint working")
        else:
            print(f"Unexpected status: {resp.status_code}")
            
    except Exception as e:
        print(f"Error testing: {e}")

if __name__ == '__main__':
    test_portfolio()
