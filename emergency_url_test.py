#!/usr/bin/env python3
"""
EMERGENCY TEST - User reported URLs failing after login
"""
import urllib.request
import urllib.error

FAILING_URLS = [
    "https://aksjeradar.trade/watchlist/",
    "https://aksjeradar.trade/index", 
    "https://aksjeradar.trade/analysis/currency_overview",
    "https://aksjeradar.trade/analysis/market-overview"
]

print("🚨 EMERGENCY URL TEST - Testing user reported failures")
print("=" * 60)

for url in FAILING_URLS:
    print(f"\nTesting: {url}")
    try:
        response = urllib.request.urlopen(url, timeout=10)
        status = response.getcode()
        print(f"✅ Status: {status}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code}")
        if e.code == 500:
            print("   🚨 SERVER ERROR - BuildError likely!")
        elif e.code == 404:
            print("   🚨 NOT FOUND")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("Testing complete - investigating authenticated route failures...")
