#!/usr/bin/env python3
"""
Production database migration - runs once at startup
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from sqlalchemy import text

def migrate_database():
    """Add missing columns to production database"""
    print("🔄 Starting database migration...")
    
    app = create_app()
    with app.app_context():
        try:
            # Check if we're using PostgreSQL (production)
            if 'postgresql' not in str(db.engine.url):
                print("⚠️ Not PostgreSQL - skipping migration")
                return
            
            # List of columns to add
            columns_to_add = [
                ('email_notifications', 'BOOLEAN DEFAULT TRUE'),
                ('price_alerts', 'BOOLEAN DEFAULT TRUE'),
                ('market_news', 'BOOLEAN DEFAULT TRUE'),
                ('first_name', 'VARCHAR(50)'),
                ('last_name', 'VARCHAR(50)'),
                ('two_factor_enabled', 'BOOLEAN DEFAULT FALSE'),
                ('two_factor_secret', 'VARCHAR(32)'),
                ('email_verified', 'BOOLEAN DEFAULT TRUE'),
                ('is_locked', 'BOOLEAN DEFAULT FALSE'),
                ('last_login', 'TIMESTAMP'),
                ('login_count', 'INTEGER DEFAULT 0'),
                ('reset_token', 'VARCHAR(100)'),
                ('reset_token_expires', 'TIMESTAMP')
            ]
            
            for column_name, column_def in columns_to_add:
                try:
                    # Try to add the column directly (will fail if exists)
                    db.session.execute(text(f"""
                        ALTER TABLE users 
                        ADD COLUMN {column_name} {column_def}
                    """))
                    print(f"✅ Added column: {column_name}")
                except Exception as e:
                    if "already exists" in str(e) or "duplicate column name" in str(e):
                        print(f"✓ Column already exists: {column_name}")
                    else:
                        print(f"❌ Error with column {column_name}: {e}")
                    continue
            
            db.session.commit()
            print("✅ Database migration completed!")
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_database()
