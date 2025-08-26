#!/usr/bin/env python3
"""
Test to verify the Norwegian Intel Shipping Intelligence icon fix
"""

import requests
from bs4 import BeautifulSoup

def test_norwegian_intel_icons():
    """Test that all icons are properly displayed on Norwegian Intel page"""
    print("🧪 Testing Norwegian Intel Icons...")
    
    try:
        # Test the main Norwegian Intel page
        response = requests.get("https://aksjeradar.trade/norwegian-intel/", timeout=30)
        
        if response.status_code == 200:
            print("✅ Norwegian Intel page loads successfully")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all icon elements
            icons = soup.find_all('i', class_=lambda x: x and ('bi' in x or 'fas' in x or 'fa' in x))
            
            bootstrap_icons = []
            fontawesome_icons = []
            
            for icon in icons:
                classes = icon.get('class', [])
                if 'bi' in classes:
                    bootstrap_icons.append(' '.join(classes))
                elif 'fas' in classes or 'fa' in classes:
                    fontawesome_icons.append(' '.join(classes))
            
            print(f"Found {len(bootstrap_icons)} Bootstrap icons:")
            for icon in bootstrap_icons:
                print(f"  ✅ {icon}")
                
            if fontawesome_icons:
                print(f"Found {len(fontawesome_icons)} FontAwesome icons (potential issues):")
                for icon in fontawesome_icons:
                    print(f"  ⚠️  {icon}")
            else:
                print("✅ No FontAwesome icons found - all icons should display correctly")
            
            # Check specifically for shipping intelligence card
            shipping_card = soup.find('h5', string='Shipping Intelligence')
            if shipping_card:
                icon_div = shipping_card.find_previous('div', class_='feature-icon')
                if icon_div:
                    icon = icon_div.find('i')
                    if icon:
                        icon_classes = ' '.join(icon.get('class', []))
                        print(f"✅ Shipping Intelligence icon: {icon_classes}")
                        
                        if 'bi' in icon_classes:
                            print("✅ Shipping Intelligence now uses Bootstrap icon - should display correctly")
                        else:
                            print("❌ Shipping Intelligence still uses non-Bootstrap icon")
                    else:
                        print("❌ No icon found for Shipping Intelligence")
                else:
                    print("❌ No icon div found for Shipping Intelligence")
            else:
                print("❌ Shipping Intelligence card not found")
        else:
            print(f"❌ Page failed to load: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing icons: {e}")

if __name__ == "__main__":
    test_norwegian_intel_icons()
    print("\n🎯 Icon fix verification complete!")
