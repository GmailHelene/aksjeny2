#!/usr/bin/env python3
"""
Test script to isolate the favorites loading issue
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Favorites
import re

def test_simplified_favorites():
    print("🔍 Testing favorites loading in isolated environment...")
    
    app = create_app('development')
    
    with app.test_client() as client:
        with app.app_context():
            # Check database state
            print("\n📊 Database verification:")
            test_user = User.query.filter_by(email='test@example.com').first()
            print(f"Test user: ID={test_user.id}, Email={test_user.email}")
            
            user_5_favorites = Favorites.query.filter_by(user_id=5).all()
            print(f"Favorites for user ID 5: {len(user_5_favorites)}")
            for fav in user_5_favorites:
                print(f"  - Symbol: {fav.symbol}, Name: {fav.name}")
            
            # Authenticate
            print("\n🔐 Authenticating...")
            login_page = client.get('/login')
            csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]*)"', login_page.data.decode())
            csrf_token = csrf_match.group(1)
            
            login_data = {
                'csrf_token': csrf_token,
                'email': 'test@example.com',
                'password': 'testpassword',
                'submit': 'Logg inn'
            }
            
            login_response = client.post('/auth/login', data=login_data, follow_redirects=True)
            print(f"Authentication result: {login_response.status_code}")
            
            # Test profile directly
            print("\n🎯 Testing profile route...")
            profile_response = client.get('/profile')
            print(f"Profile status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                content = profile_response.data.decode()
                
                # Look for debug info
                if 'DEBUG: About to load favorites' in content:
                    print("✅ Debug logging present")
                    
                    # Extract user ID from debug output
                    user_id_match = re.search(r'user ID: (\d+)', content)
                    if user_id_match:
                        detected_user_id = user_id_match.group(1)
                        print(f"Profile detected user ID: {detected_user_id}")
                    
                    # Extract favorites count from debug output
                    favorites_count_match = re.search(r'user_favorites has (\d+) items', content)
                    if favorites_count_match:
                        favorites_count = favorites_count_match.group(1)
                        print(f"Profile found {favorites_count} favorites")
                    
                    # Check if "no favorites" message appears
                    if 'no favorites' in content.lower() or 'ingen favoritter' in content.lower():
                        print("❌ Profile shows 'no favorites' message")
                    else:
                        print("✅ Profile does not show 'no favorites' message")
                        
                        # Look for stock symbols in the output
                        stock_symbols = re.findall(r'\b[A-Z]{2,5}\b', content)
                        unique_symbols = list(set(stock_symbols))
                        print(f"Found stock symbols: {unique_symbols}")
                
                else:
                    print("❌ Debug logging not found in profile")
                
                # Check template sections
                if 'favoritter' in content.lower():
                    print("✅ Favorites section found in template")
                else:
                    print("❌ Favorites section not found in template")
            
            else:
                print(f"❌ Profile request failed with status {profile_response.status_code}")
    
    return True

if __name__ == '__main__':
    test_simplified_favorites()
