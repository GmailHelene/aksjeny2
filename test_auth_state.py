#!/usr/bin/env python3
"""
Test script to deeply debug Flask-Login authentication state
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Favorites
from flask import session, g
from flask_login import current_user

def test_authentication_state():
    print("🔍 Deep authentication state debugging...")
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            # Check user exists
            user = User.query.filter_by(email='test@example.com').first()
            print(f"✅ Test user exists: {user.email} (ID: {user.id})")
            
            print("\n🔐 Step 1: Initial state check")
            with client.session_transaction() as sess:
                print(f"Initial session: {dict(sess)}")
                
            print("\n🔐 Step 2: Perform login")
            login_data = {
                'email': 'test@example.com',
                'password': 'testpassword',
                'submit': 'Logg inn'
            }
            
            login_response = client.post('/auth/login', data=login_data, follow_redirects=False)
            print(f"Login status: {login_response.status_code}")
            print(f"Login headers: {dict(login_response.headers)}")
            
            # Check session after login
            with client.session_transaction() as sess:
                print(f"Session after login: {dict(sess)}")
                
            print("\n🔐 Step 3: Test authentication directly within request context")
            # Make a request that checks authentication state within the app context
            
            def check_auth_state():
                print(f"current_user.is_authenticated: {current_user.is_authenticated}")
                print(f"current_user: {current_user}")
                print(f"session: {dict(session)}")
                if hasattr(current_user, 'id'):
                    print(f"current_user.id: {current_user.id}")
                if hasattr(current_user, 'email'):
                    print(f"current_user.email: {current_user.email}")
                return "OK"
                
            # Add a test route to check auth state
            @app.route('/test-auth-state')
            def test_auth_state_route():
                return check_auth_state()
                
            print("\n🔐 Step 4: Check auth state via test route")
            auth_test_response = client.get('/test-auth-state')
            print(f"Auth test response: {auth_test_response.data.decode()}")
            
            print("\n👤 Step 5: Test profile access with detailed debugging")
            # Add debug middleware to check what happens during profile access
            original_profile_view = None
            
            # Temporarily patch the access_required decorator to add logging
            from app.utils.access_control import access_required
            original_access_required = access_required
            
            def debug_access_required(f):
                def wrapper(*args, **kwargs):
                    print(f"🔍 DEBUG: access_required called for {f.__name__}")
                    print(f"🔍 DEBUG: current_user.is_authenticated = {current_user.is_authenticated}")
                    print(f"🔍 DEBUG: current_user = {current_user}")
                    result = original_access_required(f)(*args, **kwargs)
                    print(f"🔍 DEBUG: access_required returning: {type(result)}")
                    return result
                return wrapper
            
            # Test profile access
            profile_response = client.get('/profile', follow_redirects=False)
            print(f"Profile status: {profile_response.status_code}")
            if profile_response.status_code == 302:
                print(f"Profile redirected to: {profile_response.location}")
            
    return True

if __name__ == '__main__':
    test_authentication_state()
