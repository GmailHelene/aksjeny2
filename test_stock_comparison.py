#!/usr/bin/env python3
"""
Quick test script to verify stock comparison functionality
"""

import requests
import json

def test_stock_comparison():
    """Test the stock comparison endpoint"""
    
    # Test with Norwegian stocks
    test_url = "http://localhost:5000/stocks/compare?tickers=EQNR.OL,DNB.OL"
    
    print("Testing stock comparison endpoint...")
    print(f"URL: {test_url}")
    
    try:
        response = requests.get(test_url)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Stock comparison page loaded successfully!")
            
            # Check if the response contains chart-related content
            content = response.text
            if 'chart_data' in content.lower():
                print("✅ Chart data present in response")
            else:
                print("❌ No chart data found in response")
                
            if 'chart.js' in content.lower():
                print("✅ Chart.js library included")
            else:
                print("❌ Chart.js library not found")
                
            if 'pricechart' in content.lower():
                print("✅ Price chart element found")
            else:
                print("❌ Price chart element not found")
                
            if 'volumechart' in content.lower():
                print("✅ Volume chart element found")
            else:
                print("❌ Volume chart element not found")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask server. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    test_stock_comparison()
