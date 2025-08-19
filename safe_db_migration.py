#!/usr/bin/env python3
"""
Database migration to add missing columns - works both locally and in production
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from sqlalchemy import text

def add_missing_columns_safe():
    """Add missing columns using Flask app context"""
    app = create_app()
    
    with app.app_context():
        try:
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
                    # Check if column exists
                    result = db.session.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name='users' AND column_name=:column_name
                    """), {'column_name': column_name})
                    
                    if not result.fetchone():
                        # Add the column
                        db.session.execute(text(f"""
                            ALTER TABLE users 
                            ADD COLUMN {column_name} {column_def}
                        """))
                        print(f"✓ Added column: {column_name}")
                    else:
                        print(f"✓ Column already exists: {column_name}")
                        
                except Exception as e:
                    print(f"❌ Error adding column {column_name}: {e}")
                    continue
            
            # Commit all changes
            db.session.commit()
            print("✅ All database columns updated successfully!")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_missing_columns_safe()
