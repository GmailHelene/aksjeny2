#!/usr/bin/env python3
"""
Favorites Functionality Test for Crypto Page
Tests the favorites toggle endpoint specifically for crypto symbols
"""

import requests
import json
from datetime import datetime

def test_crypto_favorites():
    """Test the crypto favorites functionality"""
    base_url = "https://aksjeradar.trade"
    
    # Test crypto symbols
    crypto_symbols = ['BTC-USD', 'ETH-USD', 'XRP-USD']
    
    print("🧪 Testing Crypto Favorites Functionality")
    print("=" * 50)
    
    for symbol in crypto_symbols:
        print(f"\n🪙 Testing {symbol}")
        print("-" * 30)
        
        # Test toggle endpoint
        toggle_url = f"{base_url}/stocks/api/favorites/toggle/{symbol}"
        
        try:
            response = requests.post(toggle_url, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                if data.get('success'):
                    print(f"✅ Toggle works: {data.get('message')}")
                else:
                    print(f"❌ Toggle failed: {data.get('error')} - {data.get('message')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"Error text: {response.text[:200]}")
                    
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🔍 Additional Endpoint Tests")
    print("=" * 50)
    
    # Test the individual add/remove endpoints
    test_symbol = "BTC-USD"
    
    # Test add endpoint
    add_url = f"{base_url}/stocks/api/favorites/add"
    try:
        add_response = requests.post(add_url, 
            json={'symbol': test_symbol, 'name': 'Bitcoin', 'exchange': 'Crypto'},
            timeout=10
        )
        print(f"\n📈 Add endpoint test:")
        print(f"Status: {add_response.status_code}")
        if add_response.status_code == 200:
            print(f"Response: {json.dumps(add_response.json(), indent=2)}")
        else:
            print(f"Error: {add_response.text[:200]}")
    except Exception as e:
        print(f"❌ Add endpoint failed: {str(e)}")
    
    # Test remove endpoint  
    remove_url = f"{base_url}/stocks/api/favorites/remove"
    try:
        remove_response = requests.post(remove_url,
            json={'symbol': test_symbol},
            timeout=10
        )
        print(f"\n📉 Remove endpoint test:")
        print(f"Status: {remove_response.status_code}")
        if remove_response.status_code == 200:
            print(f"Response: {json.dumps(remove_response.json(), indent=2)}")
        else:
            print(f"Error: {remove_response.text[:200]}")
    except Exception as e:
        print(f"❌ Remove endpoint failed: {str(e)}")
    
    # Test check endpoint
    check_url = f"{base_url}/stocks/api/favorites/check/{test_symbol}"
    try:
        check_response = requests.get(check_url, timeout=10)
        print(f"\n🔍 Check endpoint test:")
        print(f"Status: {check_response.status_code}")
        if check_response.status_code == 200:
            print(f"Response: {json.dumps(check_response.json(), indent=2)}")
        else:
            print(f"Error: {check_response.text[:200]}")
    except Exception as e:
        print(f"❌ Check endpoint failed: {str(e)}")

if __name__ == "__main__":
    test_crypto_favorites()
