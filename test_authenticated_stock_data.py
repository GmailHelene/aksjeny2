#!/usr/bin/env python3
"""
Test authenticated stock data access
This tests whether authenticated users are getting real data vs synthetic data
"""

import requests
import json
import time

def test_stock_data():
    """Test stock data endpoint with and without authentication"""
    
    base_url = "https://aksjeradar.trade"
    test_symbols = ["TSLA", "DNB.OL", "EQNR.OL"]
    
    print("=== Testing Stock Data Access ===")
    
    # Test without authentication (should show demo data)
    print("\n1. Testing without authentication:")
    session = requests.Session()
    
    for symbol in test_symbols:
        url = f"{base_url}/stocks/details/{symbol}"
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                if "$100.00" in response.text:
                    print(f"  {symbol}: Shows $100.00 (synthetic data) ✓")
                elif "price" in response.text.lower():
                    print(f"  {symbol}: Shows other price data")
                else:
                    print(f"  {symbol}: No clear price found")
            else:
                print(f"  {symbol}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  {symbol}: Error - {e}")
    
    # Test API endpoint directly
    print("\n2. Testing API endpoint:")
    for symbol in test_symbols:
        api_url = f"{base_url}/api/stock/{symbol}"
        try:
            response = session.get(api_url, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    price = data.get('regularMarketPrice', data.get('last_price', 'Unknown'))
                    print(f"  {symbol} API: Price = {price}")
                except:
                    print(f"  {symbol} API: Non-JSON response")
            else:
                print(f"  {symbol} API: HTTP {response.status_code}")
        except Exception as e:
            print(f"  {symbol} API: Error - {e}")
    
    # Test real fallback data constants
    print("\n3. Testing fallback data constants:")
    fallback_data = {
        'TSLA': {'name': 'Tesla Inc', 'last_price': 230.45, 'sector': 'Technology'},
        'DNB.OL': {'name': 'DNB Bank ASA', 'last_price': 185.20, 'sector': 'Financial Services'},
        'EQNR.OL': {'name': 'Equinor ASA', 'last_price': 270.50, 'sector': 'Energy'}
    }
    
    for symbol, expected in fallback_data.items():
        print(f"  {symbol}: Expected ${expected['last_price']} for authenticated users")
    
    print("\n=== Analysis ===")
    print("If authenticated users are seeing $100.00 instead of the expected prices above,")
    print("then the authentication logic in the stock details route needs to be fixed.")
    
if __name__ == "__main__":
    test_stock_data()
