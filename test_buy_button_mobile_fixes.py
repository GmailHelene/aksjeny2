#!/usr/bin/env python3
"""
Test script to verify buy button and mobile menu fixes
"""

import requests
from bs4 import BeautifulSoup
import json

def test_buy_buttons():
    """Test that buy buttons are properly configured"""
    print("🧪 Testing Buy Button Configuration...")
    
    try:
        # Get market overview page
        response = requests.get('http://localhost:5001/analysis/market-overview')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all buy buttons
        buy_buttons = soup.find_all('button', class_='external-buy-btn')
        print(f"✅ Found {len(buy_buttons)} external buy buttons")
        
        # Check oslo stocks have oslo market data
        oslo_buttons = [btn for btn in buy_buttons if btn.get('data-market') == 'oslo']
        global_buttons = [btn for btn in buy_buttons if btn.get('data-market') == 'global']
        
        print(f"✅ Oslo market buttons: {len(oslo_buttons)}")
        print(f"✅ Global market buttons: {len(global_buttons)}")
        
        # Verify no old add-to-portfolio buttons remain
        old_buttons = soup.find_all('button', class_='add-to-portfolio')
        if old_buttons:
            print(f"❌ Found {len(old_buttons)} old add-to-portfolio buttons")
            return False
        else:
            print("✅ No old add-to-portfolio buttons found")
        
        # Check JavaScript contains external buy functionality
        script_tags = soup.find_all('script')
        has_external_buy_js = any('external-buy-btn' in str(script) for script in script_tags)
        
        if has_external_buy_js:
            print("✅ External buy JavaScript functionality found")
        else:
            print("❌ External buy JavaScript functionality not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing buy buttons: {e}")
        return False

def test_mobile_navigation():
    """Test mobile navigation structure"""
    print("\n🧪 Testing Mobile Navigation...")
    
    try:
        # Get main page to check navigation
        response = requests.get('http://localhost:5001/')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for stocks dropdown
        stocks_dropdown = soup.find('a', id='stocksDropdown')
        if stocks_dropdown:
            print("✅ Stocks dropdown found")
        else:
            print("❌ Stocks dropdown not found")
            return False
        
        # Check for user dropdown elements
        user_dropdown = soup.find('a', id='navbarDropdown')
        auth_dropdown = soup.find('a', id='authDropdown')
        
        if user_dropdown or auth_dropdown:
            print("✅ User/auth dropdown found")
        else:
            print("❌ User/auth dropdown not found")
            return False
        
        # Check for mobile nav sections
        mobile_sections = soup.find_all('div', class_='mobile-nav-section')
        print(f"✅ Found {len(mobile_sections)} mobile navigation sections")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing mobile navigation: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Buy Button and Mobile Menu Tests\n")
    
    buy_buttons_ok = test_buy_buttons()
    mobile_nav_ok = test_mobile_navigation()
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS:")
    print(f"Buy Buttons: {'✅ PASS' if buy_buttons_ok else '❌ FAIL'}")
    print(f"Mobile Navigation: {'✅ PASS' if mobile_nav_ok else '❌ FAIL'}")
    
    if buy_buttons_ok and mobile_nav_ok:
        print("\n🎉 All tests passed! Issues should be resolved.")
    else:
        print("\n⚠️  Some tests failed. Issues may still exist.")

if __name__ == "__main__":
    main()
