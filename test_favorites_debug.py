#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.user import User
from app.models.favorites import Favorites
from flask_login import login_user

def test_favorites():
    app = create_app()
    
    with app.app_context():
        print("=== Testing Favorites Functionality ===")
        
        # Get a test user
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            print("❌ No test user found")
            return
            
        print(f"✅ Found user: {user.email} (ID: {user.id})")
        
        # Check current favorites
        existing_favs = Favorites.get_user_favorites(user.id)
        print(f"📋 Current favorites count: {len(existing_favs)}")
        
        for fav in existing_favs:
            print(f"  - {fav.symbol} ({fav.name or 'No name'}) - Exchange: {fav.exchange or 'No exchange'}")
        
        # Test adding a favorite
        test_symbol = "AAPL"
        existing_fav = Favorites.query.filter_by(user_id=user.id, symbol=test_symbol).first()
        if existing_fav:
            print(f"⚠️ {test_symbol} already exists as favorite")
        else:
            success = Favorites.add_favorite(user.id, test_symbol, "Apple Inc.", "NASDAQ")
            if success:
                print(f"✅ Successfully added {test_symbol} to favorites")
            else:
                print(f"❌ Failed to add {test_symbol} to favorites")
        
        # Check favorites again
        final_favs = Favorites.get_user_favorites(user.id)
        print(f"📋 Final favorites count: {len(final_favs)}")
        
        for fav in final_favs:
            print(f"  - {fav.symbol} ({fav.name or 'No name'}) - Exchange: {fav.exchange or 'No exchange'}")

if __name__ == "__main__":
    test_favorites()
