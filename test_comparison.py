#!/usr/bin/env python3
"""Test script to check stock comparison functionality"""

import os
import sys
import requests
from werkzeug.security import generate_password_hash

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_comparison():
    """Test the stock comparison endpoint"""
    base_url = 'http://localhost:5001'
    
    # First, let's try to create a test user and login
    session = requests.Session()
    
    # Try to register a test user
    register_data = {
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }
    
    try:
        # Register
        resp = session.post(f'{base_url}/register', data=register_data)
        print(f"Register response: {resp.status_code}")
        
        # Login
        login_data = {
            'email': 'test@test.com',
            'password': 'test123'
        }
        resp = session.post(f'{base_url}/login', data=login_data)
        print(f"Login response: {resp.status_code}")
        
        # Now test the comparison endpoint
        resp = session.get(f'{base_url}/stocks/compare?symbols=AAPL,TSLA')
        print(f"Compare response: {resp.status_code}")
        
        if resp.status_code == 500:
            print("❌ 500 Error occurred")
            print("Response content:", resp.text[:500])
        elif resp.status_code == 200:
            print("✅ Compare endpoint working")
        else:
            print(f"Unexpected status: {resp.status_code}")
            
    except Exception as e:
        print(f"Error testing: {e}")

if __name__ == '__main__':
    test_comparison()
