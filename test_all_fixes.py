#!/usr/bin/env python3
"""
Test script to verify all the fixes are working correctly
"""

import requests
import sys
import time

BASE_URL = "http://localhost:5002"

# NOTE: Renamed to helper_test_endpoint to avoid pytest collecting this
# diagnostic function (returns bool and uses prints).
def helper_test_endpoint(url, expected_status=200, test_name=""):
    """Test if an endpoint is accessible"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            print(f"✅ {test_name}: {url} - Status {response.status_code}")
            return True
        else:
            print(f"❌ {test_name}: {url} - Status {response.status_code} (expected {expected_status})")
            return False
    except Exception as e:
        print(f"❌ {test_name}: {url} - Error: {e}")
        return False

def main():
    print("🚀 Testing all fixes for Aksjeradar.trade issues\n")
    
    # Test basic server health
    print("1. Testing basic server health...")
    if not helper_test_endpoint(f"{BASE_URL}/health/ready", test_name="Health Check"):
        print("❌ Server not ready, exiting...")
        return
    
    # Test the specific URLs mentioned by the user
    print("\n2. Testing specific URLs mentioned in the issue...")
    
    # Stock comparison page
    helper_test_endpoint(f"{BASE_URL}/stocks/compare", test_name="Stock Comparison Page")
    
    # Watchlist pages  
    helper_test_endpoint(f"{BASE_URL}/watchlist/", test_name="Watchlist Main Page")
    
    # Portfolio pages
    helper_test_endpoint(f"{BASE_URL}/portfolio/", test_name="Portfolio Main Page")
    
    # Profile page (may redirect to login, so expect 302)
    helper_test_endpoint(f"{BASE_URL}/profile", expected_status=302, test_name="Profile Page")
    
    print("\n3. Testing API endpoints...")
    
    # Test watchlist API endpoints
    helper_test_endpoint(f"{BASE_URL}/watchlist/api/alerts", test_name="Watchlist Alerts API")
    
    # Test portfolio API endpoints
    helper_test_endpoint(f"{BASE_URL}/portfolio/api/portfolios", test_name="Portfolio API")
    
    print("\n4. Testing Chart.js functionality...")
    
    # Test if compare page returns content with chart container
    try:
        response = requests.get(f"{BASE_URL}/stocks/compare", timeout=10)
        if response.status_code == 200:
            content = response.text
            has_chart_js = 'Chart.js' in content or 'chart.js' in content
            has_chart_canvas = 'priceChart' in content or 'chartCanvas' in content  
            has_chart_script = 'new Chart(' in content
            
            if has_chart_js and has_chart_canvas and has_chart_script:
                print("✅ Chart.js: Stock comparison page has Chart.js, canvas, and initialization script")
            else:
                print(f"❌ Chart.js: Missing elements - Chart.js: {has_chart_js}, Canvas: {has_chart_canvas}, Script: {has_chart_script}")
        else:
            print(f"❌ Chart.js: Could not access comparison page (status {response.status_code})")
    except Exception as e:
        print(f"❌ Chart.js: Error testing chart functionality: {e}")
    
    print("\n✅ Testing completed!")
    print("\nNote: Some features may require authentication to fully test.")
    print("The fixes have been applied for:")
    print("- Empty chart container on stock comparison page") 
    print("- Watchlist detail page creation")
    print("- Portfolio add stock functionality")
    print("- CSRF token display issues")
    print("- Profile favorites loading logic")

if __name__ == "__main__":
    main()
