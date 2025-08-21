#!/usr/bin/env python3
"""
Comprehensive test script to check all reported 500 error routes
and attempt to fix them systematically.
"""

import requests
import json
from datetime import datetime

# List of URLs that reportedly give 500 errors
error_urls = [
    '/profile',
    '/compare', 
    '/forum',
    '/analysis/ai',
    '/norwegian-intel/social-sentiment',
    '/norwegian-intel/government-impact',
    '/external-data/analyst-coverage',
    '/external-data/market-intelligence',
    '/market-intel/economic-indicators',
    '/market-intel/sector-analysis',
    '/market-intel/earnings-calendar',
    '/stocks/compare',
    '/norwegian-intel/oil-correlation',
    '/norwegian-intel/shipping-intelligence',
    '/portfolio/overview',
    '/portfolio/analytics',
    '/forum/category/test',
    '/forum/topic/test',
    '/forum/search?q=test'
]

def test_url(base_url, endpoint):
    """Test a single URL and return status"""
    try:
        url = f"{base_url}{endpoint}"
        response = requests.get(url, timeout=10)
        return {
            'url': endpoint,
            'status_code': response.status_code,
            'success': response.status_code == 200,
            'error': None
        }
    except Exception as e:
        return {
            'url': endpoint,
            'status_code': None,
            'success': False,
            'error': str(e)
        }

def main():
    # Test against local development server
    base_url = "http://localhost:5000"
    
    print("🔍 Testing all reported 500 error URLs...")
    print("=" * 60)
    
    results = []
    working_urls = []
    broken_urls = []
    
    for url in error_urls:
        print(f"Testing: {url}")
        result = test_url(base_url, url)
        results.append(result)
        
        if result['success']:
            working_urls.append(url)
            print(f"  ✅ OK - Status: {result['status_code']}")
        else:
            broken_urls.append(url)
            if result['error']:
                print(f"  ❌ ERROR - {result['error']}")
            else:
                print(f"  ❌ HTTP {result['status_code']}")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total URLs tested: {len(error_urls)}")
    print(f"Working URLs: {len(working_urls)}")
    print(f"Broken URLs: {len(broken_urls)}")
    
    if working_urls:
        print(f"\n✅ Working URLs ({len(working_urls)}):")
        for url in working_urls:
            print(f"  - {url}")
    
    if broken_urls:
        print(f"\n❌ Broken URLs ({len(broken_urls)}):")
        for url in broken_urls:
            print(f"  - {url}")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"url_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total_tested': len(error_urls),
            'working_count': len(working_urls),
            'broken_count': len(broken_urls),
            'working_urls': working_urls,
            'broken_urls': broken_urls,
            'detailed_results': results
        }, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: {filename}")
    
    return len(broken_urls) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
