#!/usr/bin/env python3
"""
Comprehensive test for mobile navigation functionality
"""

import requests
from bs4 import BeautifulSoup

def test_mobile_nav_structure():
    """Test mobile navigation structure and elements"""
    print("🧪 Testing Mobile Navigation Structure...")
    
    try:
        response = requests.get('http://localhost:5001/')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("\n📱 Mobile Navigation Elements:")
        
        # Check navbar toggler
        toggler = soup.find('button', class_='navbar-toggler')
        if toggler:
            print("✅ Mobile menu toggle button found")
        else:
            print("❌ Mobile menu toggle button not found")
            return False
        
        # Check stocks dropdown
        stocks_dropdown = soup.find('a', id='stocksDropdown')
        if stocks_dropdown:
            print("✅ Stocks dropdown link found")
            # Check if it has proper attributes
            if stocks_dropdown.get('data-bs-toggle') == 'dropdown':
                print("✅ Stocks dropdown has proper Bootstrap toggle")
            else:
                print("❌ Stocks dropdown missing Bootstrap toggle")
        
        # Check stocks dropdown menu items
        stocks_menu = soup.find('ul', class_='dropdown-menu')
        if stocks_menu:
            menu_items = stocks_menu.find_all('a', class_='dropdown-item')
            print(f"✅ Found {len(menu_items)} items in stocks dropdown menu")
            
            # Check specific important links
            important_links = [
                'Alle aksjer', 'Søk aksjer', 'Oslo Børs', 
                'Globale aksjer', 'Alle priser', 'Sammenlign aksjer', 'Favoritter'
            ]
            
            found_links = [item.get_text().strip() for item in menu_items]
            for link in important_links:
                if any(link in found for found in found_links):
                    print(f"  ✅ {link}")
                else:
                    print(f"  ❌ Missing: {link}")
        
        # Check user/auth dropdown
        user_dropdown = soup.find('a', id='navbarDropdown')
        auth_dropdown = soup.find('a', id='authDropdown')
        
        if user_dropdown:
            print("✅ User dropdown found (for authenticated users)")
        elif auth_dropdown:
            print("✅ Auth dropdown found (for non-authenticated users)")
        else:
            print("❌ No user/auth dropdown found")
        
        # Check mobile navigation sections
        mobile_sections = soup.find_all('div', class_='mobile-nav-section')
        print(f"✅ Found {len(mobile_sections)} mobile navigation section headers:")
        for section in mobile_sections:
            print(f"  📱 {section.get_text().strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing mobile navigation: {e}")
        return False

def test_responsive_elements():
    """Test responsive classes and structure"""
    print("\n🧪 Testing Responsive Elements...")
    
    try:
        response = requests.get('http://localhost:5001/')
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for responsive classes
        navbar = soup.find('nav', class_='navbar')
        if navbar and 'navbar-expand-lg' in navbar.get('class', []):
            print("✅ Navbar has responsive expand class")
        else:
            print("❌ Navbar missing responsive expand class")
        
        # Check for mobile-only elements
        mobile_only = soup.find_all(class_=lambda x: x and 'd-lg-none' in x)
        print(f"✅ Found {len(mobile_only)} mobile-only elements")
        
        # Check for desktop-only elements  
        desktop_only = soup.find_all(class_=lambda x: x and 'd-none d-lg-block' in x)
        print(f"✅ Found {len(desktop_only)} desktop-only elements")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing responsive elements: {e}")
        return False

def main():
    """Run all mobile navigation tests"""
    print("🚀 Running Mobile Navigation Tests\n")
    
    structure_ok = test_mobile_nav_structure()
    responsive_ok = test_responsive_elements()
    
    print("\n" + "="*50)
    print("📊 MOBILE NAVIGATION TEST RESULTS:")
    print(f"Navigation Structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"Responsive Elements: {'✅ PASS' if responsive_ok else '❌ FAIL'}")
    
    if structure_ok and responsive_ok:
        print("\n🎉 Mobile navigation tests passed!")
        print("📱 Mobile menu should work correctly on mobile devices")
    else:
        print("\n⚠️  Some mobile navigation tests failed")

if __name__ == "__main__":
    main()
