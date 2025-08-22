#!/usr/bin/env python3
"""
Comprehensive test for access control fixes
Tests all routes that were changed from @demo_access to @access_required
"""

import sys
import os
import requests
from urllib.parse import urljoin
import json

# Add the app to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_access_control():
    """Test that all critical routes now use proper access control"""
    
    # Base URL - adjust if needed
    base_url = "http://localhost:5000"
    
    # Critical routes that should now require paid access
    critical_routes = [
        # Analysis routes
        '/analysis/sentiment',
        '/analysis/warren-buffett', 
        '/analysis/insider-trading',
        '/analysis/short-analysis/AAPL',
        '/analysis/recommendations/AAPL',
        '/analysis/tradingview',
        
        # Portfolio routes  
        '/portfolio/overview',
        '/portfolio/add',
        
        # Watchlist routes
        '/watchlist',
        
        # Market intel routes
        '/market_intel/insider-trading',
        '/market_intel/earnings-calendar',
        
        # Achievements routes
        '/achievements/',
        
        # Stock search
        '/stocks/search',
        
        # Crypto dashboard routes
        '/advanced/crypto-dashboard',
        '/advanced-features/crypto-dashboard',
        
        # API routes that should require access
        '/api/watchlist/add',
        '/achievements/api/progress',
        '/achievements/api/update_stat',
        '/advanced-features/api/crypto-dashboard'
    ]
    
    print("🔍 Testing Access Control for Critical Routes")
    print("=" * 60)
    
    results = {
        'total_routes': len(critical_routes),
        'tested': 0,
        'accessible_without_auth': [],
        'require_auth': [],
        'errors': []
    }
    
    for route in critical_routes:
        print(f"\n📍 Testing: {route}")
        results['tested'] += 1
        
        try:
            # Test without authentication
            url = urljoin(base_url, route)
            response = requests.get(url, allow_redirects=False, timeout=10)
            
            # Check response
            if response.status_code == 401:
                print(f"   ✅ Correctly requires authentication (401)")
                results['require_auth'].append(route)
            elif response.status_code == 302:
                # Check if redirecting to login
                location = response.headers.get('Location', '')
                if 'login' in location.lower() or 'auth' in location.lower():
                    print(f"   ✅ Correctly redirects to login (302)")
                    results['require_auth'].append(route)
                else:
                    print(f"   ⚠️  Redirects but not to login: {location}")
                    results['accessible_without_auth'].append(route)
            elif response.status_code == 200:
                print(f"   ❌ Accessible without authentication (200)")
                results['accessible_without_auth'].append(route)
            else:
                print(f"   ❓ Unexpected status: {response.status_code}")
                results['errors'].append(f"{route}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   💥 Request failed: {e}")
            results['errors'].append(f"{route}: {str(e)}")
        except Exception as e:
            print(f"   🚨 Unexpected error: {e}")
            results['errors'].append(f"{route}: {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ACCESS CONTROL TEST SUMMARY")
    print("=" * 60)
    print(f"Total routes tested: {results['total_routes']}")
    print(f"Successfully tested: {results['tested']}")
    print(f"Properly protected: {len(results['require_auth'])}")
    print(f"Incorrectly accessible: {len(results['accessible_without_auth'])}")
    print(f"Errors encountered: {len(results['errors'])}")
    
    if results['accessible_without_auth']:
        print(f"\n❌ ROUTES STILL ACCESSIBLE WITHOUT AUTH:")
        for route in results['accessible_without_auth']:
            print(f"   - {route}")
    
    if results['errors']:
        print(f"\n⚠️  ERRORS ENCOUNTERED:")
        for error in results['errors']:
            print(f"   - {error}")
    
    if results['require_auth']:
        print(f"\n✅ PROPERLY PROTECTED ROUTES:")
        for route in results['require_auth']:
            print(f"   - {route}")
    
    # Calculate success rate
    success_rate = (len(results['require_auth']) / results['tested']) * 100 if results['tested'] > 0 else 0
    print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🏆 EXCELLENT! Access control is properly implemented.")
    elif success_rate >= 75:
        print("👍 GOOD! Most routes are properly protected.")
    else:
        print("⚠️  NEEDS WORK! Several routes still lack proper protection.")
    
    return results

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Access Control Test")
    print("This will test all routes that were updated from @demo_access to @access_required")
    print()
    
    try:
        results = test_access_control()
        
        # Save results to file
        with open('access_control_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: access_control_test_results.json")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)
