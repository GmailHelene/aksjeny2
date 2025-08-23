#!/usr/bin/env python3
"""
KRITISK PRODUKSJONS-TEST
Tester alle hovedsider for 500/404/redirect errors
"""

import requests
import time
from datetime import datetime

BASE_URL = "https://aksjeradar.trade"

# Kritiske sider som MUST fungere
CRITICAL_PAGES = [
    "/",                                    # Homepage
    "/stocks/oslo",                        # Oslo Børs
    "/stocks/details/YAR.OL",             # Stock details (test BuildError fix)
    "/analysis",                          # Analysis index  
    "/analysis/sentiment",                # Sentiment analysis
    "/analysis/technical",                # Technical analysis
    "/demo",                              # Demo page
    "/pricing",                          # Pricing page
    "/login",                            # Login page
]

# Test parameters for analysis pages
ANALYSIS_PAGES_WITH_TICKER = [
    "/analysis/technical?ticker=YAR.OL",
    "/analysis/ai?ticker=EQUI.OL", 
    "/analysis/recommendation?ticker=NHY.OL",
]

def test_page(url, timeout=10):
    """Test en enkelt side"""
    try:
        print(f"Testing: {url}")
        response = requests.get(url, timeout=timeout, allow_redirects=False)
        
        # Sjekk for redirect loops (vi vil ikke ha redirects på disse sidene)
        if response.status_code in [301, 302, 307, 308]:
            location = response.headers.get('Location', 'unknown')
            print(f"⚠️  REDIRECT: {response.status_code} -> {location}")
            return f"REDIRECT({response.status_code})"
        
        # Sjekk for errors
        if response.status_code >= 500:
            print(f"❌ SERVER ERROR: {response.status_code}")
            return f"ERROR({response.status_code})"
        elif response.status_code == 404:
            print(f"❌ NOT FOUND: 404")
            return "NOT_FOUND"
        elif response.status_code == 200:
            # Sjekk for BuildError i response content
            content = response.text.lower()
            if 'builderror' in content or 'could not build url' in content:
                print(f"❌ BUILD ERROR found in page content")
                return "BUILD_ERROR"
            elif 'internal server error' in content:
                print(f"❌ Internal server error in content")
                return "INTERNAL_ERROR"
            else:
                print(f"✅ OK: {response.status_code}")
                return "OK"
        else:
            print(f"⚠️  UNEXPECTED: {response.status_code}")
            return f"UNEXPECTED({response.status_code})"
            
    except requests.exceptions.RequestException as e:
        print(f"❌ CONNECTION ERROR: {e}")
        return "CONNECTION_ERROR"

def main():
    print(f"\n{'='*60}")
    print(f"KRITISK PRODUKSJONS-TEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print(f"{'='*60}\n")
    
    results = {}
    errors = []
    
    # Test critical pages
    print("🔍 Testing critical pages...")
    for page in CRITICAL_PAGES:
        url = BASE_URL + page
        result = test_page(url)
        results[page] = result
        if result not in ["OK"]:
            errors.append(f"{page}: {result}")
        time.sleep(0.5)  # Avoid rate limiting
    
    print("\n🔍 Testing analysis pages with ticker...")
    for page in ANALYSIS_PAGES_WITH_TICKER:
        url = BASE_URL + page
        result = test_page(url)
        results[page] = result
        if result not in ["OK"]:
            errors.append(f"{page}: {result}")
        time.sleep(0.5)
    
    # Results summary
    print(f"\n{'='*60}")
    print("RESULTATER:")
    print(f"{'='*60}")
    
    ok_count = sum(1 for r in results.values() if r == "OK")
    total_count = len(results)
    
    print(f"✅ OK: {ok_count}/{total_count}")
    
    if errors:
        print(f"❌ ERRORS: {len(errors)}")
        for error in errors:
            print(f"   - {error}")
    else:
        print("🎉 ALLE SIDER FUNGERER!")
    
    print(f"\n{'='*60}")
    if len(errors) == 0:
        print("✅ PRODUKSJONEN ER FRISK! Ingen kritiske feil funnet.")
    else:
        print("⚠️  PRODUKSJONEN HAR PROBLEMER - Se errors ovenfor")
    print(f"{'='*60}\n")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
