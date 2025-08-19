#!/usr/bin/env python3
"""
Test script to verify button functionality and API endpoints
"""
import requests
import sys
import json

def test_api_endpoints():
    """Test the watchlist and other API endpoints"""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing API endpoints...")
    
    # Test if app is running
    try:
        response = requests.get(f"{base_url}/stocks/list", timeout=5)
        print(f"✅ Stocks list page: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error accessing stocks list: {e}")
        return False
    
    # Test watchlist API (will require authentication, but we can see the response)
    try:
        response = requests.post(f"{base_url}/api/watchlist/add", 
                               json={"symbol": "AAPL"}, 
                               timeout=5)
        print(f"📊 Watchlist API response: {response.status_code}")
        if response.status_code == 401:
            print("✅ Watchlist API requires authentication (expected)")
        elif response.status_code == 200:
            print("✅ Watchlist API working")
        else:
            print(f"⚠️  Unexpected response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error testing watchlist API: {e}")
    
    # Check if we can access the page source
    try:
        response = requests.get(f"{base_url}/stocks/list", timeout=5)
        content = response.text
        
        # Check for button elements
        if 'add-to-watchlist' in content:
            print("✅ Watchlist buttons found in HTML")
        else:
            print("❌ Watchlist buttons not found in HTML")
            
        if 'external-buy-btn' in content:
            print("✅ Buy buttons found in HTML")
        else:
            print("❌ Buy buttons not found in HTML")
            
        # Check for CSRF token
        if 'csrf-token' in content:
            print("✅ CSRF token found in HTML")
        else:
            print("❌ CSRF token not found in HTML")
            
    except Exception as e:
        print(f"❌ Error checking page content: {e}")
    
    return True

def check_javascript_functionality():
    """Check if the JavaScript code looks correct"""
    print("\n🔍 Checking JavaScript functionality...")
    
    try:
        with open('/workspaces/aksjeny/app/templates/stocks/list.html', 'r') as f:
            content = f.read()
            
        # Check for event listeners
        if 'addEventListener' in content:
            print("✅ Event listeners found")
        else:
            print("❌ Event listeners not found")
            
        # Check for fetch API usage
        if 'fetch(' in content:
            print("✅ Fetch API calls found")
        else:
            print("❌ Fetch API calls not found")
            
        # Check for error handling
        if 'catch (error)' in content:
            print("✅ Error handling found")
        else:
            print("❌ Error handling not found")
            
        # Check for CSRF token usage
        if 'X-CSRFToken' in content:
            print("✅ CSRF token usage found")
        else:
            print("❌ CSRF token usage not found")
            
    except Exception as e:
        print(f"❌ Error reading template file: {e}")

if __name__ == "__main__":
    print("🔧 Testing button functionality...")
    test_api_endpoints()
    check_javascript_functionality()
    print("\n✅ Test complete!")
