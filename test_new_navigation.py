#!/usr/bin/env python3
"""
Test Navigation System - Completely New PC and Mobile Navigation

Dette scriptet tester den nye navigasjonsløsningen som ble implementert 
for å erstatte den gamle, konfliktfylte navigasjonen.

Ny navigasjon har:
- Separate CSS for desktop (769px+) og mobile (768px-)  
- Ren JavaScript uten konflikter
- Hover-baserte dropdowns på desktop
- Klikk-baserte dropdowns på mobile
- Hamburger menu for mobile
"""

import requests
import time
from datetime import datetime

def test_navigation_pages():
    """Test at navigasjonssystemet fungerer på alle hovedsider"""
    
    base_url = "http://localhost:5001"
    
    # Alle hovedsider som skal testes
    navigation_pages = [
        "/",
        "/portfolio",
        "/analysis",
        "/analysis/predictions", 
        "/analysis/currency-overview",
        "/market",
        "/market/overview",
        "/market/screener",
        "/market/gainers-losers", 
        "/news",
        "/alerts",
        "/tools",
        "/tools/calculator",
        "/buffett",
        "/about",
        "/contact"
    ]
    
    print("🧪 Testing Navigation System")
    print("=" * 50)
    print(f"🕐 Test startet: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    success_count = 0
    total_count = len(navigation_pages)
    
    for page in navigation_pages:
        try:
            url = f"{base_url}{page}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Sjekk at den nye navigasjonsstrukturen er til stede
                html = response.text
                
                checks = {
                    "Desktop nav": 'desktop-nav d-none d-lg-flex' in html,
                    "Mobile nav": 'mobile-nav d-lg-none' in html,
                    "Clean navbar": 'class="navbar"' in html and 'navbar-expand-lg' not in html,
                    "Mobile toggle": 'mobile-nav-toggle' in html,
                    "New JS": 'New clean navigation system loaded' in html
                }
                
                all_checks_passed = all(checks.values())
                
                if all_checks_passed:
                    print(f"✅ {page:<30} - Navigation OK")
                    success_count += 1
                else:
                    print(f"⚠️  {page:<30} - Navigation issues:")
                    for check, passed in checks.items():
                        if not passed:
                            print(f"   ❌ {check}")
            else:
                print(f"❌ {page:<30} - HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"💥 {page:<30} - Connection error: {str(e)[:50]}")
        except Exception as e:
            print(f"🔥 {page:<30} - Error: {str(e)[:50]}")
    
    print()
    print("=" * 50)
    print(f"📊 Navigation Test Results:")
    print(f"   ✅ Success: {success_count}/{total_count}")
    print(f"   📈 Success rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 ALL NAVIGATION TESTS PASSED! New navigation system is working!")
    else:
        print("⚠️  Some navigation issues detected - review above")
    
    return success_count == total_count

def test_mobile_responsiveness():
    """Test mobile responsiveness ved å sjekke CSS media queries"""
    
    print("\n🔍 Testing Mobile Responsiveness")
    print("-" * 30)
    
    try:
        response = requests.get("http://localhost:5001")
        html = response.text
        
        mobile_features = [
            "@media (max-width: 768px)",
            ".mobile-nav",
            ".desktop-nav",
            "mobile-nav-toggle",
            "mobile-dropdown"
        ]
        
        for feature in mobile_features:
            if feature in html:
                print(f"✅ {feature}")
            else:
                print(f"❌ {feature} - Missing!")
                
    except Exception as e:
        print(f"❌ Mobile test failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing New Navigation System")
    print("Dette tester den helt nye navigasjonsløsningen")
    print("som erstatter den gamle, konfliktfylte navigasjonen.")
    print()
    
    # Test navigasjon på alle sider
    navigation_success = test_navigation_pages()
    
    # Test mobile responsiveness
    test_mobile_responsiveness()
    
    print("\n" + "=" * 60)
    if navigation_success:
        print("🎊 SUCCESS: New navigation system is fully functional!")
        print("✨ PC and mobile navigation working perfectly!")
    else:
        print("⚠️  Issues detected - check logs above")
    print("=" * 60)
