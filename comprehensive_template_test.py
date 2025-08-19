#!/usr/bin/env python3
"""
Comprehensive test to check if dashboard activities are properly passed to template
"""

import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models.user import User
from flask import url_for

def test_dashboard_with_real_data():
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            # Find the user
            user = User.query.filter_by(username='helene_luxus').first()
            if not user:
                print("❌ User 'helene_luxus' not found!")
                return
                
            print(f"✅ Found user: {user.username}")
            
            # Simulate login by setting up session
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
                
            # Get the homepage
            print("🔍 Testing homepage with logged-in user...")
            response = client.get('/')
            
            print(f"Status code: {response.status_code}")
            
            # Get the response data as text
            html_content = response.get_data(as_text=True)
            
            # Check for various activity indicators
            checks = {
                'Din aktivitet': 'Din aktivitet' in html_content,
                'Dine investeringer': 'Dine investeringer' in html_content,
                'LSG.OL mentioned': 'LSG.OL' in html_content,
                'SALM.OL mentioned': 'SALM.OL' in html_content,
                'EQNR.OL mentioned': 'EQNR.OL' in html_content,
                'NHY.OL mentioned': 'NHY.OL' in html_content,
                'SUBSEA.OL mentioned': 'SUBSEA.OL' in html_content,
                'Lagt til mentioned': 'Lagt til' in html_content,
                'Overvåker mentioned': 'Overvåker' in html_content,
                'user_stats javascript': 'user_stats' in html_content,
                'recent_activities javascript': 'recent_activities' in html_content,
                'helene_luxus portfolio name': 'helene_luxus' in html_content,
                'Growth Plays watchlist': 'Growth Plays' in html_content
            }
            
            print("\n🔍 Checking for activity indicators in template:")
            for check_name, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check_name}: {result}")
            
            # Let's also check if there's any sign of the user being logged in at all
            authentication_checks = {
                'user is authenticated': 'is_authenticated' in html_content or 'current_user' in html_content,
                'login link present': 'login' in html_content.lower(),
                'logout link present': 'logout' in html_content.lower(),
            }
            
            print("\n🔒 Authentication status checks:")
            for check_name, result in authentication_checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check_name}: {result}")
            
            # Check for any error messages in template
            if 'error' in html_content.lower() or 'exception' in html_content.lower():
                print("⚠️ Found error/exception in HTML content")
            
            # Look for specific activity section
            activity_section_found = False
            if 'Din aktivitet' in html_content:
                # Find the section and see what's around it
                activity_index = html_content.find('Din aktivitet')
                if activity_index != -1:
                    # Get 1000 characters around the activity section
                    start = max(0, activity_index - 500)
                    end = min(len(html_content), activity_index + 500)
                    activity_section = html_content[start:end]
                    
                    print(f"\n📋 Activity section content (around 'Din aktivitet'):")
                    print("=" * 80)
                    print(activity_section)
                    print("=" * 80)
                    
                    activity_section_found = True
            
            if not activity_section_found:
                print("❌ No 'Din aktivitet' section found in template")
            
            print(f"\n✅ Test completed")

if __name__ == "__main__":
    test_dashboard_with_real_data()
