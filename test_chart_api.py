#!/usr/bin/env python3
"""
Test script for chart API endpoint
"""
import requests
import json
import sys

def test_chart_api():
    """Test the chart API endpoint"""
    
    # Test different symbols
    symbols = ['EQNR.OL', 'AAPL', 'TESLA']
    base_url = 'http://localhost:5000'  # Adjust if running on different port
    
    print("Testing Chart API Endpoints...")
    print("=" * 50)
    
    for symbol in symbols:
        try:
            url = f"{base_url}/stocks/api/chart-data/{symbol}?period=30d"
            print(f"\nTesting: {url}")
            
            response = requests.get(url, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Data keys: {list(data.keys())}")
                print(f"Data points: {len(data.get('dates', []))}")
                print(f"Currency: {data.get('currency', 'N/A')}")
                if data.get('dates'):
                    print(f"First date: {data['dates'][0] if data['dates'] else 'None'}")
                    print(f"Last date: {data['dates'][-1] if data['dates'] else 'None'}")
                print("✅ API call successful")
            else:
                print(f"❌ API call failed: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed - is Flask server running on {base_url}?")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_chart_api()
