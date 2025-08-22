#!/usr/bin/env python3
"""
Initialize database tables for aksjeradar.trade
This script creates all missing database tables including UserStats
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    try:
        print("🔧 Initializing database tables...")
        
        # Import after setting path
        from app import create_app
        from app.models import db
        
        # Create app and context
        app = create_app()
        
        with app.app_context():
            print("📋 Creating all database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Test if UserStats table was created
            from app.models.achievements import UserStats
            from app.models.user import User
            
            print("🔍 Verifying tables...")
            
            # Check if tables exist
            tables = db.engine.table_names()
            print(f"📊 Available tables: {', '.join(tables)}")
            
            if 'user_stats' in tables:
                print("✅ UserStats table exists")
            else:
                print("❌ UserStats table missing")
                
            if 'users' in tables:
                print("✅ Users table exists")
            else:
                print("❌ Users table missing")
                
            print("🎉 Database initialization complete!")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_database()
