#!/usr/bin/env python3
"""
Quick endpoint testing for Aksjeradar
Tests the most critical endpoints for errors
"""
import requests
import json
import sys

def test_endpoint(url, endpoint_name):
    """Test a single endpoint"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {endpoint_name:30} - OK ({len(response.content):,} bytes)")
            return True
        elif response.status_code == 302:
            redirect_to = response.headers.get('Location', 'unknown')
            print(f"⚠️  {endpoint_name:30} - Redirects to: {redirect_to}")
            return True
        elif response.status_code == 503:
            print(f"🔧 {endpoint_name:30} - Service Unavailable (503)")
            return False
        else:
            print(f"❌ {endpoint_name:30} - Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint_name:30} - Connection refused")
        return False
    except Exception as e:
        print(f"❌ {endpoint_name:30} - Error: {str(e)}")
        return False

def main():
    """Test critical endpoints"""
    print("🎯 QUICK ENDPOINT TESTING")
    print("=" * 60)
    
    # Try both possible ports
    base_urls = ["http://localhost:5001", "http://localhost:5000"]
    base_url = None
    
    for url in base_urls:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code in [200, 503]:  # Accept 503 as server running
                base_url = url
                print(f"✅ Server found at {base_url}")
                break
        except:
            continue
    
    if not base_url:
        print("❌ Server not running on port 5000 or 5001")
        return
    
    # Critical endpoints to test
    endpoints = [
        ("/health", "Health Check"),
        ("/health/ready", "Health Ready"),
        ("/demo", "Demo Page"),
        ("/", "Homepage"),
        ("/api/health", "API Health"),
        ("/stocks", "Stocks"),
        ("/analysis", "Analysis"),
        ("/portfolio", "Portfolio"),
        ("/pricing", "Pricing"),
        ("/features/ai-predictions", "AI Predictions"),
        ("/financial-dashboard", "Financial Dashboard"),
        ("/mobile-trading", "Mobile Trading"),
        ("/news", "News"),
        ("/notifications", "Notifications"),
        ("/investment-guides", "Investment Guides"),
        ("/analysis/technical", "Technical Analysis"),
        ("/analysis/currency-overview", "Currency Overview"),
        ("/stocks/list/oslo", "Oslo Stocks"),
        ("/stocks/list/global", "Global Stocks"),
        ("/stocks/list/crypto", "Crypto"),
    ]
    
    passed = 0
    total = len(endpoints)
    
    print(f"\nTesting {total} critical endpoints:\n")
    
    for endpoint, name in endpoints:
        url = base_url + endpoint
        if test_endpoint(url, name):
            passed += 1
    
    print(f"\n📊 RESULTS: {passed}/{total} endpoints working ({passed/total*100:.1f}%)")
    
    if passed < total:
        print("\n⚠️  Some endpoints are not working. Check server logs for details.")
    else:
        print("\n🎉 All critical endpoints are working!")

if __name__ == "__main__":
    main()
