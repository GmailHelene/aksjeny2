#!/usr/bin/env python3
"""
Systematic check for remaining issues from SISTE-GJENVÆRENDE-ARBEID-PR-0108.md
"""

import requests
import os
from datetime import datetime

def test_issue(description, url, expected_status_codes=[200], auth_required=False):
    """Test a specific issue"""
    print(f"\n🔍 Testing: {description}")
    print(f"📍 URL: {url}")
    
    try:
        # Set headers for authentication if needed
        headers = {}
        if auth_required:
            headers['User-Agent'] = 'Mozilla/5.0 (compatible; TestBot/1.0)'
        
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
        
        status_ok = response.status_code in expected_status_codes
        status_icon = "✅" if status_ok else "❌"
        
        print(f"   Status: {response.status_code} {status_icon}")
        
        # Check for specific error messages
        if "500" in str(response.status_code):
            print(f"   ❌ 500 Error detected")
        elif "404" in str(response.status_code):
            print(f"   ❌ 404 Not Found")
        elif response.status_code == 302:
            print(f"   🔄 Redirect to: {response.headers.get('Location', 'Unknown')}")
        
        return status_ok, response.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection Error: {e}")
        return False, None

def main():
    """Check all remaining issues"""
    print("🔍 SYSTEMATIC CHECK OF REMAINING ISSUES")
    print("=" * 50)
    
    base_url = "https://aksjeradar.trade"
    
    issues = [
        {
            "desc": "Homepage for not logged in user (should NOT show 500 error)",
            "url": f"{base_url}/",
            "expected": [200, 302]  # Allow redirect to demo
        },
        {
            "desc": "Notifications settings (should NOT show 404)",
            "url": f"{base_url}/notifications/settings", 
            "expected": [200, 302]  # Allow redirect for auth
        },
        {
            "desc": "Technical analysis with TSLA symbol",
            "url": f"{base_url}/analysis/technical?symbol=TSLA",
            "expected": [200]
        },
        {
            "desc": "Sentiment analysis with DNB.OL symbol", 
            "url": f"{base_url}/analysis/sentiment?symbol=DNB.OL",
            "expected": [200]
        },
        {
            "desc": "Stock details for AAPL",
            "url": f"{base_url}/stocks/details/AAPL",
            "expected": [200]
        },
        {
            "desc": "Demo page (fallback for unauthenticated users)",
            "url": f"{base_url}/demo",
            "expected": [200]
        },
        {
            "desc": "Stocks list - crypto (button consistency check)",
            "url": f"{base_url}/stocks/list/crypto",
            "expected": [200]
        },
        {
            "desc": "Stocks list - global (button consistency check)",
            "url": f"{base_url}/stocks/list/global",
            "expected": [200]
        },
        {
            "desc": "Stocks list - currency (button consistency check)",
            "url": f"{base_url}/stocks/list/currency",
            "expected": [200]
        },
        {
            "desc": "Stocks list - Oslo (reference for button types)",
            "url": f"{base_url}/stocks/list/oslo",
            "expected": [200]
        }
    ]
    
    results = []
    for issue in issues:
        success, status = test_issue(
            issue["desc"], 
            issue["url"], 
            issue["expected"]
        )
        results.append((issue["desc"], success, status))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY OF ISSUES")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed < total:
        print(f"❌ Failed tests:")
        for desc, success, status in results:
            if not success:
                print(f"   - {desc} (Status: {status})")
    else:
        print("🎉 All critical endpoints are working!")
    
    # Specific known issues (production-only)
    print("\n🔧 KNOWN PRODUCTION ISSUES (require environment config):")
    print("   1. Payment system: Missing Stripe API keys")
    print("   2. TradingView charts: May need real API keys")
    print("   3. Yahoo Finance: Rate limiting (429 errors)")

if __name__ == "__main__":
    main()
