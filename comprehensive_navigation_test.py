#!/usr/bin/env python3
"""
Comprehensive navigation test to check all links for 500 errors
Tests all navigation dropdowns and main links
"""

import requests
from urllib.parse import urljoin
import time
import json
from datetime import datetime

# Base URL for testing (adjust as needed)
BASE_URL = "http://localhost:5000"

# Test navigation links from the updated structure
NAVIGATION_LINKS = {
    "Main": [
        "/",
        "/demo",
        "/pricing"
    ],
    "Aksjer": [
        "/stocks",  # New primary "Oversikt" link
        "/analysis/market-overview",
        "/analysis/oslo-overview", 
        "/analysis/global-overview",
        "/analysis/currency-overview",
        "/stocks/list/oslo",
        "/stocks/list/global",
        "/stocks/list/crypto",
        "/advanced-features/crypto-dashboard",
        "/stocks/list/currency",
        "/stocks/prices",
        "/stocks/search",
        "/stocks/compare"
    ],
    "Analyse": [
        "/analysis",
        "/analysis/ai",
        "/analysis/technical",
        "/analysis/fundamental", 
        "/analysis/sentiment",
        "/analysis/warren-buffett",
        "/analysis/benjamin-graham",
        "/analysis/screener",
        "/analysis/strategy-builder",
        "/analysis/tradingview",
        "/analysis/recommendation"
    ],
    "Market Intel": [
        "/market-intel",
        "/market-intel/insider-trading",
        "/market-intel/earnings-calendar",
        "/market-intel/sector-analysis",
        "/market-intel/economic-indicators",
        "/news",
        "/news-intelligence/dashboard",
        "/features/market-news-sentiment",
        "/daily-view",
        "/sentiment-tracker",
        "/norwegian-intel",
        "/norwegian-intel/social-sentiment",
        "/norwegian-intel/oil-correlation",
        "/norwegian-intel/government-impact",
        "/norwegian-intel/shipping-intelligence",
        "/external-data/market-intelligence",
        "/external-data/analyst-coverage"
    ],
    "Pro Tools": [
        "/pro-tools",
        "/pro-tools/price-alerts",
        "/features/analyst-recommendations",
        "/advanced-features/currency-converter",
        "/investment-analyzer",
        "/mobile-trading/dashboard"
    ],
    "Portfolio": [
        "/portfolio",
        "/portfolio/create",
        "/portfolio/watchlist",
        "/watchlist-advanced",
        "/portfolio/stock-tips",
        "/portfolio/advanced",
        "/advanced-analytics"
    ],
    "Resources": [  # New Resources dropdown with Forum
        "/resources",
        "/forum",  # Critical forum link 
        "/resources/learning-center",
        "/resources/guides",
        "/resources/tutorials",
        "/resources/documentation",
        "/resources/api"
    ],
    "Footer": [
        "/investment-guides",
        "/resources",
        "/about",
        "/help",
        "/pricing"
    ]
}

def test_url(url, session=None):
    """Test a single URL and return status info"""
    full_url = urljoin(BASE_URL, url)
    
    try:
        if session:
            response = session.get(full_url, timeout=10)
        else:
            response = requests.get(full_url, timeout=10)
        
        return {
            "url": url,
            "full_url": full_url,
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "error": response.status_code >= 500,
            "response_time": response.elapsed.total_seconds()
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "full_url": full_url,
            "status_code": None,
            "success": False,
            "error": True,
            "exception": str(e),
            "response_time": None
        }

def run_comprehensive_test():
    """Run comprehensive test of all navigation links"""
    
    print("🚀 Starting Comprehensive Navigation Test")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {}
    total_tests = 0
    total_errors = 0
    total_500_errors = 0
    
    # Create session for connection reuse
    session = requests.Session()
    
    for section, urls in NAVIGATION_LINKS.items():
        print(f"📋 Testing {section} Section ({len(urls)} links)")
        print("-" * 40)
        
        section_results = []
        section_errors = 0
        section_500s = 0
        
        for url in urls:
            result = test_url(url, session)
            section_results.append(result)
            total_tests += 1
            
            if result["error"]:
                total_errors += 1
                section_errors += 1
                if result["status_code"] == 500:
                    total_500_errors += 1
                    section_500s += 1
                    print(f"   ❌ {url} - 500 SERVER ERROR")
                elif result["status_code"] is None:
                    print(f"   ❌ {url} - CONNECTION ERROR: {result.get('exception', 'Unknown')}")
                else:
                    print(f"   ⚠️  {url} - HTTP {result['status_code']}")
            elif not result["success"]:
                print(f"   ⚠️  {url} - HTTP {result['status_code']}")
            else:
                print(f"   ✅ {url} - OK ({result['response_time']:.2f}s)")
            
            time.sleep(0.1)  # Small delay to avoid overwhelming server
        
        results[section] = section_results
        
        if section_errors > 0:
            print(f"   💥 {section} has {section_errors} errors ({section_500s} are 500 errors)")
        else:
            print(f"   🎉 {section} - All links working!")
        
        print()
    
    session.close()
    
    # Summary report
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    print(f"Total links tested: {total_tests}")
    print(f"Total errors: {total_errors}")
    print(f"500 Server errors: {total_500_errors}")
    print(f"Success rate: {((total_tests - total_errors) / total_tests * 100):.1f}%")
    print()
    
    # Critical Issues Report
    if total_500_errors > 0:
        print("🚨 CRITICAL 500 ERRORS FOUND:")
        print("-" * 30)
        for section, section_results in results.items():
            for result in section_results:
                if result["status_code"] == 500:
                    print(f"   💥 {result['url']} (in {section})")
        print()
    
    # Forum-specific check
    forum_result = None
    for section, section_results in results.items():
        for result in section_results:
            if result["url"] == "/forum":
                forum_result = result
                break
    
    if forum_result:
        if forum_result["success"]:
            print("✅ FORUM STATUS: Forum is accessible and working")
        else:
            print(f"❌ FORUM STATUS: Forum has issues - HTTP {forum_result['status_code']}")
            if forum_result["status_code"] == 500:
                print("   This is a critical 500 server error!")
    else:
        print("⚠️  FORUM STATUS: Forum link not tested")
    
    print()
    
    # Save detailed results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f'navigation_test_results_{timestamp}.json'
    
    test_summary = {
        "timestamp": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "total_tests": total_tests,
        "total_errors": total_errors,
        "total_500_errors": total_500_errors,
        "success_rate": (total_tests - total_errors) / total_tests * 100,
        "results": results
    }
    
    with open(results_file, 'w') as f:
        json.dump(test_summary, f, indent=2)
    
    print(f"📁 Detailed results saved to: {results_file}")
    
    # Return results for programmatic use
    return {
        "success": total_500_errors == 0,
        "total_tests": total_tests,
        "total_errors": total_errors,
        "total_500_errors": total_500_errors,
        "forum_working": forum_result["success"] if forum_result else None
    }

if __name__ == "__main__":
    # Run the test
    results = run_comprehensive_test()
    
    # Exit with appropriate code
    if results["total_500_errors"] > 0:
        print("\n❌ Test completed with 500 errors - immediate attention required!")
        exit(1)
    elif results["total_errors"] > 0:
        print(f"\n⚠️  Test completed with {results['total_errors']} non-critical errors")
        exit(2)
    else:
        print("\n🎉 All tests passed successfully!")
        exit(0)
