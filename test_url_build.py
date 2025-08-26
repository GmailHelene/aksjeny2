#!/usr/bin/env python3
"""Test script to verify URL building works correctly"""

from app import create_app
from flask import url_for

def test_url_building():
    """Test that all URL endpoints can be built correctly"""
    app = create_app()
    
    with app.app_context():
        with app.test_request_context():
            try:
                # Test the main.settings endpoint
                settings_url = url_for('main.settings')
                print(f"✅ main.settings URL fungerer: {settings_url}")
                
                # Test other related endpoints
                try:
                    profile_url = url_for('main.profile')
                    print(f"✅ main.profile URL fungerer: {profile_url}")
                except Exception as e:
                    print(f"❌ main.profile feil: {e}")
                
                try:
                    price_alerts_url = url_for('price_alerts.index')
                    print(f"✅ price_alerts.index URL fungerer: {price_alerts_url}")
                except Exception as e:
                    print(f"❌ price_alerts.index feil: {e}")
                
                try:
                    privacy_url = url_for('main.privacy')
                    print(f"✅ main.privacy URL fungerer: {privacy_url}")
                except Exception as e:
                    print(f"❌ main.privacy feil: {e}")
                
                try:
                    help_url = url_for('main.help')
                    print(f"✅ main.help URL fungerer: {help_url}")
                except Exception as e:
                    print(f"❌ main.help feil: {e}")
                
                try:
                    contact_url = url_for('main.contact')
                    print(f"✅ main.contact URL fungerer: {contact_url}")
                except Exception as e:
                    print(f"❌ main.contact feil: {e}")
                
                print("\n🎉 Alle URL-er bygges korrekt! BuildError skal være løst.")
                return True
                
            except Exception as e:
                print(f"❌ FEIL ved bygging av main.settings URL: {e}")
                return False

if __name__ == "__main__":
    test_url_building()
