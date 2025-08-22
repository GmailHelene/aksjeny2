#!/usr/bin/env python3
"""Test search functionality"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.data_service import DataService

def test_search_functionality():
    """Test search to see if it works"""
    print("Testing search functionality...")
    
    # Test DataService search
    try:
        results = DataService.search_stocks('tesla')
        print(f"Search results for 'tesla': {len(results)} found")
        for result in results[:3]:
            print(f"  - {result}")
    except Exception as e:
        print(f"ERROR in DataService.search_stocks: {e}")
        import traceback
        traceback.print_exc()
    
    # Test with Flask app context
    try:
        app = create_app()
        with app.test_client() as client:
            print("\nTesting search endpoint...")
            response = client.get('/stocks/search?q=tesla')
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Search endpoint working")
            else:
                print(f"❌ Search endpoint failed: {response.data}")
    except Exception as e:
        print(f"ERROR in Flask search endpoint: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_search_functionality()
