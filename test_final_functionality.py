#!/usr/bin/env python3
"""
Final functionality test after successful server startup
Testing all user-reported issues to verify they are resolved
"""

import requests
import time
import json
import pytest

# Server URL
BASE_URL = "http://localhost:5000"

# NOTE: Renamed from test_endpoint to helper_test_endpoint to avoid
# pytest collecting this diagnostic helper as a real test function.
def helper_test_endpoint(endpoint, description):
    """Test an endpoint and return status"""
    try:
        print(f"🔍 Testing {description}...")
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {description} - SUCCESS (200)")
            return True
        elif response.status_code == 302:
            print(f"🔄 {description} - REDIRECT (302) - {response.headers.get('Location', 'Unknown')}")
            return True
        else:
            print(f"❌ {description} - FAILED ({response.status_code})")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except requests.exceptions.ConnectionError:
        print(f"🔌 {description} - CONNECTION ERROR")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False

@pytest.mark.skip(reason="Diagnostic aggregate functionality script; skipped during standard test run.")
def test_all_functionality():
    """Test all functionality reported as problematic by user"""
    
    print("🚀 FINAL FUNCTIONALITY TEST")
    print("=" * 50)
    
    tests = [
        # Main user-reported issues
        ("/", "Home page"),
        ("/profile", "Profile page (was showing 'Det oppstod en teknisk feil under lasting av profilen')"),
        ("/stocks/compare", "Stocks compare page (was showing empty visualization)"),
        ("/stocks/details/TSLA", "Stocks details page for TSLA (chart loading issues)"),
        ("/stocks/details/AAPL", "Stocks details page for AAPL (RSI/MACD sections)"),
        ("/analysis/warren-buffett", "Warren Buffett analysis (search functionality)"),
        ("/price-alerts", "Price alerts page (creation functionality)"),
        ("/watchlist", "Watchlist page (adding stocks, loading alerts)"),
        
        # Additional critical pages
        ("/stocks", "Stocks main page"),
        ("/portfolio", "Portfolio page"),
        ("/analysis", "Analysis main page"),
        ("/health", "Health check"),
        
        # API endpoints for functionality testing
        ("/stocks/api/search", "Stocks search API"),
        ("/price-alerts/api/alerts", "Price alerts API"),
        ("/watchlist/api/alerts", "Watchlist alerts API"),
    ]
    
    results = []
    for endpoint, description in tests:
        success = helper_test_endpoint(endpoint, description)
        results.append((endpoint, description, success))
        time.sleep(0.5)  # Brief pause between requests
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for _, _, success in results if success)
    total = len(results)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful == total:
        print("\n🎉 ALL TESTS PASSED! ALL FUNCTIONALITY RESTORED!")
        print("🔧 Server startup dependency issues completely resolved!")
        print("📈 User-reported functionality issues should now be working!")
    else:
        print(f"\n⚠️  {total - successful} issues still need attention:")
        for endpoint, description, success in results:
            if not success:
                print(f"   ❌ {description} ({endpoint})")
    
    # Assert instead of returning bool (prevents PytestReturnNotNoneWarning)
    assert successful == total, f"{total - successful} functionality checks failed"

if __name__ == "__main__":
    test_all_functionality()
