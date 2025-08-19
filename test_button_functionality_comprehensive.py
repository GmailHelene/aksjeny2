#!/usr/bin/env python3
"""
Comprehensive test of buy+ and star button functionality 
"""

import requests
import time
import json
from bs4 import BeautifulSoup

def test_button_functionality():
    """Test the buy and star button functionality"""
    base_url = "http://localhost:5001"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("🔍 Testing Button Functionality")
    print("=" * 50)
    
    # 1. Test login
    print("\n1. Testing login...")
    login_data = {
        'email': 'tonje@gmail.com',
        'password': 'pass123'
    }
    
    try:
        login_response = session.post(f"{base_url}/auth/login", data=login_data)
        print(f"   ✅ Login status: {login_response.status_code}")
        if login_response.status_code != 200:
            print(f"   ❌ Login failed with status {login_response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # 2. Test currency page access
    print("\n2. Testing currency page access...")
    try:
        currency_response = session.get(f"{base_url}/stocks/list/currency")
        print(f"   ✅ Currency page status: {currency_response.status_code}")
        
        if currency_response.status_code == 200:
            # Parse the HTML to check for buttons
            soup = BeautifulSoup(currency_response.text, 'html.parser')
            
            # Check for buy buttons
            buy_buttons = soup.find_all('button', class_='external-buy-btn')
            print(f"   ✅ Found {len(buy_buttons)} buy buttons")
            
            # Check for star buttons
            star_buttons = soup.find_all('button', class_='add-to-watchlist')
            print(f"   ✅ Found {len(star_buttons)} star buttons")
            
            # Check for JavaScript functionality
            scripts = soup.find_all('script')
            has_watchlist_js = any('add-to-watchlist' in str(script) for script in scripts)
            has_buy_js = any('external-buy-btn' in str(script) for script in scripts)
            
            print(f"   ✅ Has watchlist JavaScript: {has_watchlist_js}")
            print(f"   ✅ Has buy button JavaScript: {has_buy_js}")
            
            # Extract CSRF token
            csrf_meta = soup.find('meta', {'name': 'csrf-token'})
            csrf_token = csrf_meta.get('content') if csrf_meta else None
            print(f"   ✅ CSRF token found: {csrf_token is not None}")
            
            if len(buy_buttons) > 0 and len(star_buttons) > 0:
                print("   ✅ Currency page has all required buttons")
            else:
                print("   ❌ Currency page missing some buttons")
                
        else:
            print(f"   ❌ Currency page failed: {currency_response.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Currency page error: {e}")
        return
    
    # 3. Test watchlist API endpoint
    print("\n3. Testing watchlist API...")
    try:
        # Get CSRF token first
        csrf_response = session.get(f"{base_url}/stocks/list/currency")
        soup = BeautifulSoup(csrf_response.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        csrf_token = csrf_meta.get('content') if csrf_meta else None
        
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
        
        # Test adding to watchlist
        watchlist_data = {'symbol': 'USDNOK'}
        watchlist_response = session.post(
            f"{base_url}/api/watchlist/add",
            json=watchlist_data,
            headers=headers
        )
        
        print(f"   ✅ Watchlist API status: {watchlist_response.status_code}")
        if watchlist_response.status_code == 200:
            response_json = watchlist_response.json()
            print(f"   ✅ Watchlist response: {response_json}")
        else:
            print(f"   ❌ Watchlist API failed: {watchlist_response.text}")
            
    except Exception as e:
        print(f"   ❌ Watchlist API error: {e}")
    
    # 4. Test oslo stocks page
    print("\n4. Testing Oslo stocks page...")
    try:
        oslo_response = session.get(f"{base_url}/stocks/list/oslo")
        print(f"   ✅ Oslo page status: {oslo_response.status_code}")
        
        if oslo_response.status_code == 200:
            soup = BeautifulSoup(oslo_response.text, 'html.parser')
            buy_buttons = soup.find_all('button', class_='external-buy-btn')
            star_buttons = soup.find_all('button', class_='add-to-watchlist')
            
            print(f"   ✅ Oslo page - Buy buttons: {len(buy_buttons)}")
            print(f"   ✅ Oslo page - Star buttons: {len(star_buttons)}")
            
    except Exception as e:
        print(f"   ❌ Oslo page error: {e}")
    
    # 5. Test global stocks page
    print("\n5. Testing Global stocks page...")
    try:
        global_response = session.get(f"{base_url}/stocks/list/global")
        print(f"   ✅ Global page status: {global_response.status_code}")
        
        if global_response.status_code == 200:
            soup = BeautifulSoup(global_response.text, 'html.parser')
            buy_buttons = soup.find_all('button', class_='external-buy-btn')
            star_buttons = soup.find_all('button', class_='add-to-watchlist')
            
            print(f"   ✅ Global page - Buy buttons: {len(buy_buttons)}")
            print(f"   ✅ Global page - Star buttons: {len(star_buttons)}")
            
    except Exception as e:
        print(f"   ❌ Global page error: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 Button Functionality Test Complete")

if __name__ == "__main__":
    test_button_functionality()
