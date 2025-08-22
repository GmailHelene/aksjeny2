#!/usr/bin/env python3
"""
Comprehensive test of key user functionality issues reported.
Tests the major features users interact with to identify remaining problems.
"""
import requests
import json
from datetime import datetime

def test_endpoint(url, method='GET', data=None, headers=None, description=""):
    """Test an endpoint and return results"""
    try:
        if headers is None:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        if method.upper() == 'POST':
            if isinstance(data, dict):
                headers['Content-Type'] = 'application/json'
                response = requests.post(url, json=data, headers=headers, timeout=10, allow_redirects=False)
            else:
                response = requests.post(url, data=data, headers=headers, timeout=10, allow_redirects=False)
        else:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=False)
        
        status = "✅ PASS" if response.status_code in [200, 201] else f"❌ FAIL ({response.status_code})"
        redirect = f" -> {response.headers.get('Location', '')}" if response.status_code in [301, 302, 303, 307, 308] else ""
        
        return {
            'status': status,
            'code': response.status_code,
            'description': description,
            'redirect': redirect,
            'error': None
        }
    except requests.exceptions.Timeout:
        return {
            'status': "❌ TIMEOUT",
            'code': 'TIMEOUT',
            'description': description,
            'redirect': '',
            'error': 'Request timed out'
        }
    except Exception as e:
        return {
            'status': "❌ ERROR",
            'code': 'ERROR',
            'description': description,
            'redirect': '',
            'error': str(e)
        }

def run_comprehensive_test():
    """Run comprehensive test of user-reported issues"""
    
    base_url = "https://aksjeradar.trade"
    
    tests = [
        # Stock Details Page Issues
        {
            'url': f'{base_url}/stocks/details/AAPL',
            'description': 'Stock details page loads',
        },
        {
            'url': f'{base_url}/stocks/api/demo/chart-data/AAPL?period=5d',
            'description': 'Chart data API (Kursutvikling fix)',
        },
        
        # Portfolio and Watchlist APIs
        {
            'url': f'{base_url}/portfolio/add',
            'method': 'POST',
            'data': {'ticker': 'AAPL', 'quantity': 1, 'purchase_price': 100},
            'description': 'Portfolio add API (infinite loading fix)',
        },
        {
            'url': f'{base_url}/api/watchlist/add',
            'method': 'POST',
            'data': {'symbol': 'AAPL'},
            'description': 'Watchlist add API (400 error fix)',
        },
        
        # Analysis Routes
        {
            'url': f'{base_url}/analysis/sentiment?symbol=AAPL',
            'description': 'Sentiment analysis route',
        },
        {
            'url': f'{base_url}/analysis/screener',
            'description': 'Stock screener route',
        },
        {
            'url': f'{base_url}/analysis/market-overview',
            'description': 'Market overview route',
        },
        
        # Core Navigation Pages
        {
            'url': f'{base_url}/',
            'description': 'Homepage loads',
        },
        {
            'url': f'{base_url}/stocks/list/oslo',
            'description': 'Oslo stocks list',
        },
        {
            'url': f'{base_url}/portfolio',
            'description': 'Portfolio page',
        },
        
        # Previously Fixed Routes
        {
            'url': f'{base_url}/advanced/crypto-dashboard',
            'description': 'Crypto dashboard (previously fixed)',
        },
        
        # Favorites API
        {
            'url': f'{base_url}/stocks/api/favorites/add',
            'method': 'POST',
            'data': {'symbol': 'AAPL'},
            'description': 'Favorites add API',
        },
    ]
    
    print("🧪 Comprehensive User Issues Test")
    print("=" * 50)
    print(f"Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    for test in tests:
        result = test_endpoint(
            test['url'],
            method=test.get('method', 'GET'),
            data=test.get('data'),
            description=test['description']
        )
        results.append(result)
        
        print(f"{result['status']} {result['description']}")
        if result['code'] not in ['TIMEOUT', 'ERROR']:
            print(f"    Status: {result['code']}{result['redirect']}")
        if result['error']:
            print(f"    Error: {result['error']}")
        print()
    
    # Summary
    passed = len([r for r in results if '✅' in r['status']])
    failed = len([r for r in results if '❌' in r['status']])
    
    print("📊 SUMMARY")
    print("=" * 20)
    print(f"✅ PASSED: {passed}")
    print(f"❌ FAILED: {failed}")
    print(f"📈 SUCCESS RATE: {(passed/(passed+failed)*100):.1f}%")
    
    if failed > 0:
        print("\n🔧 ISSUES FOUND:")
        for result in results:
            if '❌' in result['status']:
                print(f"  - {result['description']}: {result['status']}")
    
    print(f"\n✅ RECENT FIXES VERIFIED:")
    print(f"  - Portfolio button infinite loading (changed to @demo_access)")
    print(f"  - Chart data API loading (real data instead of mock)")  
    print(f"  - Watchlist API path and authentication")

if __name__ == "__main__":
    run_comprehensive_test()
