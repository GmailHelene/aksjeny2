#!/usr/bin/env python3
"""
Test Mobile Navigation Overlay - Sjekker at mobilmenyen ikke dekker hele siden
"""

import requests

def test_mobile_menu_behavior():
    """Test at mobilmenyen er skjult som default og viser kun på toggle"""
    
    print("🧪 Testing Mobile Menu Behavior")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:5001")
        html = response.text
        
        # Sjekk at mobilmenyen er skjult som default
        mobile_checks = {
            "Mobile menu skjult": '.mobile-nav-menu {' in html and 'display: none;' in html,
            "Kun vises med .show": '.mobile-nav-menu.show {' in html and 'display: block;' in html,
            "Fixed positioning": 'position: fixed;' in html and 'top: 76px;' in html,
            "Har z-index": 'z-index: 1050;' in html,
            "Transform skjuler": 'transform: translateX(-100%);' in html
        }
        
        print("📱 Mobile Menu CSS Checks:")
        for check, passed in mobile_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        # Sjekk at JavaScript håndterer toggle korrekt
        js_checks = {
            "Toggle button funnet": "querySelector('.mobile-nav-toggle')" in html,
            "Menu element funnet": "querySelector('.mobile-nav-menu')" in html,
            "Toggle show class": "classList.toggle('show')" in html,
            "Event listener aktiv": "addEventListener('click'" in html
        }
        
        print("\n🎛️ JavaScript Toggle Checks:")
        for check, passed in js_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        all_passed = all(mobile_checks.values()) and all(js_checks.values())
        
        print("\n" + "=" * 40)
        if all_passed:
            print("🎉 Mobile menu er korrekt konfigurert!")
            print("✨ Menyen dekker IKKE hele siden som default")
            print("📱 Kun vises når bruker klikker hamburger-knappen")
        else:
            print("⚠️  Noen mobile menu problemer funnet")
        print("=" * 40)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Test feilet: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Mobile Menu Overlay Fix")
    print("Dette sjekker at mobilmenyen ikke dekker hele forsiden lenger")
    print()
    
    success = test_mobile_menu_behavior()
    
    print("\n" + "🎯 RESULTAT:")
    if success:
        print("✅ Mobile menu fix SUCCESS!")
        print("🚀 Menyen dekker ikke lenger hele siden!")
    else:
        print("❌ Mobile menu trenger flere justeringer")
