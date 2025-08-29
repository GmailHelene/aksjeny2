#!/usr/bin/env python3
"""
Test script to verify profile favorites loading with proper authentication
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Favorites
from flask import url_for
import requests

def test_profile_with_session():
    print("🧪 Testing profile page with authenticated session...")
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            # First check if user exists
            user = User.query.filter_by(email='test@example.com').first()
            if not user:
                print("❌ Test user not found")
                return False
                
            print(f"✅ Found test user: {user.email} (ID: {user.id})")
            
            # Check favorites
            favorites = Favorites.query.filter_by(user_id=user.id).all()
            print(f"📊 User has {len(favorites)} favorites in database")
            for fav in favorites:
                print(f"  - {fav.symbol}: {fav.name}")
            
            # Test login first
            print("\n🔐 Testing login...")
            
            # Get login page to get CSRF token
            login_page = client.get('/login')
            print(f"Login page status: {login_page.status_code}")
            
            # Login with proper credentials
            login_data = {
                'email': 'test@example.com',
                'password': 'testpassword',
                'submit': 'Logg inn'
            }
            
            login_response = client.post('/auth/login', data=login_data, follow_redirects=True)
            print(f"Login response status: {login_response.status_code}")
            print(f"Login response URL: {login_response.request.path if hasattr(login_response, 'request') else 'N/A'}")
            
            # Check if redirected to dashboard (successful login)
            if b'Dashboard' in login_response.data or b'Hjem' in login_response.data:
                print("✅ Login successful")
            else:
                print("❌ Login failed")
                # print(f"Response content: {login_response.data.decode()[:500]}...")
                
            # Now test profile page
            print("\n👤 Testing profile page...")
            profile_response = client.get('/profile')
            print(f"Profile page status: {profile_response.status_code}")
            
            # Check for favorites content
            profile_content = profile_response.data.decode()
            
            if 'no favorites' in profile_content.lower() or 'ingen favoritter' in profile_content.lower():
                print("❌ Profile shows 'no favorites' despite data in database")
                print("🔍 Let's check for debug output...")
                
                # Look for our debug messages
                if 'DEBUG: About to load favorites' in profile_content:
                    print("✅ Found debug message - favorites loading code is executing")
                else:
                    print("❌ Debug message not found - favorites loading code not executing")
                    
                # Look for user ID info
                if f'User ID: {user.id}' in profile_content:
                    print(f"✅ Found user ID {user.id} in response")
                else:
                    print("❌ User ID not found in response")
                    
            else:
                print("✅ Profile page loaded without 'no favorites' message")
                
                # Check if actual favorites are shown
                for fav in favorites:
                    if fav.symbol in profile_content:
                        print(f"✅ Found favorite {fav.symbol} in profile")
                    else:
                        print(f"❌ Favorite {fav.symbol} not found in profile")
            
            # Print some of the response for debugging
            print(f"\n📄 Profile response excerpt (first 1000 chars):")
            print(profile_content[:1000])
            print("\n" + "="*50)
            
            return True

if __name__ == '__main__':
    test_profile_with_session()
