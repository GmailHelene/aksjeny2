#!/usr/bin/env python3
"""
Critical Endpoint Tester
Test all reported problematic endpoints systematically
"""

import requests
import sys
import time
from datetime import datetime

# List of critical endpoints to test
CRITICAL_ENDPOINTS = [
    {
        'name': 'Stocks Compare',
        'url': 'http://localhost:5002/stocks/compare',
        'issue': '500 error when accessing stocks comparison',
        'test_params': {'symbols': 'EQNR.OL,DNB.OL'}
    },
    {
        'name': 'My Subscription',
        'url': 'http://localhost:5002/my-subscription',
        'issue': 'Loading error on subscription page',
        'test_params': {}
    },
    {
        'name': 'Forum Create Topic',
        'url': 'http://localhost:5002/forum/create_topic',
        'issue': 'Technical error when creating forum topics',
        'test_params': {}
    },
    {
        'name': 'Warren Buffett Analysis',
        'url': 'http://localhost:5002/analysis/warren-buffett',
        'issue': 'Search not working in Warren Buffett analysis',
        'test_params': {}
    },
    {
        'name': 'Advanced Analytics',
        'url': 'http://localhost:5002/advanced-analytics',
        'issue': 'Buttons not working properly',
        'test_params': {}
    },
    {
        'name': 'External Data Analyst Coverage',
        'url': 'http://localhost:5002/external-data/analyst-coverage',
        'issue': 'Buttons and data not working',
        'test_params': {}
    },
    {
        'name': 'Profile Page',
        'url': 'http://localhost:5002/profile',
        'issue': 'Favorites displaying incorrect data',
        'test_params': {}
    },
    {
        'name': 'Health Check',
        'url': 'http://localhost:5002/health',
        'issue': 'Basic health check',
        'test_params': {}
    }
]

# NOTE: Renamed to helper_test_endpoint to avoid pytest collecting this
# diagnostics helper as a real test function.
def helper_test_endpoint(endpoint_info):
    """Test a single endpoint and return results"""
    name = endpoint_info['name']
    url = endpoint_info['url']
    issue = endpoint_info['issue']
    params = endpoint_info.get('test_params', {})
    
    print(f"\n🧪 Testing: {name}")
    print(f"   URL: {url}")
    print(f"   Issue: {issue}")
    
    try:
        # Test with timeout
        response = requests.get(url, params=params, timeout=10, allow_redirects=False)
        
        status_code = response.status_code
        content_length = len(response.content)
        
        if status_code == 200:
            print(f"   ✅ Status: {status_code} (OK)")
            print(f"   📄 Content Length: {content_length} bytes")
            return 'PASS'
        elif status_code in [301, 302, 303, 307, 308]:
            print(f"   ↩️  Status: {status_code} (Redirect)")
            print(f"   🔗 Location: {response.headers.get('Location', 'N/A')}")
            return 'REDIRECT'
        elif status_code == 404:
            print(f"   ❌ Status: {status_code} (Not Found)")
            return 'NOT_FOUND'
        elif status_code == 500:
            print(f"   💥 Status: {status_code} (Internal Server Error)")
            return 'ERROR_500'
        else:
            print(f"   ⚠️  Status: {status_code}")
            return f'HTTP_{status_code}'
            
    except requests.exceptions.ConnectionError:
        print(f"   🔌 Connection Error: Server not responding")
        return 'CONNECTION_ERROR'
    except requests.exceptions.Timeout:
        print(f"   ⏰ Timeout: Request took too long")
        return 'TIMEOUT'
    except Exception as e:
        print(f"   💀 Exception: {str(e)}")
        return 'EXCEPTION'

def wait_for_server(max_attempts=30):
    """Wait for server to become available"""
    print("🕐 Waiting for server to start...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get('http://localhost:5002/health', timeout=2)
            if response.status_code in [200, 404]:  # Either OK or route not found is fine
                print(f"✅ Server is responding after {attempt + 1} attempts")
                return True
        except:
            pass
        
        time.sleep(2)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    print("❌ Server failed to respond")
    return False

def main():
    print("=" * 60)
    print("🚀 CRITICAL ENDPOINT TESTING SYSTEM")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Wait for server
    if not wait_for_server():
        print("\n💀 Cannot proceed without server. Exiting.")
        sys.exit(1)
    
    print(f"\n📊 Testing {len(CRITICAL_ENDPOINTS)} critical endpoints...")
    
    results = {}
    
    for endpoint_info in CRITICAL_ENDPOINTS:
        result = helper_test_endpoint(endpoint_info)
        results[endpoint_info['name']] = result
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    pass_count = 0
    fail_count = 0
    
    for name, result in results.items():
        status_emoji = "✅" if result == 'PASS' else "❌"
        print(f"{status_emoji} {name}: {result}")
        
        if result == 'PASS':
            pass_count += 1
        else:
            fail_count += 1
    
    print(f"\n📊 Total: {len(results)} endpoints")
    print(f"✅ Passed: {pass_count}")
    print(f"❌ Failed: {fail_count}")
    
    if fail_count == 0:
        print("\n🎉 All endpoints are working correctly!")
        return 0
    else:
        print(f"\n⚠️  {fail_count} endpoints need attention!")
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💀 Unexpected error: {e}")
        sys.exit(1)
