#!/usr/bin/env python3
"""
Final verification script for stock search and compare functionality
Run this after deployment to verify all fixes are working
"""
import requests
import time
import json

def test_search_functionality():
    """Test that search pages load and work correctly"""
    print("🔍 TESTING SEARCH FUNCTIONALITY")
    print("=" * 50)
    
    test_cases = [
        {
            'url': 'https://aksjeradar.trade/stocks/search?q=tesla',
            'query': 'tesla',
            'expected_in_content': ['søk', 'tesla', 'search'],
            'should_not_contain': ['demo-modus aktivert', 'prøv alle aksjeradar funksjoner']
        },
        {
            'url': 'https://aksjeradar.trade/stocks/search?q=TSLA', 
            'query': 'TSLA',
            'expected_in_content': ['søk', 'tsla', 'search'],
            'should_not_contain': ['demo-modus aktivert', 'prøv alle aksjeradar funksjoner']
        },
        {
            'url': 'https://aksjeradar.trade/stocks/search?q=apple',
            'query': 'apple', 
            'expected_in_content': ['søk', 'apple', 'search'],
            'should_not_contain': ['demo-modus aktivert', 'prøv alle aksjeradar funksjoner']
        },
        {
            'url': 'https://aksjeradar.trade/stocks/search',
            'query': 'empty',
            'expected_in_content': ['søk', 'search', 'form'],
            'should_not_contain': ['demo-modus aktivert', 'prøv alle aksjeradar funksjoner']
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['url']}")
        try:
            response = requests.get(test_case['url'], timeout=10)
            content = response.text.lower()
            
            # Check if it's still showing demo content
            is_demo_content = any(term in content for term in test_case['should_not_contain'])
            
            # Check if it has expected search content
            has_search_content = any(term in content for term in test_case['expected_in_content'])
            
            if is_demo_content:
                result = f"❌ STILL SHOWING DEMO CONTENT"
                status = "FAIL"
            elif has_search_content:
                result = f"✅ SEARCH PAGE WORKING"
                status = "PASS"
            else:
                result = f"❓ UNCLEAR CONTENT"
                status = "UNKNOWN"
                
            print(f"   Status: {response.status_code}")
            print(f"   Result: {result}")
            
            results.append({
                'url': test_case['url'],
                'query': test_case['query'],
                'status': status,
                'result': result,
                'response_code': response.status_code
            })
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append({
                'url': test_case['url'],
                'query': test_case['query'], 
                'status': 'ERROR',
                'result': f"Request failed: {e}",
                'response_code': None
            })
    
    return results

def test_compare_functionality():
    """Test that compare page loads correctly"""
    print("\n🔗 TESTING COMPARE FUNCTIONALITY") 
    print("=" * 50)
    
    test_urls = [
        'https://aksjeradar.trade/stocks/compare',
        'https://aksjeradar.trade/stocks/compare?symbols=TSLA,AAPL'
    ]
    
    results = []
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        try:
            response = requests.get(url, timeout=10)
            content = response.text.lower()
            
            # Check if it's still showing demo content
            is_demo_content = 'demo-modus aktivert' in content or 'prøv alle aksjeradar funksjoner' in content
            
            # Check if it has expected compare content  
            has_compare_content = any(term in content for term in ['sammenlign', 'compare', 'chart', 'aksje'])
            
            if is_demo_content:
                result = f"❌ STILL SHOWING DEMO CONTENT"
                status = "FAIL"
            elif has_compare_content:
                result = f"✅ COMPARE PAGE WORKING"
                status = "PASS"
            else:
                result = f"❓ UNCLEAR CONTENT"
                status = "UNKNOWN"
                
            print(f"   Status: {response.status_code}")
            print(f"   Result: {result}")
            
            results.append({
                'url': url,
                'status': status,
                'result': result,
                'response_code': response.status_code
            })
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append({
                'url': url,
                'status': 'ERROR', 
                'result': f"Request failed: {e}",
                'response_code': None
            })
    
    return results

def generate_report(search_results, compare_results):
    """Generate final verification report"""
    print("\n📊 FINAL VERIFICATION REPORT")
    print("=" * 50)
    
    # Count results
    search_pass = sum(1 for r in search_results if r['status'] == 'PASS')
    search_total = len(search_results)
    compare_pass = sum(1 for r in compare_results if r['status'] == 'PASS') 
    compare_total = len(compare_results)
    
    print(f"\nSearch Functionality: {search_pass}/{search_total} tests passed")
    print(f"Compare Functionality: {compare_pass}/{compare_total} tests passed")
    
    total_pass = search_pass + compare_pass
    total_tests = search_total + compare_total
    
    if total_pass == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! ({total_pass}/{total_tests})")
        print("✅ Stock search and compare functionality is working correctly!")
    elif total_pass > 0:
        print(f"\n⚠️  PARTIAL SUCCESS ({total_pass}/{total_tests} tests passed)")
        print("Some functionality is working, but issues remain.")
    else:
        print(f"\n❌ ALL TESTS FAILED (0/{total_tests})")
        print("Deployment may not have completed or there are remaining issues.")
    
    # Save detailed results
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'search_results': search_results,
        'compare_results': compare_results,
        'summary': {
            'search_pass': search_pass,
            'search_total': search_total,
            'compare_pass': compare_pass,
            'compare_total': compare_total,
            'overall_pass': total_pass,
            'overall_total': total_tests
        }
    }
    
    return report

if __name__ == "__main__":
    print("🚀 STOCK SEARCH & COMPARE VERIFICATION")
    print("=" * 60)
    print("This script verifies that the stock search and compare fixes are working")
    print("Run this after deployment to confirm functionality")
    print("=" * 60)
    
    search_results = test_search_functionality()
    compare_results = test_compare_functionality()
    report = generate_report(search_results, compare_results)
    
    # Save report to file
    with open('verification_results.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed results saved to verification_results.json")
    print("\n🏁 Verification complete!")
