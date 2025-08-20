#!/usr/bin/env python3

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_endpoint(method, url, data=None, description=""):
    """Test an endpoint and return the result"""
    try:
        if method.upper() == 'GET':
            response = requests.get(f"{BASE_URL}{url}", timeout=10)
        elif method.upper() == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(f"{BASE_URL}{url}", json=data, headers=headers, timeout=10)
        
        print(f"✅ {description} - Status: {response.status_code}")
        if response.status_code >= 400:
            print(f"   Error: {response.text[:200]}")
        return response.status_code < 400
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def main():
    print("🔬 Testing all broken functionalities...")
    print("=" * 50)
    
    # Test basic connectivity
    print("\n1. Basic Connectivity Tests:")
    test_endpoint('GET', '/', description="Main page")
    test_endpoint('GET', '/stocks', description="Stocks overview")
    test_endpoint('GET', '/stocks/list', description="Stocks list")
    
    # Test favorites API
    print("\n2. Favorites API Tests:")
    test_endpoint('GET', '/stocks/api/favorites/check/AAPL', description="Check favorite status")
    test_endpoint('POST', '/stocks/api/favorites/add', {'symbol': 'AAPL'}, description="Add to favorites")
    test_endpoint('POST', '/stocks/api/favorites/remove', {'symbol': 'AAPL'}, description="Remove from favorites")
    
    # Test portfolio and watchlist
    print("\n3. Portfolio/Watchlist Tests:")
    test_endpoint('GET', '/portfolio/portfolio', description="Portfolio page")
    test_endpoint('GET', '/portfolio/watchlist', description="Watchlist page")
    test_endpoint('POST', '/watchlist/delete/1', description="Delete watchlist")
    test_endpoint('POST', '/portfolio/portfolio/9/add', {'symbol': 'AAPL', 'quantity': 10, 'price': 150}, description="Add to portfolio")
    
    # Test analysis tools
    print("\n4. Analysis Tools Tests:")
    test_endpoint('GET', '/stocks/compare?symbols=AAPL,MSFT', description="Stock comparison")
    test_endpoint('GET', '/analyse/sentiment', description="Sentiment analysis")
    test_endpoint('GET', '/settings', description="Settings page")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    main()
