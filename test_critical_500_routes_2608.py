#!/usr/bin/env python3
"""
Test script for critical 500 error routes - 2608 version
Tests the specific routes mentioned in the TODO list
"""

import requests
import sys
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Create a session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def test_route(session, url, description):
    """Test a single route"""
    try:
        print(f"Testing {description}: {url}")
        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"  ✅ {response.status_code} OK")
            return True
        elif response.status_code == 500:
            print(f"  ❌ {response.status_code} INTERNAL SERVER ERROR")
            return False
        else:
            print(f"  ⚠️  {response.status_code} - {response.reason}")
            return True  # Not a 500 error
            
    except requests.exceptions.RequestException as e:
        print(f"  💥 REQUEST ERROR: {e}")
        return False

def main():
    base_url = "http://localhost:5002"  # Updated port
    
    # Critical routes from TODO list
    critical_routes = [
        ("/stocks/compare", "Stocks Compare"),
        ("/analysis/sentiment", "Analysis Sentiment"),
        ("/forum/create_topic", "Forum Create Topic"),
        ("/profile", "User Profile"),
        ("/notifications/api/settings", "Notifications API Settings"),
        ("/external-data/market-intelligence", "Market Intelligence"),
        ("/external-data/analyst-coverage", "Analyst Coverage"),
    ]
    
    print("🔍 TESTING CRITICAL 500 ERROR ROUTES")
    print("=" * 50)
    
    session = create_session()
    results = []
    
    for route, description in critical_routes:
        url = f"{base_url}{route}"
        success = test_route(session, url, description)
        results.append((route, success))
        time.sleep(0.5)  # Small delay between requests
    
    print("\n📊 RESULTS SUMMARY")
    print("=" * 50)
    
    success_count = 0
    for route, success in results:
        status = "✅ WORKING" if success else "❌ 500 ERROR"
        print(f"{route:<30} {status}")
        if success:
            success_count += 1
    
    print(f"\n🎯 SUCCESS RATE: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
    
    if success_count == len(results):
        print("🎉 ALL CRITICAL ROUTES ARE WORKING!")
        return 0
    else:
        remaining = len(results) - success_count
        print(f"⚠️  {remaining} routes still need fixing")
        return 1

if __name__ == "__main__":
    sys.exit(main())
