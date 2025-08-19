#!/usr/bin/env python3
"""Test script to check insider trading functionality"""

import requests

def test_insider_trading():
    """Test the insider trading endpoints"""
    base_url = 'http://localhost:5001'
    
    # Create session and login
    session = requests.Session()
    
    # Register a test user
    register_data = {
        'username': 'insideruser',
        'email': 'insider@test.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }
    
    try:
        # Register
        resp = session.post(f'{base_url}/register', data=register_data)
        print(f"Register response: {resp.status_code}")
        
        # Login
        login_data = {
            'email': 'insider@test.com',
            'password': 'test123'
        }
        resp = session.post(f'{base_url}/login', data=login_data)
        print(f"Login response: {resp.status_code}")
        
        # Test insider trading index
        resp = session.get(f'{base_url}/insider-trading/')
        print(f"Insider trading index response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Insider trading index error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Insider trading index working")
            
        # Test insider trading API
        resp = session.get(f'{base_url}/insider-trading/api/latest')
        print(f"Insider trading API response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Insider trading API error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Insider trading API working")
            
        # Test insider trading search
        resp = session.get(f'{base_url}/insider-trading/search?symbol=AAPL')
        print(f"Insider trading search response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Insider trading search error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Insider trading search working")
            
    except Exception as e:
        print(f"Error testing: {e}")

if __name__ == '__main__':
    test_insider_trading()
