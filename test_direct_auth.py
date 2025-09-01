#!/usr/bin/env python3
"""
Direct authentication test bypassing form validation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.user import User
from flask_login import login_user
from werkzeug.security import check_password_hash

def test_direct_authentication():
    print("🔐 Testing direct authentication...")
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            # Get the test user
            user = User.query.filter_by(email='test@example.com').first()
            if not user:
                print("❌ Test user not found")
                return False
                
            print(f"✅ Test user found: {user.email} (ID: {user.id})")
            
            # Check password directly
            password_valid = check_password_hash(user.password_hash, 'testpass123')
            print(f"Password validation: {password_valid}")
            
            if not password_valid:
                print("❌ Password validation failed")
                return False
                
            # Simulate a request context and login the user directly
            with client.session_transaction() as sess:
                print(f"Initial session: {dict(sess)}")
                
            # Create a proper request context and login user
            with app.test_request_context():
                login_result = login_user(user, remember=False)
                print(f"Login user result: {login_result}")
                
            # Now test protected routes
            print("\n🔐 Testing protected routes after direct login...")
            
            # Make a request to check if authentication persists
            response = client.get('/profile', follow_redirects=False)
            print(f"Profile access: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Authentication working! Profile returned 200")
                return True
            elif response.status_code == 302:
                print(f"❌ Still redirecting. Location: {response.headers.get('Location', 'Unknown')}")
                return False
            else:
                print(f"❌ Unexpected status: {response.status_code}")
                return False

if __name__ == "__main__":
    success = test_direct_authentication()
    if success:
        print("\n✅ Authentication system is working!")
    else:
        print("\n❌ Authentication system has issues!")
