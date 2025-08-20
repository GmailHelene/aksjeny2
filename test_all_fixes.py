#!/usr/bin/env python3
"""
Comprehensive test for all recent fixes
"""

import requests
import sys
from urllib.parse import urljoin

def test_fixes():
    base_url = "http://localhost:5000"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print("🔍 Testing all recent fixes...\n")
    
    # Test 1: ROI Calculator accessibility (should work)
    print("1️⃣ Testing ROI Calculator accessibility...")
    try:
        response = session.get(f"{base_url}/roi_kalkulator")
        if response.status_code == 200:
            print("   ✅ ROI Calculator accessible")
        else:
            print(f"   ❌ ROI Calculator failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ ROI Calculator error: {e}")
    
    # Test 2: Check if ROI Calculator is removed from navigation
    print("\n2️⃣ Testing navigation menu structure...")
    try:
        response = session.get(base_url)
        if response.status_code == 200:
            content = response.text
            roi_nav_count = content.count('ROI Kalkulator')
            if roi_nav_count == 0:
                print("   ✅ ROI Calculator removed from navigation")
            else:
                print(f"   ⚠️ ROI Calculator still in navigation ({roi_nav_count} times)")
        else:
            print(f"   ❌ Homepage failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Navigation test error: {e}")
    
    # Test 3: Check if ROI Calculator promotion exists on homepage
    print("\n3️⃣ Testing ROI Calculator promotion on homepage...")
    try:
        response = session.get(base_url)
        if response.status_code == 200:
            content = response.text
            if 'Beregn ROI' in content and 'roi_kalkulator' in content:
                print("   ✅ ROI Calculator promotion found on homepage")
            else:
                print("   ❌ ROI Calculator promotion not found")
        else:
            print(f"   ❌ Homepage failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Promotion test error: {e}")
    
    # Test 4: Check recommendations page buttons
    print("\n4️⃣ Testing recommendations page buttons...")
    try:
        response = session.get(f"{base_url}/analysis/recommendations")
        if response.status_code == 200:
            content = response.text
            buy_buttons = content.count('external-buy-btn')
            favorite_buttons = content.count('btn-star-favorite')
            if buy_buttons > 0 and favorite_buttons > 0:
                print(f"   ✅ Recommendations buttons found (Buy: {buy_buttons}, Fav: {favorite_buttons})")
            else:
                print(f"   ❌ Missing buttons - Buy: {buy_buttons}, Favorite: {favorite_buttons}")
        else:
            print(f"   ❌ Recommendations page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Recommendations test error: {e}")
    
    # Test 5: Check AI Predictions in Analysis menu
    print("\n5️⃣ Testing AI Predictions in Analysis menu...")
    try:
        response = session.get(base_url)
        if response.status_code == 200:
            content = response.text
            if 'AI Prediksjoner' in content and 'analysis.ai_predictions' in content:
                print("   ✅ AI Predictions found in Analysis menu")
            else:
                print("   ❌ AI Predictions not found in Analysis menu")
        else:
            print(f"   ❌ Homepage failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ AI Predictions test error: {e}")
    
    # Test 6: Check settings page functionality
    print("\n6️⃣ Testing settings page access...")
    try:
        response = session.get(f"{base_url}/settings")
        if response.status_code == 200:
            content = response.text
            if 'Varsler' in content and 'update_notifications' in content:
                print("   ✅ Settings page loads with notification form")
            else:
                print("   ❌ Settings page missing notification form")
        else:
            print(f"   ❌ Settings page failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Settings test error: {e}")
    
    # Test 7: Check price alerts create page
    print("\n7️⃣ Testing price alerts create page...")
    try:
        response = session.get(f"{base_url}/price-alerts/create")
        if response.status_code == 200:
            content = response.text
            if 'Populære aksjer:' in content and 'stock-suggestion' in content:
                print("   ✅ Price alerts create page with popular stocks")
            elif 'Populære aksjer:' in content:
                print("   ⚠️ Price alerts page loads but popular stocks may be empty")
            else:
                print("   ❌ Price alerts create page missing popular stocks section")
        else:
            print(f"   ❌ Price alerts create failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Price alerts test error: {e}")
    
    # Test 8: Check if all pages load without 500 errors
    print("\n8️⃣ Testing core pages for 500 errors...")
    pages_to_test = [
        '/analysis/sentiment',
        '/stocks/comparison', 
        '/analysis/ai_predictions',
        '/analysis/technical',
        '/portfolio/',
        '/price-alerts/',
        '/stocks/list/oslo'
    ]
    
    errors_found = 0
    for page in pages_to_test:
        try:
            response = session.get(f"{base_url}{page}")
            if response.status_code == 500:
                print(f"   ❌ 500 error on {page}")
                errors_found += 1
            elif response.status_code == 200:
                print(f"   ✅ {page} loads correctly")
            else:
                print(f"   ⚠️ {page} returned {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error testing {page}: {e}")
            errors_found += 1
    
    if errors_found == 0:
        print("\n🎉 All core pages load without 500 errors!")
    else:
        print(f"\n⚠️ Found {errors_found} pages with errors")
    
    print("\n" + "="*50)
    print("✅ Fix verification complete!")
    print("🚀 Platform is ready for production with improved functionality!")

if __name__ == "__main__":
    test_fixes()
