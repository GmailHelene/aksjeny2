#!/usr/bin/env python3
"""
Comprehensive test for stock search functionality 
Test both access control and search data functionality
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_search_access_control():
    """Test that search routes have proper access control"""
    try:
        from app.utils.access_control import public_endpoints
        from app.routes.main import EXEMPT_ENDPOINTS, PREMIUM_ENDPOINTS
        
        print("=== TESTING ACCESS CONTROL ===")
        
        # Check that stocks.search is in public_endpoints
        if 'stocks.search' in public_endpoints:
            print("✅ stocks.search is in public_endpoints")
        else:
            print("❌ stocks.search NOT in public_endpoints")
            
        # Check that stocks.compare is in public_endpoints  
        if 'stocks.compare' in public_endpoints:
            print("✅ stocks.compare is in public_endpoints")
        else:
            print("❌ stocks.compare NOT in public_endpoints")
            
        # Check EXEMPT_ENDPOINTS
        if 'stocks.search' in EXEMPT_ENDPOINTS:
            print("✅ stocks.search is in EXEMPT_ENDPOINTS")
        else:
            print("❌ stocks.search NOT in EXEMPT_ENDPOINTS")
            
        # Check PREMIUM_ENDPOINTS
        if 'stocks.compare' not in PREMIUM_ENDPOINTS:
            print("✅ stocks.compare NOT in PREMIUM_ENDPOINTS (correct)")
        else:
            print("❌ stocks.compare is in PREMIUM_ENDPOINTS (wrong)")
            
        print(f"Public endpoints count: {len(public_endpoints)}")
        print(f"Exempt endpoints count: {len(EXEMPT_ENDPOINTS)}")
        print(f"Premium endpoints count: {len(PREMIUM_ENDPOINTS)}")
        
    except Exception as e:
        print(f"❌ Error testing access control: {e}")
        import traceback
        traceback.print_exc()

def test_search_data_service():
    """Test that search data service works correctly"""
    try:
        from app.services.data_service import DataService, FALLBACK_GLOBAL_DATA, FALLBACK_OSLO_DATA
        
        print("\n=== TESTING SEARCH DATA SERVICE ===")
        
        # Test Tesla search specifically
        print("\nTesting tesla search...")
        tesla_results = DataService.search_stocks('tesla')
        if tesla_results:
            print(f"✅ Tesla search returned {len(tesla_results)} results:")
            for result in tesla_results:
                print(f"  - {result.get('ticker', 'N/A')}: {result.get('name', 'N/A')}")
        else:
            print("❌ Tesla search returned no results")
            
        # Test TSLA search  
        print("\nTesting TSLA search...")
        tsla_results = DataService.search_stocks('TSLA')
        if tsla_results:
            print(f"✅ TSLA search returned {len(tsla_results)} results:")
            for result in tsla_results:
                print(f"  - {result.get('ticker', 'N/A')}: {result.get('name', 'N/A')}")
        else:
            print("❌ TSLA search returned no results")
            
        # Test Apple search
        print("\nTesting apple search...")
        apple_results = DataService.search_stocks('apple')
        if apple_results:
            print(f"✅ Apple search returned {len(apple_results)} results:")
            for result in apple_results:
                print(f"  - {result.get('ticker', 'N/A')}: {result.get('name', 'N/A')}")
        else:
            print("❌ Apple search returned no results")
            
        # Verify fallback data contains Tesla
        if 'TSLA' in FALLBACK_GLOBAL_DATA:
            tesla_data = FALLBACK_GLOBAL_DATA['TSLA']
            print(f"\n✅ Tesla found in fallback data: {tesla_data['name']}")
        else:
            print("\n❌ Tesla NOT found in fallback data")
            
        print(f"\nGlobal fallback data contains {len(FALLBACK_GLOBAL_DATA)} stocks")
        print(f"Oslo fallback data contains {len(FALLBACK_OSLO_DATA)} stocks")
        
    except Exception as e:
        print(f"❌ Error testing search data service: {e}")
        import traceback
        traceback.print_exc()

def test_stocks_route():
    """Test stocks route configuration"""
    try:
        from app.routes.stocks import stocks
        
        print("\n=== TESTING STOCKS ROUTE ===")
        
        # Get all routes in the stocks blueprint
        routes = []
        for rule in stocks.url_map.iter_rules():
            routes.append(str(rule))
            
        print(f"Stocks blueprint routes: {routes}")
        
        # Check if search route exists
        search_found = any('/search' in route for route in routes)
        compare_found = any('/compare' in route for route in routes)
        
        if search_found:
            print("✅ Search route found in stocks blueprint")
        else:
            print("❌ Search route NOT found in stocks blueprint")
            
        if compare_found:
            print("✅ Compare route found in stocks blueprint")
        else:
            print("❌ Compare route NOT found in stocks blueprint")
            
    except Exception as e:
        print(f"❌ Error testing stocks route: {e}")
        import traceback
        traceback.print_exc()

def test_route_decorators():
    """Test that routes have correct decorators"""
    try:
        import inspect
        from app.routes.stocks import search, compare
        
        print("\n=== TESTING ROUTE DECORATORS ===")
        
        # Get source code to check decorators
        search_source = inspect.getsource(search)
        compare_source = inspect.getsource(compare)
        
        if '@demo_access' in search_source:
            print("✅ Search route has @demo_access decorator")
        else:
            print("❌ Search route missing @demo_access decorator")
            
        if '@demo_access' in compare_source:
            print("✅ Compare route has @demo_access decorator")
        else:
            print("❌ Compare route missing @demo_access decorator")
            
        # Check for access_required (should NOT be present)
        if '@access_required' not in search_source:
            print("✅ Search route does NOT have @access_required (correct)")
        else:
            print("❌ Search route has @access_required (wrong)")
            
    except Exception as e:
        print(f"❌ Error testing route decorators: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 COMPREHENSIVE SEARCH FUNCTIONALITY TEST")
    print("=" * 50)
    
    test_search_access_control()
    test_search_data_service()
    test_stocks_route()
    test_route_decorators()
    
    print("\n" + "=" * 50)
    print("🎯 Test completed! Check results above.")
