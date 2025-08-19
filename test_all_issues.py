#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_all_reported_issues():
    """Test all the issues reported by the user"""
    
    print("🔍 Testing All Reported Issues")
    print("=" * 60)
    
    base_url = "https://aksjeradar.trade"
    
    # Test scenarios
    test_cases = [
        {
            "name": "Warren Buffett Analysis",
            "url": f"{base_url}/analysis/warren-buffett?ticker=KO",
            "expected_content": ["warren", "buffett", "analysis", "ko"],
            "should_not_contain": ["error", "prøv igjen senere"]
        },
        {
            "name": "Stock Details - EQNR.OL", 
            "url": f"{base_url}/stocks/details/EQNR.OL",
            "expected_content": ["eqnr", "equinor"],
            "should_not_contain": ["feil ved lasting", "500"]
        },
        {
            "name": "Financial Dashboard",
            "url": f"{base_url}/financial-dashboard",
            "expected_content": ["innsidehandel", "nyheter", "aksjer", "valuta"],
            "should_not_contain": ["error", "ikke tilgjengelig"]
        },
        {
            "name": "Settings Page",
            "url": f"{base_url}/settings", 
            "expected_content": ["varsler", "innstillinger"],
            "should_not_contain": ["error"]
        },
        {
            "name": "Index Page (Homepage)",
            "url": f"{base_url}/",
            "expected_content": ["aksjeradar"],
            "should_not_contain": ["500", "server error"]
        },
        {
            "name": "Crypto List",
            "url": f"{base_url}/stocks/list/crypto",
            "expected_content": ["crypto", "bitcoin", "krypto"],
            "should_not_contain": ["500", "server error"]
        },
        {
            "name": "Currency List", 
            "url": f"{base_url}/stocks/list/currency",
            "expected_content": ["currency", "usd", "valuta"],
            "should_not_contain": ["500", "server error"]
        },
        {
            "name": "Global Stocks List",
            "url": f"{base_url}/stocks/list/global",
            "expected_content": ["global", "aapl", "stocks"],
            "should_not_contain": ["500", "server error"]
        },
        {
            "name": "Sentiment Analysis",
            "url": f"{base_url}/analysis/sentiment?symbol=DNB.OL",
            "expected_content": ["sentiment", "dnb"],
            "should_not_contain": ["nameerror", "requests", "not defined"]
        }
    ]
    
    results = []
    
    for test in test_cases:
        print(f"\n📋 Testing: {test['name']}")
        print(f"   URL: {test['url']}")
        
        try:
            response = requests.get(test['url'], timeout=30, allow_redirects=True)
            
            result = {
                "name": test['name'],
                "url": test['url'], 
                "status_code": response.status_code,
                "success": False,
                "issues": [],
                "content_length": len(response.content)
            }
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for expected content
                expected_found = []
                for expected in test['expected_content']:
                    if expected.lower() in content:
                        expected_found.append(expected)
                
                # Check for content that should not be present
                unwanted_found = []
                for unwanted in test['should_not_contain']:
                    if unwanted.lower() in content:
                        unwanted_found.append(unwanted)
                
                if expected_found and not unwanted_found:
                    result['success'] = True
                    print(f"   ✅ SUCCESS - Found expected content: {expected_found}")
                else:
                    if not expected_found:
                        result['issues'].append(f"Missing expected content: {test['expected_content']}")
                        print(f"   ⚠️  Missing expected content: {test['expected_content']}")
                    if unwanted_found:
                        result['issues'].append(f"Found unwanted content: {unwanted_found}")
                        print(f"   ❌ Found unwanted content: {unwanted_found}")
                        
            elif response.status_code == 500:
                result['issues'].append("500 Server Error")
                print(f"   ❌ 500 SERVER ERROR - Issue still exists!")
                
            elif response.status_code == 302:
                redirect_url = response.headers.get('Location', 'Unknown')
                print(f"   🔄 REDIRECT to: {redirect_url}")
                if "login" in redirect_url.lower():
                    result['issues'].append("Requires authentication")
                    
            else:
                result['issues'].append(f"Unexpected status code: {response.status_code}")
                print(f"   ⚠️  Status: {response.status_code}")
                
            results.append(result)
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results.append({
                "name": test['name'],
                "url": test['url'],
                "status_code": None,
                "success": False,
                "issues": [str(e)],
                "content_length": 0
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    print("\n🔴 Issues that still need fixing:")
    for result in results:
        if not result['success']:
            print(f"   - {result['name']}: {', '.join(result['issues'])}")
    
    print("\n✅ Working correctly:")
    for result in results:
        if result['success']:
            print(f"   - {result['name']}")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"production_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    test_all_reported_issues()
