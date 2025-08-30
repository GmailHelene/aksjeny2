#!/usr/bin/env python3
"""
Test script to debug and fix the favorites display issue
"""
import sys
sys.path.append('/workspaces/aksjeny2')

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.favorites import Favorites
from flask import current_app
import traceback

def test_favorites():
    app = create_app()
    
    with app.app_context():
        try:
            print("=== FAVORITES DEBUG TEST ===")
            
            # Check if favorites table exists
            print("\n1. Checking favorites table...")
            try:
                result = db.session.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='favorites'"))
                table_exists = result.fetchone()
                print(f"Favorites table exists: {table_exists is not None}")
                
                if table_exists:
                    # Get table schema
                    result = db.session.execute(db.text("PRAGMA table_info(favorites)"))
                    columns = result.fetchall()
                    print("Favorites table columns:")
                    for col in columns:
                        print(f"  - {col[1]} ({col[2]})")
                else:
                    print("Creating favorites table...")
                    db.create_all()
                    
            except Exception as e:
                print(f"Error checking table: {e}")
                
            # Check existing favorites
            print("\n2. Checking existing favorites...")
            all_favorites = Favorites.query.all()
            print(f"Total favorites in database: {len(all_favorites)}")
            
            for fav in all_favorites:
                print(f"  - User {fav.user_id}: {fav.symbol} ({fav.name})")
                
            # Check users
            print("\n3. Checking users...")
            all_users = User.query.all()
            print(f"Total users: {len(all_users)}")
            
            if len(all_users) > 0:
                test_user = all_users[0]
                print(f"Test user ID: {test_user.id}, Username: {test_user.username}")
                
                # Check favorites for this user
                user_favorites = Favorites.query.filter_by(user_id=test_user.id).all()
                print(f"Favorites for user {test_user.id}: {len(user_favorites)}")
                
                # If no favorites, create one for testing
                if len(user_favorites) == 0:
                    print("\n4. Creating test favorite...")
                    test_favorite = Favorites(
                        user_id=test_user.id,
                        symbol='AAPL',
                        name='Apple Inc.',
                        exchange='NASDAQ'
                    )
                    db.session.add(test_favorite)
                    db.session.commit()
                    print("Test favorite created successfully!")
                    
                    # Verify it was created
                    user_favorites = Favorites.query.filter_by(user_id=test_user.id).all()
                    print(f"After creation - favorites for user {test_user.id}: {len(user_favorites)}")
                    
                # Test the exact query from profile route
                print("\n5. Testing profile route logic...")
                user_id = test_user.id
                db.session.commit()  # Ensure any pending transactions are committed
                favorites = Favorites.query.filter_by(user_id=user_id).all()
                print(f"Profile route query found {len(favorites)} favorites for user {user_id}")
                
                # Build user_favorites list like in profile route
                user_favorites_list = []
                for fav in favorites:
                    favorite_info = {
                        'symbol': fav.symbol,
                        'name': fav.name,
                        'exchange': fav.exchange,
                        'created_at': fav.created_at
                    }
                    user_favorites_list.append(favorite_info)
                    
                print(f"Built user_favorites list: {user_favorites_list}")
                
                # Test template condition
                has_favorites = user_favorites_list and len(user_favorites_list) > 0
                print(f"Template condition (user_favorites and user_favorites|length > 0): {has_favorites}")
                
                if has_favorites:
                    print("✅ Should show favorites in template")
                else:
                    print("❌ Will show 'no favorites' message in template")
            else:
                print("No users found! Creating a test user...")
                from werkzeug.security import generate_password_hash
                test_user = User(
                    username='testuser',
                    email='test@test.com',
                    password_hash=generate_password_hash('password123')
                )
                db.session.add(test_user)
                db.session.commit()
                print(f"Created test user with ID: {test_user.id}")
                
        except Exception as e:
            print(f"Error in test: {e}")
            print(f"Traceback: {traceback.format_exc()}")

if __name__ == '__main__':
    test_favorites()
