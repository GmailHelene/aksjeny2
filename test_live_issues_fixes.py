#!/usr/bin/env python3
"""
Test script to verify fixes for specific live site issues
"""

import requests
import json
from datetime import datetime
from urllib.parse import urljoin

# Base URL for the local development server
BASE_URL = "http://localhost:5001"

def test_endpoint(url, description, expected_status=200):
    """Test an endpoint and return results"""
    try:
        full_url = urljoin(BASE_URL, url)
        print(f"\n🔍 Testing: {description}")
        print(f"   URL: {full_url}")
        
        response = requests.get(full_url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"   ✅ Status: {response.status_code} (Expected: {expected_status})")
            
            # Check if it's HTML content
            if 'text/html' in response.headers.get('content-type', ''):
                # Look for common error indicators
                content = response.text.lower()
                if 'error' in content and 'feil' in content:
                    print(f"   ⚠️  Warning: Page contains error messages")
                elif 'kan ikke laste' in content:
                    print(f"   ❌ Error: Page shows 'kan ikke laste' message")
                    return False
                elif 'stock_info' in content and 'undefined' in content:
                    print(f"   ❌ Error: Template has undefined stock_info variable")
                    return False
                else:
                    print(f"   ✅ Content: Looks good, no obvious errors")
            
            return True
        else:
            print(f"   ❌ Status: {response.status_code} (Expected: {expected_status})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")
        return False

def main():
    """Test all the reported live site issues"""
    print("🧪 Testing Live Site Issues Fixes")
    print("=" * 50)
    
    test_results = {}
    
    # Test cases based on user's reported issues
    test_cases = [
        {
            'url': '/portfolio/overview',
            'description': 'Portfolio Overview - "kan ikke laste" fix',
            'key': 'portfolio_overview'
        },
        {
            'url': '/news/',
            'description': 'News page - oversized images fix',
            'key': 'news_images'
        },
        {
            'url': '/advanced/crypto-dashboard',
            'description': 'Crypto Dashboard implementation',
            'key': 'crypto_dashboard'
        },
        {
            'url': '/analysis/technical?symbol=TEL.OL',
            'description': 'Technical Analysis - TEL.OL symbol validation',
            'key': 'technical_analysis_symbol'
        },
        {
            'url': '/analysis/screener',
            'description': 'Screener page functionality',
            'key': 'screener'
        },
        {
            'url': '/analysis/fundamental?ticker=AAPL',
            'description': 'Fundamental Analysis - stock_info undefined fix',
            'key': 'fundamental_analysis'
        },
        {
            'url': '/analysis/fundamental?ticker=TEL.OL',
            'description': 'Fundamental Analysis - Oslo symbol test',
            'key': 'fundamental_oslo'
        },
        {
            'url': '/analysis/',
            'description': 'Analysis main page',
            'key': 'analysis_main'
        },
        {
            'url': '/portfolio/',
            'description': 'Portfolio main page',
            'key': 'portfolio_main'
        },
        {
            'url': '/analysis/market-overview',
            'description': 'Market Overview page',
            'key': 'market_overview'
        }
    ]
    
    # Run tests
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        result = test_endpoint(
            test_case['url'], 
            test_case['description']
        )
        test_results[test_case['key']] = result
        if result:
            passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 Test Results Summary")
    print("=" * 50)
    
    for test_case in test_cases:
        key = test_case['key']
        status = "✅ PASS" if test_results[key] else "❌ FAIL"
        print(f"{status} - {test_case['description']}")
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All issues appear to be fixed!")
    else:
        print(f"⚠️  {total - passed} issues still need attention")
    
    # Save detailed results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f'live_issues_test_results_{timestamp}.json'
    
    detailed_results = {
        'timestamp': timestamp,
        'total_tests': total,
        'passed_tests': passed,
        'test_results': test_results,
        'test_cases': test_cases
    }
    
    with open(results_file, 'w') as f:
        json.dump(detailed_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()
