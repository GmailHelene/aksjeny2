#!/usr/bin/env python3
"""Quick status check for key routes we fixed."""

import requests
import sys

def test_route(path, description):
    """Test a single route and return status."""
    try:
        response = requests.get(f"http://localhost:5001{path}", timeout=10)
        status = "✅ OK" if response.status_code == 200 else f"⚠️ {response.status_code}"
        if response.status_code == 302:
            location = response.headers.get('Location', 'unknown')
            status = f"↗️ 302 → {location}"
        print(f"{path:30} {status:20} {description}")
        return response.status_code in [200, 302]
    except Exception as e:
        print(f"{path:30} ❌ ERROR        {str(e)[:50]}")
        return False

def main():
    """Test key routes that should be working."""
    print("🧪 QUICK STATUS CHECK - Key Fixed Routes")
    print("=" * 70)
    
    tests = [
        ("/", "Homepage redirect"),
        ("/demo", "Demo page"),
        ("/stocks", "Stocks index"),
        ("/stocks/list/oslo", "Oslo stocks list"),
        ("/stocks/list/global", "Global stocks list"),
        ("/stocks/list/crypto", "Crypto list"),
        ("/stocks/details/DNB.OL", "Stock details"),
        ("/stocks/compare", "Stock comparison"),
        ("/register", "Registration page"),
        ("/pricing", "Pricing page"),
    ]
    
    passed = 0
    total = len(tests)
    
    for path, description in tests:
        if test_route(path, description):
            passed += 1
    
    print("=" * 70)
    print(f"📊 Results: {passed}/{total} working ({100*passed/total:.1f}% success rate)")
    
    if passed == total:
        print("🎉 All key routes are working!")
    elif passed > total * 0.7:
        print("🚀 Most routes working - good progress!")
    else:
        print("⚠️ Still issues with key routes")

if __name__ == "__main__":
    main()
