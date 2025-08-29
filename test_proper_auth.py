#!/usr/bin/env python3
"""
Test script to properly authenticate with CSRF and test profile access
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Favorites
from flask import session
from flask_login import current_user
import re

def test_proper_authentication():
    print("🔍 Testing proper authentication with CSRF...")
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            # Check user exists
            user = User.query.filter_by(email='test@example.com').first()
            print(f"✅ Test user exists: {user.email} (ID: {user.id})")
            
            print("\n🔐 Step 1: Get login page to extract CSRF token")
            login_page = client.get('/login')
            print(f"Login page status: {login_page.status_code}")
            
            # Extract CSRF token from the login page
            login_content = login_page.data.decode()
            csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]*)"', login_content)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print(f"✅ Extracted CSRF token: {csrf_token[:20]}...")
            else:
                print("❌ Could not extract CSRF token")
                return False
            
            print("\n🔐 Step 2: Login with proper CSRF token")
            login_data = {
                'csrf_token': csrf_token,
                'email': 'test@example.com',
                'password': 'testpassword',
                'submit': 'Logg inn'
            }
            
            login_response = client.post('/auth/login', data=login_data, follow_redirects=False)
            print(f"Login status: {login_response.status_code}")
            print(f"Login location: {login_response.location if login_response.status_code == 302 else 'N/A'}")
            
            # Check session after login
            with client.session_transaction() as sess:
                print(f"Session after login: {list(sess.keys())}")
                for key, value in sess.items():
                    if key == '_flashes':
                        print(f"  {key}: {value}")
                    else:
                        print(f"  {key}: {type(value)}")
            
            if login_response.status_code == 302 and '/login' not in login_response.location:
                print("✅ Login successful - redirected away from login page")
                
                # Follow the redirect to establish session
                redirect_response = client.get(login_response.location)
                print(f"After login redirect status: {redirect_response.status_code}")
                
            else:
                print("❌ Login failed - stayed on login page")
                return False
            
            print("\n👤 Step 3: Test profile access")
            profile_response = client.get('/profile', follow_redirects=False)
            print(f"Profile status: {profile_response.status_code}")
            
            if profile_response.status_code == 302:
                print(f"Profile redirected to: {profile_response.location}")
                
                # Check what type of redirect this is
                if '/demo' in profile_response.location:
                    print("❌ Profile redirecting to demo (authentication issue)")
                    
                    # Let's test another protected route to confirm
                    dashboard_response = client.get('/dashboard', follow_redirects=False)
                    print(f"Dashboard status: {dashboard_response.status_code}")
                    if dashboard_response.status_code == 302:
                        print(f"Dashboard redirected to: {dashboard_response.location}")
                        
                    # Let's also test with following redirects to see final destination
                    profile_final = client.get('/profile', follow_redirects=True)
                    print(f"Profile final status: {profile_final.status_code}")
                    final_content = profile_final.data.decode()
                    if 'demo' in final_content.lower():
                        print("❌ Profile ultimately shows demo page")
                    elif 'profile' in final_content.lower():
                        print("✅ Profile shows profile content")
                    else:
                        print(f"Profile final content (first 200 chars): {final_content[:200]}")
                        
                else:
                    print(f"Profile redirecting to: {profile_response.location}")
                    
            elif profile_response.status_code == 200:
                print("✅ Profile page loaded successfully")
                content = profile_response.data.decode()
                if 'favorites' in content.lower():
                    print("✅ Profile contains favorites content")
                    if 'no favorites' in content.lower():
                        print("❌ But shows 'no favorites' message")
                    else:
                        print("✅ Profile shows favorites without 'no favorites' message")
                else:
                    print("⚠️ Profile doesn't contain favorites content")
                    
            else:
                print(f"❌ Unexpected profile response: {profile_response.status_code}")
            
    return True

if __name__ == '__main__':
    test_proper_authentication()
