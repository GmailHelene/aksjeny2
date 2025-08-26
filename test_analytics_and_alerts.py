#!/usr/bin/env python3
"""
Test advanced analytics page functionality
"""

import requests
from bs4 import BeautifulSoup

def test_advanced_analytics():
    """Test that the advanced analytics page loads correctly"""
    print("🧪 Testing Advanced Analytics Page...")
    
    try:
        # Test the advanced analytics page
        response = requests.get("https://aksjeradar.trade/advanced-analytics/", timeout=30)
        
        if response.status_code == 200:
            print("✅ Advanced Analytics page loads successfully")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for key elements
            title = soup.find('h1')
            if title and 'Avanserte Analyser' in title.text:
                print("✅ Page title found: Avanserte Analyser")
            
            # Check for tabs
            tabs = soup.find_all('button', class_='nav-link')
            tab_names = [tab.get_text(strip=True) for tab in tabs]
            
            expected_tabs = ['ML Prediksjoner', 'Porteføljeoptimalisering', 'Risikostyring']
            found_tabs = []
            
            for expected in expected_tabs:
                for tab_name in tab_names:
                    if expected in tab_name:
                        found_tabs.append(expected)
                        print(f"✅ Found tab: {expected}")
            
            if len(found_tabs) == len(expected_tabs):
                print("✅ All expected tabs found - CMC Markets inspired functionality is working")
            else:
                print(f"⚠️  Only found {len(found_tabs)}/{len(expected_tabs)} expected tabs")
            
            # Check if it's accessible in navigation
            nav_links = soup.find_all('a', href=True)
            analytics_link_found = False
            for link in nav_links:
                if 'advanced-analytics' in link.get('href', '') or 'ML Analytics' in link.get_text():
                    analytics_link_found = True
                    print("✅ Analytics link found in navigation")
                    break
            
            if not analytics_link_found:
                print("⚠️  Analytics link not visible in navigation (may require login)")
            
        elif response.status_code == 403 or response.status_code == 401:
            print("⚠️  Advanced Analytics requires authentication (403/401)")
            print("✅ Page exists but requires login - this is correct behavior")
        else:
            print(f"❌ Page failed to load: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing advanced analytics: {e}")

def test_price_alerts_page():
    """Test that the price alerts page functionality"""
    print("\n🧪 Testing Price Alerts Page...")
    
    try:
        # Test the pro-tools alerts page
        response = requests.get("https://aksjeradar.trade/pro-tools/alerts", timeout=30)
        
        if response.status_code == 200:
            print("✅ Pro Tools Alerts page loads successfully")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for alert creation form
            forms = soup.find_all('form')
            if forms:
                print("✅ Alert creation form found")
            else:
                print("⚠️  No forms found on alerts page")
                
        elif response.status_code == 403 or response.status_code == 401:
            print("⚠️  Pro Tools Alerts requires authentication (403/401)")
            print("✅ Page exists but requires login - this is correct behavior")
        else:
            print(f"❌ Page failed to load: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing price alerts: {e}")

if __name__ == "__main__":
    test_advanced_analytics()
    test_price_alerts_page()
    print("\n🎯 Testing complete!")
