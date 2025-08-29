#!/usr/bin/env python3
"""
Test script to debug SQLAlchemy session issues with favorites
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.user import User
from app.extensions import db

def test_sqlalchemy_session():
    print("🔍 Testing SQLAlchemy session and favorites query...")
    
    app = create_app('development')
    
    with app.app_context():
        # Check database connection
        print("\n📊 Database connection test:")
        try:
            # Test basic query
            user_count = User.query.count()
            print(f"Total users in database: {user_count}")
            
            # Get our test user
            test_user = User.query.filter_by(email='test@example.com').first()
            print(f"Test user: ID={test_user.id}, Email={test_user.email}")
            
            # Test direct SQL query first
            print("\n🔍 Testing direct SQL query:")
            result = db.session.execute(db.text("SELECT * FROM favorites WHERE user_id = 5"))
            rows = result.fetchall()
            print(f"Direct SQL query found {len(rows)} favorites for user ID 5:")
            for row in rows:
                print(f"  - Row: {dict(row._mapping)}")
            
            # Test SQLAlchemy query without import issues
            print("\n🔍 Testing SQLAlchemy query with fresh import:")
            from app.models.favorites import Favorites
            print(f"Favorites model: {Favorites}")
            print(f"Favorites table name: {Favorites.__tablename__}")
            
            # Test the exact same query as in profile route
            favorites = Favorites.query.filter_by(user_id=5).all()
            print(f"SQLAlchemy query found {len(favorites)} favorites for user ID 5:")
            for fav in favorites:
                print(f"  - Favorite: {fav.symbol}, Name: {fav.name}, User ID: {fav.user_id}")
            
            # Test with different query approaches
            print("\n🔍 Testing alternative query approaches:")
            
            # Using filter instead of filter_by
            favorites_alt1 = Favorites.query.filter(Favorites.user_id == 5).all()
            print(f"Using filter(): found {len(favorites_alt1)} favorites")
            
            # Using get by joining
            user_with_favorites = User.query.filter_by(id=5).first()
            if user_with_favorites:
                favorites_alt2 = user_with_favorites.favorites.all()
                print(f"Using user.favorites: found {len(favorites_alt2)} favorites")
            else:
                print("User with ID 5 not found")
            
            # Test session commit/flush
            print("\n🔍 Testing session state:")
            print(f"Session dirty objects: {len(db.session.dirty)}")
            print(f"Session new objects: {len(db.session.new)}")
            print(f"Session deleted objects: {len(db.session.deleted)}")
            
            # Force commit and re-query
            db.session.commit()
            favorites_after_commit = Favorites.query.filter_by(user_id=5).all()
            print(f"After commit: found {len(favorites_after_commit)} favorites")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            import traceback
            traceback.print_exc()
    
    return True

if __name__ == '__main__':
    test_sqlalchemy_session()
