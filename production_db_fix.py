#!/usr/bin/env python3
"""
Quick database column addition for production
"""
import os
import sys
import psycopg2
from urllib.parse import urlparse

def add_missing_columns_production():
    """Add missing columns directly to production database"""
    
    # Get database URL from environment (Railway sets this)
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("No DATABASE_URL found in environment")
        return
    
    # Parse the database URL
    parsed_url = urlparse(database_url)
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=parsed_url.hostname,
            port=parsed_url.port,
            database=parsed_url.path[1:],  # Remove leading slash
            user=parsed_url.username,
            password=parsed_url.password
        )
        
        cursor = conn.cursor()
        
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
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='users' AND column_name=%s
                """, (column_name,))
                
                if not cursor.fetchone():
                    # Add the column
                    cursor.execute(f"""
                        ALTER TABLE users 
                        ADD COLUMN {column_name} {column_def}
                    """)
                    print(f"✓ Added column: {column_name}")
                else:
                    print(f"✓ Column already exists: {column_name}")
                    
            except Exception as e:
                print(f"❌ Error adding column {column_name}: {e}")
                continue
        
        # Commit all changes
        conn.commit()
        print("✅ All database columns updated successfully!")
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    add_missing_columns_production()
