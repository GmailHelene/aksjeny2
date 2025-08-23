#!/usr/bin/env python3
"""Test script to verify search functionality is working correctly"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_data_service_search():
    """Test DataService.search_stocks directly"""
    try:
        from services.data_service import DataService
        
        print("Testing DataService.search_stocks()...")
        
        # Test searches
        test_queries = ['tesla', 'TSLA', 'apple', 'AAPL', 'microsoft', 'MSFT']
        
        for query in test_queries:
            print(f"\n=== Testing query: '{query}' ===")
            results = DataService.search_stocks(query)
            
            if results:
                print(f"Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result.get('ticker', 'N/A')} - {result.get('name', 'N/A')}")
            else:
                print(f"❌ No results found for '{query}'")
        
        print("\n" + "="*50)
        print("✅ DataService search test completed")
        
    except Exception as e:
        print(f"❌ Error testing DataService: {e}")
        import traceback
        traceback.print_exc()

def test_fallback_data():
    """Test that fallback data is accessible"""
    try:
        from services.data_service import FALLBACK_GLOBAL_DATA, FALLBACK_OSLO_DATA
        
        print(f"\nFALLBACK_GLOBAL_DATA contains {len(FALLBACK_GLOBAL_DATA)} stocks:")
        for ticker, data in list(FALLBACK_GLOBAL_DATA.items())[:5]:
            print(f"  {ticker}: {data['name']}")
        
        print(f"\nFALLBACK_OSLO_DATA contains {len(FALLBACK_OSLO_DATA)} stocks:")
        for ticker, data in list(FALLBACK_OSLO_DATA.items())[:5]:
            print(f"  {ticker}: {data['name']}")
            
        # Check specifically for Tesla
        if 'TSLA' in FALLBACK_GLOBAL_DATA:
            tesla_data = FALLBACK_GLOBAL_DATA['TSLA']
            print(f"\n✅ Tesla found in fallback data: {tesla_data['name']}")
        else:
            print(f"\n❌ Tesla NOT found in fallback data")
            
    except Exception as e:
        print(f"❌ Error testing fallback data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing stock search functionality...")
    test_fallback_data()
    test_data_service_search()
