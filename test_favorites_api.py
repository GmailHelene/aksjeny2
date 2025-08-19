#!/usr/bin/env python3
"""Test favorites API directly through Flask app"""

import requests
import time

def test_favorites_api():
    """Test the favorites API endpoints"""
    base_url = "http://localhost:5001"
    
    print("=== Testing Favorites API ===")
    
    # Test if stocks route is accessible
    try:
        response = requests.get(f"{base_url}/stocks/")
        print(f"Stocks route status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Stocks blueprint is working")
        else:
            print(f"❌ Stocks route error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error accessing stocks route: {e}")
    
    # Test favorites API (should return 401 without login)
    try:
        response = requests.post(f"{base_url}/stocks/api/favorites/add",
                               json={"symbol": "AAPL", "name": "Apple Inc"})
        print(f"Favorites API status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Favorites API requires authentication (as expected)")
        elif response.status_code == 404:
            print("❌ Favorites API endpoint not found!")
        elif response.status_code == 500:
            print("❌ Server error in favorites API")
            print(f"Response: {response.text[:200]}")
        else:
            print(f"Unexpected status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Error testing favorites API: {e}")
    
    # Test if the route is registered by checking available routes
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is responding to requests")
        else:
            print(f"❌ Server issue: {response.status_code}")
    except Exception as e:
        print(f"❌ Server connection error: {e}")

if __name__ == '__main__':
    test_favorites_api()
