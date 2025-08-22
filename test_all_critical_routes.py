#!/usr/bin/env python3
"""
Comprehensive test of all critical routes mentioned in the user's issue list
Tests TradingView, sentiment analysis, watchlist, crypto dashboard, stock compare, etc.
"""

import requests
import json
import time
from datetime import datetime

def test_route(url, description, expected_status=200):
    """Test a single route and return results"""
    try:
        print(f"\n🔍 Testing: {description}")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=10)
        status = response.status_code
        
        if status == expected_status:
            print(f"   ✅ SUCCESS: {status}")
            return True
        else:
            print(f"   ❌ FAILED: {status}")
            if status == 500:
                print(f"   💥 500 ERROR - This is a critical issue!")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   💥 NETWORK ERROR: {e}")
        return False
    except Exception as e:
        print(f"   ❌ UNEXPECTED ERROR: {e}")
        return False

def main():
    print("🚀 TESTING ALL CRITICAL ROUTES")
    print("=" * 50)
    
    # Base URL - adjust this to your actual server
    base_url = "http://localhost:5000"  # Change if different
    
    # Critical routes to test
    test_routes = [
        # TradingView routes
        (f"{base_url}/analysis/tradingview", "TradingView Analysis Page"),
        (f"{base_url}/analysis/tradingview?symbol=EQNR.OL", "TradingView with Oslo symbol"),
        (f"{base_url}/analysis/tradingview?symbol=AAPL", "TradingView with US symbol"),
        
        # Sentiment analysis routes  
        (f"{base_url}/analysis/sentiment", "Sentiment Analysis Main Page"),
        (f"{base_url}/analysis/sentiment?symbol=EQNR.OL", "Sentiment Analysis with symbol"),
        (f"{base_url}/api/sentiment?symbol=AAPL", "Sentiment API endpoint"),
        
        # Technical analysis with TradingView widget
        (f"{base_url}/analysis/technical?symbol=EQNR.OL", "Technical Analysis with TradingView"),
        (f"{base_url}/analysis/technical?symbol=TSLA", "Technical Analysis US stock"),
        
        # Watchlist routes
        (f"{base_url}/portfolio/watchlist", "Portfolio Watchlist"),
        
        # Crypto dashboard routes
        (f"{base_url}/advanced-features/crypto-dashboard", "Crypto Dashboard"),
        (f"{base_url}/api/crypto-dashboard", "Crypto Dashboard API"),
        
        # Stock comparison routes
        (f"{base_url}/stocks/compare", "Stock Compare Tool"),
        (f"{base_url}/stocks/compare?stocks=EQNR.OL,DNB.OL", "Stock Compare with symbols"),
        
        # Other analysis routes mentioned
        (f"{base_url}/analysis/screener", "Stock Screener"),
        (f"{base_url}/analysis/fundamental?symbol=EQNR.OL", "Fundamental Analysis"),
        (f"{base_url}/analysis/warren_buffett?ticker=AAPL", "Warren Buffett Analysis"),
        
        # API routes that might have 500 errors
        (f"{base_url}/achievements/api/update_stat", "Achievement Tracking API", 405),  # POST only
        (f"{base_url}/api/user/watchlist", "User Watchlist API"),
    ]
    
    # Track results
    passed = 0
    failed = 0
    total = len(test_routes)
    
    for url, description, *expected in test_routes:
        expected_status = expected[0] if expected else 200
        
        if test_route(url, description, expected_status):
            passed += 1
        else:
            failed += 1
        
        time.sleep(0.5)  # Brief pause between requests
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 FINAL RESULTS:")
    print(f"   ✅ Passed: {passed}/{total}")
    print(f"   ❌ Failed: {failed}/{total}")
    print(f"   📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! All critical routes are working!")
    elif failed <= 3:
        print(f"\n⚠️  Minor issues found. {failed} routes need attention.")
    else:
        print(f"\n🚨 CRITICAL ISSUES: {failed} routes are failing!")
    
    print("\n🔧 TRADINGVIEW SPECIFIC CHECKS:")
    print("   - Ensure TradingView scripts load (check browser console)")
    print("   - Verify symbol mapping (EQNR.OL → OSL:EQNR)")  
    print("   - Check for ad blocker interference")
    print("   - Confirm fallback Chart.js works if TradingView is blocked")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
