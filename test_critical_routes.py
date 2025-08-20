#!/usr/bin/env python3
"""
Critical Routes Testing Script
=============================

Tests all routes that were previously returning 500 errors
to verify that the demo_access decorator fixes are working.
"""

import requests
import sys
from datetime import datetime

def test_critical_routes():
    """Test all critical routes that were reported as 500 errors"""
    
    # Routes that were previously failing with 500 errors
    test_routes = [
        # Norwegian Intel routes (recently fixed)
        'http://localhost:5000/norwegian-intel/',
        'http://localhost:5000/norwegian-intel/social-sentiment',
        'http://localhost:5000/norwegian-intel/oil-correlation', 
        'http://localhost:5000/norwegian-intel/government-impact',
        'http://localhost:5000/norwegian-intel/shipping-intelligence',
        
        # Market Intel routes
        'http://localhost:5000/market-intel/',
        'http://localhost:5000/market-intel/sector-analysis',
        'http://localhost:5000/market-intel/insider-trading',
        'http://localhost:5000/market-intel/technical-overview',
        
        # External Data routes
        'http://localhost:5000/external-data/',
        'http://localhost:5000/external-data/global-markets',
        'http://localhost:5000/external-data/economic-calendar',
        
        # Achievements routes
        'http://localhost:5000/achievements/',
        
        # Portfolio Analytics routes  
        'http://localhost:5000/portfolio-analytics/',
        
        # Stocks compare
        'http://localhost:5000/stocks/compare'
    ]

    print(f'=== Testing Critical Routes - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ===')
    print()

    failed_routes = []
    passed_routes = []
    warning_routes = []

    for route in test_routes:
        try:
            response = requests.get(route, timeout=10, allow_redirects=False)
            status = response.status_code
            
            if status == 500:
                print(f'❌ FAIL: {route} -> Status: {status}')
                failed_routes.append(route)
            elif status in [200]:  # OK
                print(f'✅ PASS: {route} -> Status: {status}')
                passed_routes.append(route)
            elif status in [302, 401]:  # Redirect or Auth required - route works
                print(f'✅ PASS: {route} -> Status: {status} (redirect/auth)')
                passed_routes.append(route)
            else:
                print(f'⚠️  WARN: {route} -> Status: {status}')
                warning_routes.append(route)
                
        except requests.exceptions.ConnectionError:
            print(f'🔌 CONN: {route} -> Server not running')
            failed_routes.append(route)
        except Exception as e:
            print(f'💥 ERROR: {route} -> Exception: {str(e)[:100]}')
            failed_routes.append(route)

    print()
    print(f'=== RESULTS ===')
    print(f'✅ Passed: {len(passed_routes)}/{len(test_routes)}')
    print(f'⚠️  Warnings: {len(warning_routes)}/{len(test_routes)}')
    print(f'❌ Failed: {len(failed_routes)}/{len(test_routes)}')

    if failed_routes:
        print('\nFailed routes:')
        for route in failed_routes:
            print(f'  - {route}')
            
    if warning_routes:
        print('\nWarning routes:')
        for route in warning_routes:
            print(f'  - {route}')

    if len(failed_routes) == 0 and len(warning_routes) == 0:
        print('\n🎉 ALL CRITICAL ROUTES WORKING PERFECTLY!')
        return True
    elif len(failed_routes) == 0:
        print('\n✅ ALL CRITICAL ROUTES ACCESSIBLE (some warnings)')
        return True
    else:
        print(f'\n❌ {len(failed_routes)} routes still have issues')
        return False

if __name__ == '__main__':
    success = test_critical_routes()
    sys.exit(0 if success else 1)
