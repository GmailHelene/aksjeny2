#!/usr/bin/env python3
"""
Quick test to verify the stocks compare page is working after fixing route conflict
"""
import sys
import os
import requests

def test_compare_route():
    """Test the compare route directly"""
    print("🔧 Testing Stocks Compare Page Fix")
    print("=" * 50)
    
    # Test URLs
    base_url = "https://aksjeradar.trade"
    test_urls = [
        f"{base_url}/stocks/compare",
        f"{base_url}/stocks/compare?symbols=EQNR.OL,DNB.OL",
        f"{base_url}/stocks/compare?tickers=AAPL,MSFT"
    ]
    
    results = []
    
    for url in test_urls:
        try:
            print(f"\n🌐 Testing: {url}")
            response = requests.get(url, timeout=15)
            status = response.status_code
            
            # Check if we get the actual compare page vs redirect/demo page
            content = response.text.lower()
            
            # Look for compare-specific content
            has_compare_form = 'sammenlign aksjer' in content or 'compare' in content
            has_demo_redirect = 'demo-modus aktivert' in content or 'prøv alle aksjeradar funksjoner' in content
            has_chart_js = 'chart.js' in content or 'chartjs' in content
            
            if status == 200:
                if has_demo_redirect:
                    result = "❌ REDIRECTED TO DEMO"
                elif has_compare_form:
                    if has_chart_js:
                        result = "✅ WORKING (with charts)"
                    else:
                        result = "⚠️ WORKING (no charts)"
                else:
                    result = "❓ UNKNOWN CONTENT"
            else:
                result = f"❌ ERROR {status}"
            
            print(f"   Status: {status}")
            print(f"   Result: {result}")
            
            results.append((url, status, result))
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append((url, 'ERROR', str(e)))
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    working_count = 0
    for url, status, result in results:
        if '✅' in result:
            working_count += 1
        print(f"{result}")
    
    if working_count == len(results):
        print("\n🎉 ALL TESTS PASSED - Compare page is working!")
        return True
    elif working_count > 0:
        print(f"\n⚠️ PARTIAL SUCCESS - {working_count}/{len(results)} tests passed")
        return False
    else:
        print("\n❌ ALL TESTS FAILED - Compare page still not working")
        return False

if __name__ == "__main__":
    success = test_compare_route()
    sys.exit(0 if success else 1)
