#!/usr/bin/env python3
"""Test script to debug stocks details route issues"""

import sys
import os
import requests
from datetime import datetime

def test_stocks_route():
    """Test the stocks details route"""
    
    # Test the local development server
    base_url = "http://localhost:5002"
    test_symbol = "EQNR.OL"
    
    print(f"Testing stocks details route at {base_url}")
    print(f"Testing symbol: {test_symbol}")
    print(f"Time: {datetime.now()}")
    print("-" * 50)
    
    try:
        # Test the stocks details route
        url = f"{base_url}/stocks/details/{test_symbol}"
        print(f"Testing URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 500:
            print("500 Error detected!")
            print("Response content:")
            print(response.text[:2000])  # First 2000 chars
            
        elif response.status_code == 200:
            print("Success! Route is working.")
            print(f"Response length: {len(response.text)} characters")
            
        else:
            print(f"Unexpected status code: {response.status_code}")
            print("Response content:")
            print(response.text[:1000])
            
    except requests.ConnectionError:
        print("Connection error - server may not be running")
    except requests.Timeout:
        print("Request timed out")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_stocks_route()
