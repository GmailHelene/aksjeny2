#!/usr/bin/env python3
"""Test script for stocks compare functionality"""

import requests
import json

def test_compare():
    """Test the stocks compare endpoint"""
    try:
        # Test with simple tickers
        url = "http://localhost:5000/stocks/compare"
        params = {
            'tickers': ['EQNR.OL', 'DNB.OL'],
            'period': '6mo',
            'interval': '1d',
            'normalize': '1'
        }
        
        print(f"Testing {url} with params: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Compare endpoint working!")
            print(f"Response length: {len(response.text)} characters")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:1000]}...")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_compare()
