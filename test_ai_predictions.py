#!/usr/bin/env python3
"""Test script to check AI predictions functionality"""

import requests

def test_ai_predictions():
    """Test the AI predictions endpoint"""
    base_url = 'http://localhost:5001'
    
    # Create session and login
    session = requests.Session()
    
    # Register a test user
    register_data = {
        'username': 'aiuser',
        'email': 'ai@test.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }
    
    try:
        # Register
        resp = session.post(f'{base_url}/register', data=register_data)
        print(f"Register response: {resp.status_code}")
        
        # Login
        login_data = {
            'email': 'ai@test.com',
            'password': 'test123'
        }
        resp = session.post(f'{base_url}/login', data=login_data)
        print(f"Login response: {resp.status_code}")
        
        # Test AI predictions index
        resp = session.get(f'{base_url}/analysis/ai-predictions')
        print(f"AI predictions index response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ AI predictions index error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ AI predictions index working")
            
        # Test AI predictions for specific ticker
        resp = session.get(f'{base_url}/analysis/ai-predictions/AAPL')
        print(f"AI predictions for AAPL response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ AI predictions for ticker error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ AI predictions for ticker working")
            
    except Exception as e:
        print(f"Error testing: {e}")

if __name__ == '__main__':
    test_ai_predictions()
