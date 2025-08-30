#!/usr/bin/env python3
"""
Simple script to test and fix the favorites display issue
"""
import sys
import os
sys.path.append('/workspaces/aksjeny2')

# Set Flask app environment
os.environ['FLASK_APP'] = 'app'

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.favorites import Favorites
from werkzeug.security import generate_password_hash
from datetime import datetime

def fix_favorites():
    app = create_app()
    
    with app.app_context():
        print("=== FAVORITES DATABASE FIX ===")
        
        try:
            # 1. Check if favorites table exists and create if needed
            print("1. Checking database structure...")
            db.create_all()
            print("✅ Database tables ensured")
            
            # 2. Check existing data
            all_users = User.query.all()
            all_favorites = Favorites.query.all()
            print(f"📊 Found {len(all_users)} users and {len(all_favorites)} favorites")
            
            # 3. If no test user exists, create one
            test_user = User.query.filter_by(username='testuser').first()
            if not test_user:
                print("2. Creating test user...")
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash=generate_password_hash('password123'),
                    created_at=datetime.utcnow()
                )
                db.session.add(test_user)
                db.session.commit()
                print(f"✅ Created test user with ID: {test_user.id}")
            else:
                print(f"✅ Test user exists with ID: {test_user.id}")
            
            # 4. Check if test user has favorites
            user_favorites = Favorites.query.filter_by(user_id=test_user.id).all()
            print(f"📋 Test user has {len(user_favorites)} favorites")
            
            # 5. If no favorites, create some test favorites
            if len(user_favorites) == 0:
                print("3. Creating test favorites...")
                test_favorites = [
                    Favorites(
                        user_id=test_user.id,
                        symbol='AAPL',
                        name='Apple Inc.',
                        exchange='NASDAQ',
                        created_at=datetime.utcnow()
                    ),
                    Favorites(
                        user_id=test_user.id,
                        symbol='GOOGL',
                        name='Alphabet Inc.',
                        exchange='NASDAQ',
                        created_at=datetime.utcnow()
                    ),
                    Favorites(
                        user_id=test_user.id,
                        symbol='NEL.OL',
                        name='Nel ASA',
                        exchange='Oslo Børs',
                        created_at=datetime.utcnow()
                    )
                ]
                
                for fav in test_favorites:
                    db.session.add(fav)
                
                db.session.commit()
                print(f"✅ Created {len(test_favorites)} test favorites")
                
                # Verify they were created
                user_favorites = Favorites.query.filter_by(user_id=test_user.id).all()
                print(f"✅ Verified: Test user now has {len(user_favorites)} favorites")
            
            # 6. Test the profile route logic simulation
            print("4. Testing profile route logic...")
            user_id = test_user.id
            
            # Simulate the exact query from profile route
            db.session.commit()  # Ensure any pending transactions are committed
            favorites = Favorites.query.filter_by(user_id=user_id).all()
            print(f"📋 Profile query found {len(favorites)} favorites for user {user_id}")
            
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
                print(f"  - {fav.symbol}: {fav.name} ({fav.exchange})")
            
            # Test template condition
            has_favorites = user_favorites_list and len(user_favorites_list) > 0
            print(f"\n5. Template condition result:")
            print(f"   user_favorites: {user_favorites_list is not None}")
            print(f"   length > 0: {len(user_favorites_list) > 0}")
            print(f"   Final condition: {has_favorites}")
            
            if has_favorites:
                print("✅ Template SHOULD show favorites")
            else:
                print("❌ Template WILL show 'no favorites' message")
            
            print(f"\n=== FIX COMPLETE ===")
            print(f"Test user credentials:")
            print(f"Username: testuser")
            print(f"Password: password123")
            print(f"User ID: {test_user.id}")
            print(f"Favorites count: {len(user_favorites_list)}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_favorites()
