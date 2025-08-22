#!/usr/bin/env python3
"""
Database migration to ensure UserStats table exists
"""

import sys
import os
import traceback

# Set environment variables
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def migrate_database():
    """Create UserStats and other missing tables"""
    try:
        print("🔧 Database Migration - Creating UserStats table...")
        
        from app import create_app
        from app.models import db
        from app.models.achievements import UserStats
        
        app = create_app('development')
        
        with app.app_context():
            # Create all tables
            db.create_all()
            
            # Check if UserStats table exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Available database tables: {len(tables)}")
            
            if 'user_stats' in tables:
                print("✅ UserStats table created/verified successfully")
                
                # Check UserStats columns
                columns = [col['name'] for col in inspector.get_columns('user_stats')]
                print(f"📋 UserStats columns: {', '.join(columns)}")
                
                return True
            else:
                print("❌ UserStats table creation failed")
                return False
                
    except Exception as e:
        print(f"❌ Database migration failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if migrate_database():
        print("\n🎉 Database migration completed successfully!")
        print("The 'table does not exist' errors should now be resolved.")
    else:
        print("\n❌ Database migration failed!")
        print("Manual intervention may be required.")
