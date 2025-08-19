#!/usr/bin/env python3
"""Test script to check sentiment analysis functionality"""

import requests

def test_sentiment():
    """Test the sentiment analysis endpoint"""
    base_url = 'http://localhost:5001'
    
    # Create session and login
    session = requests.Session()
    
    # Register a test user
    register_data = {
        'username': 'sentimentuser',
        'email': 'sentiment@test.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }
    
    try:
        # Register
        resp = session.post(f'{base_url}/register', data=register_data)
        print(f"Register response: {resp.status_code}")
        
        # Login
        login_data = {
            'email': 'sentiment@test.com',
            'password': 'test123'
        }
        resp = session.post(f'{base_url}/login', data=login_data)
        print(f"Login response: {resp.status_code}")
        
        # Test sentiment analysis
        resp = session.get(f'{base_url}/analysis/sentiment')
        print(f"Sentiment analysis response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Sentiment analysis error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Sentiment analysis working")
            
        # Test sentiment with symbol
        resp = session.get(f'{base_url}/analysis/sentiment?symbol=AAPL')
        print(f"Sentiment analysis with symbol response: {resp.status_code}")
        if resp.status_code != 200:
            print("❌ Sentiment analysis with symbol error")
            print("Response content:", resp.text[:500])
        else:
            print("✅ Sentiment analysis with symbol working")
            
    except Exception as e:
        print(f"Error testing: {e}")

if __name__ == '__main__':
    test_sentiment()
