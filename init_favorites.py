#!/usr/bin/env python3
"""Initialize favorites table if it doesn't exist"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/workspaces/aksjeny')

def init_favorites_table():
    """Initialize the favorites table"""
    try:
        # Import Flask app factory
        from app import create_app
        from app.extensions import db
        from config import DevelopmentConfig
        
        # Create Flask app
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            print("Initializing favorites table...")
            
            # Import the model to ensure it's registered
            from app.models.favorites import Favorites
            
            # Create the table
            db.create_all()
            print("✅ Favorites table created/verified successfully!")
            
            # Test query
            count = Favorites.query.count()
            print(f"Current favorites count: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error initializing favorites table: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    init_favorites_table()
