#!/usr/bin/env python3
import requests
import json

def test_chart_api():
    """Test the chart data API endpoint"""
    
    # Test the demo chart data API
    symbol = 'AAPL'
    url = f'https://aksjeradar.trade/stocks/api/demo/chart-data/{symbol}?period=5d'
    
    try:
        print(f"Testing chart API: {url}")
        response = requests.get(url, timeout=10)
        print(f'Status Code: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'Response keys: {list(data.keys())}')
            if 'dates' in data and 'prices' in data:
                print(f'Dates count: {len(data["dates"])}')
                print(f'Prices count: {len(data["prices"])}')
                print('✅ Chart API is working - returns proper data structure')
            else:
                print('❌ Chart API missing expected keys (dates, prices)')
        else:
            print(f'❌ Chart API failed with status {response.status_code}')
            print(f'Response: {response.text[:500]}')
            
    except requests.exceptions.Timeout:
        print("❌ Chart API request timed out")
    except Exception as e:
        print(f'❌ Chart API error: {e}')

if __name__ == "__main__":
    test_chart_api()
