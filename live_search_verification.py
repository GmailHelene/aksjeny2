#!/usr/bin/env python3
"""
Live site verification for search and compare functionality
"""
import requests
import time

def test_live_search():
    """Test if search page works on live site"""
    print("🔍 Testing live search functionality...")
    
    test_urls = [
        "https://aksjeradar.trade/stocks/search?q=tesla",
        "https://aksjeradar.trade/stocks/search?q=TSLA", 
        "https://aksjeradar.trade/stocks/search?q=apple",
        "https://aksjeradar.trade/stocks/compare"
    ]
    
    for url in test_urls:
        try:
            print(f"\nTesting: {url}")
            response = requests.get(url, timeout=10)
            
            # Check if we get demo content or actual page
            content = response.text.lower()
            
            if "demo-modus aktivert" in content:
                print(f"❌ Still redirecting to demo content")
            elif "ingen resultater funnet" in content:
                print(f"⚠️  Search page accessible but no results (this could be expected)")
            elif "søk aksjer" in content or "search" in content:
                print(f"✅ Search page appears to be working")
            elif "sammenlign aksjer" in content or "compare" in content:
                print(f"✅ Compare page appears to be working")
            else:
                print(f"❓ Unclear page content")
                
            print(f"   Status: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Error accessing {url}: {e}")

def test_live_search_json():
    """Test if search API returns JSON results"""
    print("\n🔍 Testing live search API...")
    
    api_urls = [
        "https://aksjeradar.trade/stocks/api/search?q=tesla",
        "https://aksjeradar.trade/stocks/api/search?q=TSLA"
    ]
    
    for url in api_urls:
        try:
            print(f"\nTesting API: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"✅ API returned {len(data)} results")
                        print(f"   First result: {data[0].get('symbol', 'N/A')} - {data[0].get('name', 'N/A')}")
                    elif isinstance(data, list) and len(data) == 0:
                        print(f"⚠️  API returned empty results list")
                    else:
                        print(f"❓ API returned unexpected data: {type(data)}")
                except:
                    print(f"❌ API did not return valid JSON")
            else:
                print(f"❌ API returned status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error accessing API {url}: {e}")

if __name__ == "__main__":
    print("🚀 LIVE SITE VERIFICATION TEST")
    print("=" * 50)
    
    test_live_search()
    test_live_search_json()
    
    print("\n" + "=" * 50)
    print("🎯 Live verification completed!")
