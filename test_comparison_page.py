#!/usr/bin/env python3
"""
Test script to validate the comparison page functionality
"""
import requests
import json
from bs4 import BeautifulSoup

def test_comparison_page():
    """Test the comparison page with AAPL and MSFT"""
    try:
        # Test the comparison endpoint
        url = "http://localhost:5002/stocks/compare"
        params = {
            'tickers': ['AAPL', 'MSFT'],
            'period': '6mo',
            'interval': '1d',
            'normalize': '1'
        }
        
        print("🧪 Testing comparison page...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ Comparison page loads successfully")
            
            # Check if response contains chart data
            content = response.text
            if 'chart_data' in content:
                print("✅ Chart data variable found in template")
            else:
                print("⚠️ Chart data variable not found")
                
            # Check for JavaScript errors in template
            if 'Chart(' in content:
                print("✅ Chart.js initialization found")
            else:
                print("⚠️ Chart.js initialization not found")
                
            # Parse HTML to check structure
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for chart canvases
            price_chart = soup.find('canvas', {'id': 'priceChart'})
            volume_chart = soup.find('canvas', {'id': 'volumeChart'})
            
            if price_chart:
                print("✅ Price chart canvas found")
            else:
                print("⚠️ Price chart canvas missing")
                
            if volume_chart:
                print("✅ Volume chart canvas found")
            else:
                print("⚠️ Volume chart canvas missing")
                
            # Check for data tables
            tables = soup.find_all('table')
            if len(tables) >= 2:
                print(f"✅ Found {len(tables)} data tables")
            else:
                print(f"⚠️ Expected at least 2 tables, found {len(tables)}")
                
        else:
            print(f"❌ Failed to load comparison page: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server. Make sure it's running on localhost:5002")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_comparison_page()
