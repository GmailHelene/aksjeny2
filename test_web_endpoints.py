#!/usr/bin/env python3
"""Direct web test of fixed issues"""

import sys
import os
import time

def test_web_endpoints():
    """Test web endpoints directly"""
    
    print("🌐 TESTING WEB ENDPOINTS")
    print("="*40)
    
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        os.system("pip install requests")
        import requests
    
    base_url = "http://localhost:5000"
    
    # Test endpoints
    endpoints = [
        "/",
        "/analysis/warren-buffett", 
        "/profile",
        "/stocks/list/oslo"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"Testing {endpoint}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - Status: {response.status_code}")
            elif response.status_code == 302:
                print(f"   🔄 {endpoint} - Redirect (likely to login): {response.status_code}")
            else:
                print(f"   ⚠️  {endpoint} - Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint} - Error: {e}")
    
    print()
    print("🎯 TESTING WARREN BUFFETT WITH TICKER")
    print("="*40)
    
    try:
        # Test Warren Buffett with a ticker
        response = requests.get(f"{base_url}/analysis/warren-buffett?ticker=AAPL", timeout=10)
        
        if response.status_code == 200:
            print("✅ Warren Buffett analysis with ticker AAPL works!")
            if "AAPL" in response.text:
                print("✅ Response contains ticker data")
            else:
                print("⚠️  Response doesn't contain expected ticker data")
        else:
            print(f"❌ Warren Buffett analysis failed - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Warren Buffett test error: {e}")

if __name__ == '__main__':
    test_web_endpoints()
