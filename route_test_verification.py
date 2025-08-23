#!/usr/bin/env python3
"""
Test script to verify all critical route fixes  
Tests the routes that were reported as failing with 500/404 errors
"""
import requests
import time
from datetime import datetime

BASE_URL = "https://aksjeradar.trade"

# Routes that were returning 404 errors
ROUTES_TO_TEST = [
    # Analysis routes that were 404
    "/analysis/market-overview",
    "/analysis/market_overview", 
    "/analysis/currency-overview",
    "/analysis/currency_overview",
    "/analysis/strategy-builder", 
    "/analysis/strategy_builder",
    "/analysis/fundamental",
    
    # Core routes that were 500
    "/index",
    "/",
    "/profile",  # Requires authentication
    
    # Achievements API that was 404
    "/achievements/api/update_stat",  # POST endpoint
    
    # Other critical routes
    "/demo",
    "/contact",
    "/pricing"
]

def test_route(route, method="GET"):
    """Test a single route"""
    try:
        url = f"{BASE_URL}{route}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json={"test": "data"}, timeout=10)
        
        status = response.status_code
        
        # Check for success or expected authentication redirects
        if status == 200:
            return "✅ OK"
        elif status == 302 and "/login" in response.headers.get('Location', ''):
            return "✅ OK (Auth redirect)"  
        elif status == 401 or status == 403:
            return "✅ OK (Auth required)"
        elif status == 404:
            return "❌ 404 NOT FOUND"
        elif status == 500:
            return "❌ 500 INTERNAL ERROR"
        else:
            return f"⚠️ {status}"
            
    except requests.exceptions.Timeout:
        return "⏱️ TIMEOUT"
    except requests.exceptions.RequestException as e:
        return f"🔌 CONNECTION ERROR: {e}"

def main():
    """Run all route tests"""
    print(f"🧪 Testing critical routes on {BASE_URL}")
    print(f"⏰ Started at: {datetime.now()}")
    print("=" * 60)
    
    results = {}
    
    for route in ROUTES_TO_TEST:
        print(f"Testing {route:<35} ... ", end="", flush=True)
        
        # Test POST for API endpoints
        if "/api/" in route:
            result = test_route(route, "POST")
        else:
            result = test_route(route, "GET")
            
        print(result)
        results[route] = result
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    print("=" * 60)
    
    # Summary
    success = sum(1 for r in results.values() if r.startswith("✅"))
    total = len(results)
    
    print(f"📊 SUMMARY: {success}/{total} routes working properly")
    
    # Show failures
    failures = {route: result for route, result in results.items() if not result.startswith("✅")}
    if failures:
        print("\n❌ FAILED ROUTES:")
        for route, result in failures.items():
            print(f"   {route}: {result}")
    else:
        print("\n🎉 All routes are working!")
    
    print(f"\n⏰ Completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
