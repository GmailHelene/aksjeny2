#!/usr/bin/env python3
"""Simple test of search URLs and basic functionality"""

import requests
import sys

def test_search_urls():
    """Test various search-related URLs to see what works"""
    base_url = 'http://localhost:5000'  # Assumes local Flask server
    
    test_urls = [
        '/stocks/search',  # Main search page
        '/stocks/search?q=tesla',  # Search with query
        '/stocks/api/search?q=dnb',  # API search endpoint
        '/api/stocks/search?q=eqnr',  # Alternative API endpoint
    ]
    
    print("Testing search URLs...")
    print("=" * 50)
    
    for url in test_urls:
        full_url = f"{base_url}{url}"
        try:
            response = requests.get(full_url, timeout=5)
            status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"{status} - {url}")
            if response.status_code != 200:
                print(f"    Error: {response.text[:100]}")
        except Exception as e:
            print(f"❌ FAILED - {url}: {e}")
    
    print("\n" + "=" * 50)
    print("Note: This test requires a running Flask server on localhost:5000")

if __name__ == '__main__':
    test_search_urls()
