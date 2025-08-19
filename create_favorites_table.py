#!/usr/bin/env python3
"""Create favorites table if it doesn't exist"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_favorites_table():
    try:
        # Import after adding path
        from app import create_app
        from app.extensions import db
        from app.models.favorites import Favorites
        from config import DevelopmentConfig
        
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            print("Creating favorites table...")
            
            # Create all tables
            db.create_all()
            
            print("✅ Favorites table created successfully!")
            
            # Test the table
            count = Favorites.query.count()
            print(f"Current favorites count: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating favorites table: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_favorites_table()
