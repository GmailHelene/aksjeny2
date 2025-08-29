#!/usr/bin/env python3
"""
Test script to debug the profile route redirect issue
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Favorites
from flask import url_for
from flask_login import current_user

def test_profile_route_detailed():
    print("🔍 Detailed profile route debugging...")
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            # First check if user exists
            user = User.query.filter_by(email='test@example.com').first()
            if not user:
                print("❌ Test user not found")
                return False
                
            print(f"✅ Found test user: {user.email} (ID: {user.id})")
            
            # Test login first
            print("\n🔐 Testing login...")
            
            # Test login with proper form data
            login_data = {
                'email': 'test@example.com',
                'password': 'testpassword',
                'submit': 'Logg inn'
            }
            
            login_response = client.post('/auth/login', data=login_data, follow_redirects=False)
            print(f"Login response status: {login_response.status_code}")
            
            if login_response.status_code == 302:
                print(f"Login redirected to: {login_response.location}")
                
                # Follow the redirect
                follow_response = client.get(login_response.location, follow_redirects=False)
                print(f"After redirect status: {follow_response.status_code}")
                if follow_response.status_code == 200:
                    print("✅ Login redirect successful")
                else:
                    print(f"❌ Login redirect failed: {follow_response.status_code}")
                    
            # Now test profile page with debug
            print("\n👤 Testing profile page access...")
            
            # Check auth status before profile request
            with client.session_transaction() as sess:
                print(f"Session before profile request: {dict(sess)}")
            
            # Test profile page access
            profile_response = client.get('/profile', follow_redirects=False)
            print(f"Profile response status: {profile_response.status_code}")
            
            if profile_response.status_code == 302:
                print(f"Profile redirected to: {profile_response.location}")
                
                # Check if redirecting to demo
                if '/demo' in profile_response.location:
                    print("❌ Profile is redirecting to /demo - this suggests authentication issue")
                    
                    # Let's check if the unauthorized handler is being triggered
                    print("\n🔍 Testing authentication state...")
                    
                    # Try to access another authenticated route
                    dashboard_response = client.get('/dashboard', follow_redirects=False)
                    print(f"Dashboard response status: {dashboard_response.status_code}")
                    if dashboard_response.status_code == 302:
                        print(f"Dashboard redirected to: {dashboard_response.location}")
                        
                    # Test if we can access any authenticated route
                    subscription_response = client.get('/my-subscription', follow_redirects=False)
                    print(f"Subscription response status: {subscription_response.status_code}")
                    if subscription_response.status_code == 302:
                        print(f"Subscription redirected to: {subscription_response.location}")
                        
                else:
                    print(f"Profile redirecting to: {profile_response.location}")
                    
            elif profile_response.status_code == 200:
                print("✅ Profile page loaded successfully")
                content = profile_response.data.decode()
                if 'no favorites' in content.lower():
                    print("❌ Profile shows 'no favorites'")
                else:
                    print("✅ Profile loaded without 'no favorites' message")
                    
            else:
                print(f"❌ Unexpected profile response status: {profile_response.status_code}")
                
            # Test if we can access the URL patterns
            print("\n🔗 Testing URL patterns...")
            try:
                with app.test_request_context():
                    profile_url = url_for('main.profile')
                    demo_url = url_for('main.demo')
                    print(f"Profile URL: {profile_url}")
                    print(f"Demo URL: {demo_url}")
            except Exception as url_error:
                print(f"URL generation error: {url_error}")
            
            return True

if __name__ == '__main__':
    test_profile_route_detailed()
