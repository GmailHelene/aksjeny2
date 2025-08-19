#!/usr/bin/env python3

import sys
import os
sys.path.append('/workspaces/aksjeny')

from app import create_app
from app.models import User
from flask_login import login_user

def test_real_authentication():
    """Test authentication using proper Flask-Login methods"""
    
    app = create_app()
    
    with app.app_context():
        # Find user
        user = User.query.filter_by(username='helene_luxus').first()
        if not user:
            print("❌ User not found!")
            return
            
        print(f"✅ Found user: {user.username}")
        
        # Test with proper Flask-Login authentication
        with app.test_client() as client:
            # Simulate proper login using session variables
            with client.session_transaction() as sess:
                # Store user_id in session (this is what Flask-Login does)
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
                
            print("🔍 Testing homepage with properly authenticated user...")
            response = client.get('/')
            
            print(f"Status code: {response.status_code}")
            
            html_content = response.get_data(as_text=True)
            
            # Check for authentication status
            if 'current_user.is_authenticated' in html_content:
                print("✅ current_user.is_authenticated found in template")
            else:
                print("❌ current_user.is_authenticated not found")
            
            # Check what's in user_stats
            if 'user_stats' in html_content:
                print("✅ user_stats found in template")
                
                # Check for recent activities specifically
                if 'recent_activities' in html_content:
                    print("✅ recent_activities found in template")
                    
                    # Count activities in HTML
                    activity_count = html_content.count('activity-item')
                    print(f"📊 Found {activity_count} activity items in HTML")
                    
                    # Check for specific stock symbols
                    stock_symbols = ['LSG.OL', 'SALM.OL', 'EQNR.OL', 'NHY.OL', 'SUBSEA.OL']
                    found_symbols = []
                    for symbol in stock_symbols:
                        if symbol in html_content:
                            found_symbols.append(symbol)
                    
                    print(f"🎯 Found stock symbols: {', '.join(found_symbols)}")
                    
                    if found_symbols:
                        print("✅ Real user activity data is displaying correctly!")
                    else:
                        print("❌ No user stock symbols found - activities not showing")
                        
                else:
                    print("❌ recent_activities not found in template")
            else:
                print("❌ user_stats not found in template")
                
            # Check for fallback message
            if 'Velkommen til' in html_content and 'dashboard' in html_content.lower():
                print("ℹ️ Showing fallback welcome message")
            else:
                print("ℹ️ Not showing fallback welcome message")

if __name__ == "__main__":
    test_real_authentication()
