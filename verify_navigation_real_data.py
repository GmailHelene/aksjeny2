#!/usr/bin/env python3
"""
Navigation Pages Real Data Verification Script
Checks that all navigation pages show real data for logged-in users
"""

import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:5002"

# Key navigation pages that should show real data for authenticated users
NAVIGATION_PAGES = [
    # Analysis Pages
    ("/analysis/", "Analysis Dashboard"),
    ("/analysis/market-overview", "Market Overview"), 
    ("/analysis/warren-buffett", "Warren Buffett Analysis"),
    ("/analysis/technical", "Technical Analysis"),
    ("/analysis/fundamental", "Fundamental Analysis"),
    ("/analysis/sentiment", "Sentiment Analysis"),
    
    # Market Intelligence
    ("/market-intel/", "Market Intelligence Dashboard"),
    ("/market-intel/sector-analysis", "Sector Analysis (Enhanced)"),
    ("/market-intel/insider-trading", "Insider Trading"),
    ("/market-intel/earnings-calendar", "Earnings Calendar"),
    
    # Financial Dashboard
    ("/financial-dashboard", "Financial Dashboard"),
    
    # Advanced Features
    ("/advanced-analytics/", "Advanced Analytics"),
    ("/advanced/", "Advanced Features"),
    
    # Portfolio & Watchlist
    ("/portfolio/", "Portfolio Management"),
    ("/portfolio/watchlist/", "Watchlist Management"),
    
    # Stocks & Data
    ("/stocks/", "Stock Overview"),
    ("/stocks/list/oslo", "Oslo Stocks List"),
    ("/stocks/list/global", "Global Stocks List"),
    
    # External Data
    ("/external-data/analyst-coverage", "Analyst Coverage"),
    
    # Price Alerts
    ("/price-alerts/", "Price Alerts Dashboard"),
    
    # News & Intelligence
    ("/news-intelligence/", "News Intelligence"),
    ("/norwegian-intel/", "Norwegian Intelligence"),
    
    # Real-time Data
    ("/realtime/", "Real-time Dashboard"),
    
    # Mobile Trading
    ("/mobile-trading/", "Mobile Trading Interface"),
]

def check_page_for_real_data(url, page_name):
    """Check if a page provides real data indicators"""
    try:
        logger.info(f"🔍 Checking: {page_name} ({url})")
        
        response = requests.get(f"{BASE_URL}{url}", timeout=10)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # Indicators of real data
            real_data_indicators = [
                'real data', 'ekte data', 'live data', 'sanntidsdata',
                'yahoo finance', 'financial modeling prep', 'alpha vantage',
                'dataservice', 'real market', 'live market',
                'authenticated user', 'premium access'
            ]
            
            # Indicators of demo/fallback data
            demo_indicators = [
                'demo data', 'fallback data', 'mock data', 'test data',
                'sample data', 'placeholder', 'dummy data'
            ]
            
            real_count = sum(1 for indicator in real_data_indicators if indicator in content)
            demo_count = sum(1 for indicator in demo_indicators if indicator in content)
            
            # Check for specific data patterns
            has_prices = 'nok' in content or '$' in content or '€' in content
            has_percentages = '%' in content
            has_charts = 'chart' in content or 'graph' in content
            has_tables = '<table' in content
            
            status = "✅ REAL DATA" if real_count > demo_count else "⚠️ NEEDS REVIEW" if demo_count > 0 else "📊 FUNCTIONAL"
            
            logger.info(f"   {status} - Prices: {has_prices}, Charts: {has_charts}, Tables: {has_tables}")
            
            return {
                'url': url,
                'name': page_name,
                'status_code': response.status_code,
                'real_indicators': real_count,
                'demo_indicators': demo_count,
                'has_prices': has_prices,
                'has_charts': has_charts,
                'has_tables': has_tables,
                'assessment': status
            }
            
        else:
            logger.warning(f"   ❌ ERROR - Status: {response.status_code}")
            return {
                'url': url,
                'name': page_name,
                'status_code': response.status_code,
                'error': f"HTTP {response.status_code}",
                'assessment': "❌ ERROR"
            }
            
    except requests.exceptions.Timeout:
        logger.error(f"   ⏱️ TIMEOUT - {page_name}")
        return {'url': url, 'name': page_name, 'error': 'Timeout', 'assessment': "⏱️ TIMEOUT"}
    except Exception as e:
        logger.error(f"   💥 EXCEPTION - {page_name}: {e}")
        return {'url': url, 'name': page_name, 'error': str(e), 'assessment': "💥 EXCEPTION"}

def main():
    """Run the navigation pages verification"""
    logger.info("🚀 Starting Navigation Pages Real Data Verification")
    logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🌐 Base URL: {BASE_URL}")
    logger.info(f"📄 Checking {len(NAVIGATION_PAGES)} pages")
    print("=" * 80)
    
    results = []
    
    for url, page_name in NAVIGATION_PAGES:
        result = check_page_for_real_data(url, page_name)
        results.append(result)
    
    print("\n" + "=" * 80)
    logger.info("📊 VERIFICATION SUMMARY")
    print("=" * 80)
    
    # Count assessments
    status_counts = {}
    for result in results:
        assessment = result.get('assessment', 'UNKNOWN')
        status_counts[assessment] = status_counts.get(assessment, 0) + 1
    
    # Print summary
    for status, count in status_counts.items():
        logger.info(f"   {status}: {count} pages")
    
    # Print detailed results
    print("\n📋 DETAILED RESULTS:")
    print("-" * 80)
    
    for result in results:
        print(f"{result.get('assessment', '❓')} {result['name']}")
        if 'error' in result:
            print(f"     Error: {result['error']}")
        else:
            print(f"     URL: {result['url']}")
            if 'real_indicators' in result:
                print(f"     Real Data Indicators: {result['real_indicators']}")
                print(f"     Demo Data Indicators: {result['demo_indicators']}")
                print(f"     Features: Prices={result['has_prices']}, Charts={result['has_charts']}, Tables={result['has_tables']}")
        print()
    
    # Recommendations
    print("🎯 RECOMMENDATIONS:")
    print("-" * 40)
    
    needs_review = [r for r in results if 'NEEDS REVIEW' in r.get('assessment', '')]
    errors = [r for r in results if 'ERROR' in r.get('assessment', '') or 'TIMEOUT' in r.get('assessment', '') or 'EXCEPTION' in r.get('assessment', '')]
    
    if needs_review:
        print("⚠️ Pages that may need real data improvements:")
        for result in needs_review:
            print(f"   - {result['name']} ({result['url']})")
    
    if errors:
        print("\n❌ Pages with errors that need fixing:")
        for result in errors:
            print(f"   - {result['name']} ({result['url']}) - {result.get('error', 'Unknown error')}")
    
    if not needs_review and not errors:
        print("✅ All pages are functional and providing appropriate data!")
    
    print(f"\n🏁 Verification completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
