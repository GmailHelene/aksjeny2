#!/usr/bin/env python3
"""
Add missing email_notifications column to users table
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from sqlalchemy import text

def add_missing_columns():
    """Add missing columns to users table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if email_notifications column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='email_notifications'
            """))
            
            if not result.fetchone():
                print("Adding email_notifications column...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN email_notifications BOOLEAN DEFAULT TRUE
                """))
                print("✓ email_notifications column added")
            else:
                print("✓ email_notifications column already exists")
                
            # Check if price_alerts column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='price_alerts'
            """))
            
            if not result.fetchone():
                print("Adding price_alerts column...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN price_alerts BOOLEAN DEFAULT TRUE
                """))
                print("✓ price_alerts column added")
            else:
                print("✓ price_alerts column already exists")
                
            # Check if market_news column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='market_news'
            """))
            
            if not result.fetchone():
                print("Adding market_news column...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN market_news BOOLEAN DEFAULT TRUE
                """))
                print("✓ market_news column added")
            else:
                print("✓ market_news column already exists")
                
            db.session.commit()
            print("✓ All missing columns added successfully!")
            
        except Exception as e:
            print(f"Error adding columns: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_missing_columns()
