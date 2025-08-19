#!/usr/bin/env python3
"""Test script to check price alerts functionality"""

import requests

def test_price_alerts():
    """Test the price alerts endpoints"""
    base_url = 'http://localhost:5001'
    
    # Create session and login
    session = requests.Session()
    
    # Register a test user
    register_data = {
        'username': 'alertuser',
        'email': 'alerts@test.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }
    
    try:
        # Register
        resp = session.post(f'{base_url}/register', data=register_data)
        print(f"Register response: {resp.status_code}")
        
        # Login
        login_data = {
            'email': 'alerts@test.com',
            'password': 'test123'
        }
        resp = session.post(f'{base_url}/login', data=login_data)
        print(f"Login response: {resp.status_code}")
        
        # Test price alerts index
        resp = session.get(f'{base_url}/price-alerts/')
        print(f"Price alerts index response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Price alerts index error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Price alerts index working")
            
        # Test price alerts API
        resp = session.get(f'{base_url}/price-alerts/api/alerts')
        print(f"Price alerts API response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Price alerts API error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Price alerts API working")
            
        # Test creating a price alert (pro tools alerts)
        resp = session.get(f'{base_url}/pro-tools/alerts')
        print(f"Pro tools alerts response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Pro tools alerts error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Pro tools alerts working")
            
    except Exception as e:
        print(f"Error testing: {e}")

if __name__ == '__main__':
    test_price_alerts()
