#!/usr/bin/env python3
"""Debug script for testing favorites system"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import DevelopmentConfig
from app.extensions import db
from app.models.favorites import Favorites
from app.models.users import User

def debug_favorites():
    """Debug favorites system"""
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    
    with app.app_context():
        print("=== Favorites System Debug ===")
        
        # Check if favorites table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Database tables: {tables}")
        print(f"Favorites table exists: {'favorites' in tables}")
        
        # Create tables if they don't exist
        if 'favorites' not in tables:
            print("Creating favorites table...")
            try:
                db.create_all()
                print("✅ Tables created successfully")
            except Exception as e:
                print(f"❌ Error creating tables: {e}")
                return
        
        # Test favorites functionality
        try:
            # Count existing favorites
            count = Favorites.query.count()
            print(f"Current favorites count: {count}")
            
            # Find a test user (create one if needed)
            test_user = User.query.filter_by(email='test@test.com').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@test.com',
                    subscription_type='basic'
                )
                test_user.set_password('testpass')
                db.session.add(test_user)
                db.session.commit()
                print("✅ Created test user")
            
            print(f"Test user ID: {test_user.id}")
            
            # Test adding a favorite
            is_fav_before = Favorites.is_favorite(test_user.id, 'AAPL')
            print(f"AAPL is favorite before: {is_fav_before}")
            
            if not is_fav_before:
                fav = Favorites.add_favorite(test_user.id, 'AAPL', 'Apple Inc', 'NASDAQ')
                print(f"✅ Added AAPL as favorite: {fav}")
            
            is_fav_after = Favorites.is_favorite(test_user.id, 'AAPL')
            print(f"AAPL is favorite after: {is_fav_after}")
            
            # Get user favorites
            user_favs = Favorites.get_user_favorites(test_user.id)
            print(f"User favorites: {[f.symbol for f in user_favs]}")
            
            print("=== Favorites system working correctly! ===")
            
        except Exception as e:
            print(f"❌ Error testing favorites: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    debug_favorites()
