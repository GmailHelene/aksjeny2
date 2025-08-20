"""
Simple test to check Oslo stocks count using built-in urllib
"""
import urllib.request
import json
import sys

def test_oslo_stocks():
    try:
        print("Testing Oslo stocks count...")
        with urllib.request.urlopen('http://localhost:5000/api/data/oslo-bors') as response:
            data = json.loads(response.read().decode())
            stock_count = len(data.get('data', []))
            print(f"Oslo stocks count: {stock_count}")
            
            if stock_count >= 40:
                print("✅ PASS: Oslo stocks showing 40+ companies")
            else:
                print(f"❌ FAIL: Only showing {stock_count} companies (expected 40+)")
                
            return stock_count
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return 0

if __name__ == "__main__":
    count = test_oslo_stocks()
    print(f"\nResult: {count} Oslo stocks found")
