#!/usr/bin/env python3
"""
Test critical endpoints after database migration
"""
import sys
import os
import requests
import time
from datetime import datetime

# Railway production URL
BASE_URL = "https://aksjeny2-production.up.railway.app"

def test_endpoint(url, name, method='GET', data=None, headers=None):
    """Test a single endpoint"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers, timeout=10)
        
        status_code = response.status_code
        
        if status_code == 200:
            return f"✅ {name}: {status_code} OK"
        elif status_code in [302, 301]:
            return f"🔄 {name}: {status_code} REDIRECT"
        elif status_code == 403:
            return f"🔒 {name}: {status_code} ACCESS DENIED (expected for auth)"
        elif status_code == 404:
            return f"❓ {name}: {status_code} NOT FOUND"
        elif status_code == 500:
            return f"💥 {name}: {status_code} SERVER ERROR"
        else:
            return f"⚠️  {name}: {status_code} UNEXPECTED"
            
    except requests.exceptions.Timeout:
        return f"⏰ {name}: TIMEOUT"
    except requests.exceptions.ConnectionError:
        return f"🚫 {name}: CONNECTION ERROR"
    except Exception as e:
        return f"💥 {name}: ERROR - {e}"

def test_critical_endpoints():
    """Test all critical endpoints that were having 500 errors"""
    print("🧪 Testing critical endpoints after database migration...")
    print("=" * 60)
    
    # Test endpoints that were having 500 errors
    critical_tests = [
        # Primary 500 error endpoints
        (f"{BASE_URL}/analysis/warren-buffett", "Warren Buffett Analysis"),
        (f"{BASE_URL}/watchlist", "Watchlist"),
        (f"{BASE_URL}/profile", "Profile"),
        (f"{BASE_URL}/analysis/sentiment", "Sentiment Analysis"),
        
        # Search functionality
        (f"{BASE_URL}/stocks/search?q=tesla", "Search Tesla"),
        (f"{BASE_URL}/stocks/search?q=dnb", "Search DNB"),
        (f"{BASE_URL}/stocks/search?q=apple", "Search Apple"),
        
        # Other critical routes
        (f"{BASE_URL}/", "Homepage"),
        (f"{BASE_URL}/dashboard", "Dashboard"),
        (f"{BASE_URL}/market-intel", "Market Intel"),
        (f"{BASE_URL}/daily-view", "Daily View"),
        (f"{BASE_URL}/norwegian-intel", "Norwegian Intel"),
        (f"{BASE_URL}/sentiment", "Sentiment Page"),
        (f"{BASE_URL}/news", "News"),
        
        # API endpoints
        (f"{BASE_URL}/api/stocks/data", "Stocks API"),
        (f"{BASE_URL}/api/user/stats", "User Stats API"),
    ]
    
    results = []
    for url, name in critical_tests:
        result = test_endpoint(url, name)
        results.append(result)
        print(result)
        time.sleep(0.5)  # Be nice to the server
    
    print("=" * 60)
    
    # Count results
    success_count = sum(1 for r in results if "✅" in r)
    redirect_count = sum(1 for r in results if "🔄" in r)
    auth_count = sum(1 for r in results if "🔒" in r)
    error_500_count = sum(1 for r in results if "💥" in r and "500" in r)
    other_errors = len(results) - success_count - redirect_count - auth_count - error_500_count
    
    print(f"📊 TEST SUMMARY:")
    print(f"   ✅ Success: {success_count}")
    print(f"   🔄 Redirects: {redirect_count}")
    print(f"   🔒 Auth Required: {auth_count}")
    print(f"   💥 500 Errors: {error_500_count}")
    print(f"   ⚠️  Other Issues: {other_errors}")
    
    if error_500_count == 0:
        print("\n🎉 NO 500 ERRORS FOUND! Database migration successful!")
    else:
        print(f"\n⚠️  {error_500_count} endpoints still have 500 errors")
        print("Additional fixes may be needed.")
    
    # Test search specifically
    print("\n🔍 SEARCH SPECIFIC TESTS:")
    search_tests = [
        (f"{BASE_URL}/stocks/search?q=tesla", "Tesla Search"),
        (f"{BASE_URL}/stocks/search?q=dnb", "DNB Search"),
        (f"{BASE_URL}/stocks/search?q=eqnr", "Equinor Search"),
    ]
    
    for url, name in search_tests:
        result = test_endpoint(url, name)
        print(result)
    
    return error_500_count == 0

if __name__ == '__main__':
    print(f"🕐 Starting endpoint tests at {datetime.now()}")
    success = test_critical_endpoints()
    print(f"🕐 Tests completed at {datetime.now()}")
    sys.exit(0 if success else 1)
