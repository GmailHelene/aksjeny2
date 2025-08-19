#!/usr/bin/env python3

"""
Test authentication by properly handling CSRF or disabling it for testing
"""

from app import create_app, db
from app.models.user import User
from flask_login import current_user
import sys

def test_authentication_with_csrf():
    """Test authentication with proper CSRF handling"""
    print("🔍 Testing authentication with CSRF handling...")
    
    app = create_app()
    
    # Disable CSRF for testing
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        # Find our test user
        user = User.query.filter_by(username='helene_luxus').first()
        if not user:
            print("❌ Test user helene_luxus not found")
            return
            
        print(f"✅ Found user: {user.username}")
        print(f"   User ID: {user.id}")
        print(f"   User email: {user.email}")
        
        # Test authentication through auth blueprint login route
        with app.test_client() as client:
            print("\n🔍 Step 1: Testing auth blueprint login...")
            
            # Now attempt to login with credentials (using email, not username)
            login_data = {
                'email': 'helene.luxus@example.com',  # Use email from our creation script
                'password': 'password123'  # From our creation script
            }
            
            response = client.post('/auth/login', data=login_data, follow_redirects=True)
            print(f"   Login response status: {response.status_code}")
            
            # Check if login was successful by looking at response content
            content = response.get_data(as_text=True)
            
            # Look for login success indicators
            login_success_indicators = [
                'logout',  # Logout link appears when logged in
                'helene_luxus',  # Username appears when logged in
                'Din aktivitet',  # Norwegian for "Your activity"
                'Velkommen tilbake',  # Norwegian for "Welcome back"
                'user_stats'  # User stats should be present
            ]
            
            print("\n🔍 Checking login success indicators:")
            for indicator in login_success_indicators:
                found = indicator in content
                print(f"   {'✅' if found else '❌'} {indicator}: {found}")
            
            # Check for login failure indicators
            login_failure_indicators = [
                'Invalid username or password',
                'Login failed',
                'csrf',
                'form-control-error'
            ]
            
            print("\n🔍 Checking login failure indicators:")
            for indicator in login_failure_indicators:
                found = indicator.lower() in content.lower()
                print(f"   {'✅' if not found else '❌'} {indicator}: {'Not Found' if not found else 'Found - Problem!'}")
            
            # Now test the homepage after login
            print("\n🔍 Step 2: Testing homepage after login...")
            response = client.get('/')
            print(f"   Homepage status: {response.status_code}")
            
            content = response.get_data(as_text=True)
            
            # Look for authenticated homepage content
            auth_indicators = [
                'current_user.is_authenticated',
                'user_stats.recent_activities', 
                'Din aktivitet',
                'helene_luxus'
            ]
            
            print("\n🔍 Checking authenticated homepage content:")
            for indicator in auth_indicators:
                found = indicator in content
                print(f"   {'✅' if found else '❌'} {indicator}: {found}")
            
            # Look for activity stock symbols
            activity_symbols = ['EQNR.OL', 'DNB.OL', 'TEL.OL', 'SALM.OL', 'LSG.OL']
            print("\n🔍 Checking for activity stock symbols:")
            activity_found = 0
            for symbol in activity_symbols:
                found = symbol in content
                if found:
                    activity_found += 1
                print(f"   {'✅' if found else '❌'} {symbol}: {found}")
                
            print(f"\n📊 Activity symbols found: {activity_found}/{len(activity_symbols)}")
                
            # Check for generic welcome message (should NOT appear when authenticated)
            fallback_indicators = [
                'Velkommen til finansiell analyse',
                'comprehensive investment platform',
                'no recent activity'
            ]
            
            print("\n🔍 Checking for fallback welcome message (should NOT appear):")
            for indicator in fallback_indicators:
                found = indicator in content
                print(f"   {'✅' if not found else '❌'} {indicator}: {'Not Found (Good!)' if not found else 'Found (Problem!)'}")
                
            # Check authentication status in template
            auth_template_indicators = [
                '{% if current_user.is_authenticated %}',
                '{% if user_stats.recent_activities %}',
                'current_user.username'
            ]
            
            print("\n🔍 Checking template authentication logic:")
            for indicator in auth_template_indicators:
                found = indicator in content
                print(f"   {'✅' if found else '❌'} {indicator}: {found}")
                
            # Summary
            print(f"\n📋 SUMMARY:")
            print(f"   Login Status: {'✅ SUCCESS' if any(indicator in content for indicator in login_success_indicators) else '❌ FAILED'}")
            print(f"   Activity Data: {'✅ PRESENT' if activity_found > 0 else '❌ MISSING'}")
            print(f"   Authentication Flow: {'✅ WORKING' if 'helene_luxus' in content or 'Din aktivitet' in content else '❌ NOT WORKING'}")

if __name__ == "__main__":
    test_authentication_with_csrf()
