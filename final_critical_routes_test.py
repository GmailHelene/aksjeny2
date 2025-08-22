#!/usr/bin/env python3
"""
Comprehensive Test of All Critical Routes - Final Validation
"""

import requests
import json
import time
from urllib.parse import urljoin
import sys

# Configuration
BASE_URL = "http://localhost:5002"  # Main.py uses port 5002
TIMEOUT = 10

def test_route(route, method='GET', data=None, expected_status=200, description=""):
    """Test a single route"""
    url = urljoin(BASE_URL, route)
    print(f"\n🔍 Testing: {method} {route}")
    if description:
        print(f"   Description: {description}")
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=TIMEOUT)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=TIMEOUT)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
            
        print(f"   Status: {response.status_code}")
        
        # Check for specific error patterns
        if response.status_code == 500:
            print(f"❌ 500 Error detected!")
            try:
                error_text = response.text[:500] if response.text else "No error text"
                print(f"   Error content: {error_text}")
            except:
                print("   Could not read error content")
            return False
        elif response.status_code == 404:
            print(f"⚠️  404 Not Found")
            return False
        elif response.status_code in [200, 302]:
            print(f"✅ Success ({response.status_code})")
            return True
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectError:
        print(f"❌ Connection Error - Is the server running?")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("🚀 COMPREHENSIVE CRITICAL ROUTES TEST")
    print("=" * 50)
    
    # Test critical routes from the original list
    critical_routes = [
        # Search functionality
        ("/search", "GET", None, "Search page access"),
        
        # TradingView and chart components
        ("/analysis/tradingview", "GET", None, "TradingView charts"),
        ("/analysis/technical", "GET", None, "Technical analysis with TradingView"),
        
        # Stock analysis
        ("/analysis/compare", "GET", None, "Stock comparison tool"),
        ("/analysis/recommendations", "GET", None, "Stock recommendations"),
        ("/analysis/screener", "GET", None, "Stock screener"),
        
        # News and sentiment
        ("/news-intelligence", "GET", None, "News intelligence dashboard"),
        ("/news-intelligence/sentiment", "GET", None, "Sentiment analysis"),
        
        # Portfolio management
        ("/portfolio", "GET", None, "Portfolio dashboard"),
        ("/portfolio/performance", "GET", None, "Portfolio performance"),
        
        # Watchlist functionality
        ("/portfolio/watchlist", "GET", None, "Watchlist management"),
        
        # Advanced features
        ("/advanced/crypto-dashboard", "GET", None, "Crypto dashboard"),
        ("/advanced/options-analyzer", "GET", None, "Options analyzer"),
        
        # API endpoints (these might require authentication)
        ("/achievements/api/user_stats", "GET", None, "Achievement tracking API"),
        ("/api/notifications", "GET", None, "Notifications API"),
        
        # Analysis pages
        ("/analysis", "GET", None, "Main analysis page"),
        ("/analysis/risk", "GET", None, "Risk analysis"),
        ("/analysis/sectors", "GET", None, "Sector analysis"),
        
        # User features
        ("/features/notifications", "GET", None, "Notification settings"),
        ("/features/profile", "GET", None, "User profile"),
    ]
    
    print(f"Testing {len(critical_routes)} critical routes...\n")
    
    success_count = 0
    failure_count = 0
    
    for route, method, data, description in critical_routes:
        if test_route(route, method, data, description=description):
            success_count += 1
        else:
            failure_count += 1
        time.sleep(0.5)  # Rate limiting
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    print(f"✅ Successful routes: {success_count}")
    print(f"❌ Failed routes: {failure_count}")
    print(f"📈 Success rate: {(success_count/(success_count+failure_count))*100:.1f}%")
    
    if failure_count == 0:
        print("\n🎉 ALL CRITICAL ROUTES ARE WORKING!")
        print("   The application appears to be fully functional.")
    else:
        print(f"\n⚠️  {failure_count} routes still need attention.")
        print("   Review the failed routes above for remaining issues.")
    
    return failure_count == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
