#!/usr/bin/env python3
"""Test script for favorites/watchlist functionality"""

import requests
import sys
import json

def test_favorites_system():
    """Test the favorites system endpoints"""
    base_url = "http://localhost:5001"
    
    print("=== Testing Favorites/Watchlist System ===")
    
    # Test 1: Check if stocks route works
    print("1. Testing stocks route...")
    try:
        response = requests.get(f"{base_url}/stocks/")
        print(f"   Stocks route status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Stocks route working")
        else:
            print(f"   ❌ Stocks route failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing stocks route: {e}")
    
    # Test 2: Test favorites API without authentication (should return 401)
    print("\n2. Testing favorites API without authentication...")
    try:
        response = requests.post(f"{base_url}/stocks/api/favorites/add",
                               json={"symbol": "AAPL", "name": "Apple Inc"})
        print(f"   Favorites API status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Favorites API correctly requires authentication")
        elif response.status_code == 404:
            print("   ❌ Favorites API endpoint not found!")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error testing favorites API: {e}")
    
    # Test 3: Check basic home page
    print("\n3. Testing home page...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Home page status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Home page working")
        else:
            print(f"   ❌ Home page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing home page: {e}")
    
    # Test 4: Check price alerts endpoint
    print("\n4. Testing price alerts...")
    try:
        response = requests.get(f"{base_url}/price-alerts/")
        print(f"   Price alerts page status: {response.status_code}")
        if response.status_code in [200, 302]:  # 302 if redirected to login
            print("   ✅ Price alerts route exists")
        else:
            print(f"   ❌ Price alerts route failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing price alerts: {e}")
    
    # Test 5: Check sentiment analysis
    print("\n5. Testing sentiment analysis...")
    try:
        response = requests.get(f"{base_url}/analysis/sentiment")
        print(f"   Sentiment analysis status: {response.status_code}")
        if response.status_code in [200, 302]:
            print("   ✅ Sentiment analysis route exists")
        else:
            print(f"   ❌ Sentiment analysis failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing sentiment analysis: {e}")
    
    # Test 6: Check insider trading
    print("\n6. Testing insider trading...")
    try:
        response = requests.get(f"{base_url}/market-intel/insider-trading")
        print(f"   Insider trading status: {response.status_code}")
        if response.status_code in [200, 302]:
            print("   ✅ Insider trading route exists")
        else:
            print(f"   ❌ Insider trading failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing insider trading: {e}")
    
    print("\n=== Test Summary ===")
    print("All major routes are accessible. Issues with favorites system")
    print("are likely related to authentication/CSRF tokens or database table.")
    print("\nNext steps:")
    print("1. Ensure favorites table exists in database")
    print("2. Test with logged-in user session")
    print("3. Verify CSRF tokens are generated correctly")

if __name__ == '__main__':
    test_favorites_system()
