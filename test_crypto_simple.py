#!/usr/bin/env python3
"""
Simple favorites test for crypto symbols
"""

import requests
import json

def test_crypto_favorites_simple():
    """Test crypto favorites functionality"""
    base_url = "https://aksjeradar.trade"
    test_symbol = "BTC-USD"
    
    print(f"🧪 Testing crypto favorites for {test_symbol}")
    print("=" * 50)
    
    # Test the toggle endpoint
    toggle_url = f"{base_url}/stocks/api/favorites/toggle/{test_symbol}"
    
    for i in range(2):  # Test toggling twice
        print(f"\n🔄 Toggle attempt {i+1}")
        try:
            response = requests.post(toggle_url, timeout=15)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Success: {data.get('success')}")
                print(f"Favorited: {data.get('favorited')}")
                print(f"Message: {data.get('message')}")
                
                if not data.get('success'):
                    print(f"❌ Error: {data.get('error')}")
                    print(f"❌ Full response: {json.dumps(data, indent=2)}")
                else:
                    print(f"✅ Success: {data.get('message')}")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response text: {response.text[:500]}")
                
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Test completed")

if __name__ == "__main__":
    test_crypto_favorites_simple()
