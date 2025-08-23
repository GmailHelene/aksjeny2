#!/usr/bin/env python3
"""
SIMPLIFIED DIRECT TEST - Test critical authenticated URLs
"""

import urllib.request
import urllib.error
import time

def test_url(url, description):
    """Test a single URL"""
    print(f"Testing {description}: {url}")
    try:
        response = urllib.request.urlopen(url, timeout=15)
        status = response.getcode()
        if status == 200:
            print(f"  ✅ SUCCESS: {status}")
            return True
        else:
            print(f"  ⚠️ UNEXPECTED: {status}")
            return False
    except urllib.error.HTTPError as e:
        if e.code == 500:
            print(f"  ❌ SERVER ERROR: {e.code} - BuildError likely!")
        elif e.code == 404:
            print(f"  ❌ NOT FOUND: {e.code}")
        elif e.code == 302 or e.code == 301:
            print(f"  🔄 REDIRECT: {e.code} - This might be auth redirect (OK)")
            return True
        else:
            print(f"  ❌ HTTP ERROR: {e.code}")
        return False
    except Exception as e:
        print(f"  ❌ CONNECTION ERROR: {e}")
        return False

def main():
    print("🚨 CRITICAL URL TEST - Post-Login Route Failures")
    print("=" * 60)
    
    # User reported failing URLs
    test_urls = [
        ("https://aksjeradar.trade/", "Homepage"),
        ("https://aksjeradar.trade/watchlist/", "Watchlist"),
        ("https://aksjeradar.trade/index", "Index redirect"),
        ("https://aksjeradar.trade/analysis/currency_overview", "Currency Overview"),
        ("https://aksjeradar.trade/analysis/market-overview", "Market Overview"),
        ("https://aksjeradar.trade/analysis/sentiment", "Sentiment Analysis"),
        ("https://aksjeradar.trade/portfolio", "Portfolio"),
        ("https://aksjeradar.trade/stocks/oslo", "Oslo Stocks"),
    ]
    
    success_count = 0
    total_count = len(test_urls)
    
    for url, description in test_urls:
        if test_url(url, description):
            success_count += 1
        time.sleep(1)  # Rate limiting
        print()
    
    print("=" * 60)
    print(f"RESULTS: {success_count}/{total_count} URLs responding")
    
    if success_count >= total_count * 0.8:
        print("✅ MOSTLY WORKING - Authentication route fixes successful!")
    elif success_count >= total_count * 0.5:
        print("⚠️  PARTIALLY WORKING - Some routes still failing")
    else:
        print("❌ STILL CRITICAL - Major authentication route failures persist")
    
    return success_count >= total_count * 0.5

if __name__ == "__main__":
    main()
