#!/usr/bin/env python3
"""
Test script to debug the favorites loading mismatch
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Favorites
from flask import session
from flask_login import current_user
import re

def test_favorites_loading_debug():
    print("🔍 Debugging favorites loading mismatch...")
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            # First, check what's actually in the database
            print("\n📊 Database state check:")
            user = User.query.filter_by(email='test@example.com').first()
            print(f"Test user: ID={user.id}, Email={user.email}")
            
            all_favorites = Favorites.query.all()
            print(f"Total favorites in database: {len(all_favorites)}")
            for fav in all_favorites:
                print(f"  - Favorite: user_id={fav.user_id}, symbol={fav.symbol}, name={fav.name}")
            
            user_5_favorites = Favorites.query.filter_by(user_id=5).all()
            print(f"Favorites for user ID 5: {len(user_5_favorites)}")
            for fav in user_5_favorites:
                print(f"  - User 5 favorite: symbol={fav.symbol}, name={fav.name}")
            
            test_user_favorites = Favorites.query.filter_by(user_id=user.id).all()
            print(f"Favorites for test user (ID {user.id}): {len(test_user_favorites)}")
            for fav in test_user_favorites:
                print(f"  - Test user favorite: symbol={fav.symbol}, name={fav.name}")
            
            print("\n🔐 Performing authentication...")
            # Get CSRF and login
            login_page = client.get('/login')
            csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]*)"', login_page.data.decode())
            csrf_token = csrf_match.group(1)
            
            login_data = {
                'csrf_token': csrf_token,
                'email': 'test@example.com',
                'password': 'testpassword',
                'submit': 'Logg inn'
            }
            
            login_response = client.post('/auth/login', data=login_data, follow_redirects=False)
            print(f"Login status: {login_response.status_code}")
            
            if login_response.status_code == 302:
                # Follow redirect to establish session
                client.get(login_response.location)
                print("✅ Authentication established")
                
                # Now create a test route to check what user ID the profile code sees
                @app.route('/debug-user-id')
                def debug_user_id():
                    from flask_login import current_user
                    result = {
                        'is_authenticated': current_user.is_authenticated,
                        'has_id_attr': hasattr(current_user, 'id'),
                        'id_value': getattr(current_user, 'id', None),
                        'get_id_method': current_user.get_id() if hasattr(current_user, 'get_id') else None,
                        'user_type': type(current_user).__name__
                    }
                    
                    # Try the same logic as the profile route
                    user_id = None
                    if hasattr(current_user, 'id') and current_user.id:
                        user_id = current_user.id
                    elif hasattr(current_user, 'get_id'):
                        try:
                            user_id_str = current_user.get_id()
                            if user_id_str:
                                user_id = int(user_id_str)
                        except (ValueError, TypeError):
                            pass
                    
                    result['determined_user_id'] = user_id
                    
                    # Test favorites query with this user_id
                    if user_id:
                        from app.models.favorites import Favorites
                        favorites = Favorites.query.filter_by(user_id=user_id).all()
                        result['favorites_count'] = len(favorites)
                        result['favorites'] = [{'symbol': f.symbol, 'name': f.name} for f in favorites]
                    else:
                        result['favorites_count'] = 0
                        result['favorites'] = []
                    
                    return str(result)
                
                print("\n👤 Testing user ID detection in authenticated context...")
                debug_response = client.get('/debug-user-id')
                print(f"Debug response: {debug_response.data.decode()}")
                
                print("\n🎯 Testing actual profile route...")
                profile_response = client.get('/profile')
                print(f"Profile status: {profile_response.status_code}")
                
                if profile_response.status_code == 200:
                    content = profile_response.data.decode()
                    if 'no favorites' in content.lower() or 'ingen favoritter' in content.lower():
                        print("❌ Profile still shows 'no favorites'")
                        
                        # Check if debug output is in the profile
                        if 'DEBUG: About to load favorites' in content:
                            print("✅ Debug logging present in profile")
                        else:
                            print("❌ Debug logging missing from profile")
                            
                        # Look for the user ID in the logs
                        user_id_match = re.search(r'user ID: (\d+)', content)
                        if user_id_match:
                            profile_user_id = user_id_match.group(1)
                            print(f"Profile route detected user ID: {profile_user_id}")
                        else:
                            print("❌ Could not find user ID in profile output")
                    else:
                        print("✅ Profile does not show 'no favorites'")
                        
                        # Check how many favorites are shown
                        fav_symbols = re.findall(r'([A-Z]{3,5})', content)
                        print(f"Found stock symbols in profile: {fav_symbols}")
            
    return True

if __name__ == '__main__':
    test_favorites_loading_debug()
