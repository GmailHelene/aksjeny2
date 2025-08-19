#!/usr/bin/env python3

import requests
import sys

def test_endpoints():
    base_url = "http://localhost:5002"
    
    # Test endpoints
    endpoints = [
        "/analysis/sentiment?symbol=DNB.OL",
        "/stocks/list/crypto", 
        "/stocks/list/currency",
        "/stocks/list/global",
        "/"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n=== Testing {endpoint} ===")
            response = requests.get(base_url + endpoint, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 500:
                print(f"❌ 500 Error on {endpoint}")
                if response.text:
                    # Print first 500 chars of error
                    print(f"Error: {response.text[:500]}...")
            elif response.status_code == 200:
                print(f"✅ Success on {endpoint}")
            elif response.status_code == 302:
                print(f"🔄 Redirect on {endpoint} -> {response.headers.get('Location', 'Unknown')}")
            else:
                print(f"⚠️ Status {response.status_code} on {endpoint}")
                
        except Exception as e:
            print(f"❌ Request failed for {endpoint}: {e}")

if __name__ == "__main__":
    test_endpoints()
