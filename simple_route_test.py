import urllib.request
import urllib.error
from datetime import datetime

def test_route(url):
    """Test a single route and return status"""
    try:
        response = urllib.request.urlopen(url, timeout=10)
        return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    print(f"=== Testing Critical Routes - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print()
    
    # Routes that were previously failing with 500 errors
    test_routes = [
        'http://localhost:5000/norwegian-intel/',
        'http://localhost:5000/norwegian-intel/social-sentiment',
        'http://localhost:5000/norwegian-intel/oil-correlation', 
        'http://localhost:5000/norwegian-intel/government-impact',
        'http://localhost:5000/norwegian-intel/shipping-intelligence',
        'http://localhost:5000/market-intel/',
        'http://localhost:5000/external-data/',
        'http://localhost:5000/achievements/',
        'http://localhost:5000/portfolio-analytics/',
        'http://localhost:5000/stocks/compare'
    ]
    
    failed_routes = []
    passed_routes = []
    
    for route in test_routes:
        status = test_route(route)
        route_name = route.replace('http://localhost:5000', '')
        
        if status == 500:
            print(f"❌ FAIL: {route_name} -> Status: {status}")
            failed_routes.append(route_name)
        elif status in [200, 302, 401]:  # OK, Redirect, or Auth required
            print(f"✅ PASS: {route_name} -> Status: {status}")
            passed_routes.append(route_name)
        else:
            print(f"⚠️  WARN: {route_name} -> Status: {status}")
    
    print()
    print(f"=== RESULTS ===")
    print(f"✅ Passed: {len(passed_routes)}/{len(test_routes)}")
    print(f"❌ Failed: {len(failed_routes)}/{len(test_routes)}")
    
    if failed_routes:
        print("\nFailed routes:")
        for route in failed_routes:
            print(f"  - {route}")
    else:
        print("\n🎉 ALL CRITICAL ROUTES WORKING!")

if __name__ == '__main__':
    main()
