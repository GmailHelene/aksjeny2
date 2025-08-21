"""Test script to add notification columns"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from sqlalchemy import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_notification_columns():
    """Add missing notification columns to users table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check which columns exist
            result = db.session.execute(text("PRAGMA table_info(users)"))
            existing_columns = [row[1] for row in result.fetchall()]
            print(f"Existing columns: {existing_columns}")
            
            # Columns we need
            needed_columns = {
                'email_notifications_enabled': 'BOOLEAN DEFAULT 1',
                'price_alerts_enabled': 'BOOLEAN DEFAULT 1', 
                'market_news_enabled': 'BOOLEAN DEFAULT 1',
                'portfolio_updates_enabled': 'BOOLEAN DEFAULT 1',
                'ai_insights_enabled': 'BOOLEAN DEFAULT 1',
                'weekly_reports_enabled': 'BOOLEAN DEFAULT 1'
            }
            
            # Add missing columns
            for column_name, column_def in needed_columns.items():
                if column_name not in existing_columns:
                    try:
                        sql = f"ALTER TABLE users ADD COLUMN {column_name} {column_def}"
                        print(f"Adding column: {sql}")
                        db.session.execute(text(sql))
                        db.session.commit()
                        print(f"✓ Added column {column_name}")
                    except Exception as e:
                        print(f"✗ Error adding column {column_name}: {e}")
                        db.session.rollback()
                else:
                    print(f"✓ Column {column_name} already exists")
            
            print("Notification columns setup complete!")
            return True
            
        except Exception as e:
            print(f"Error adding notification columns: {e}")
            return False

if __name__ == "__main__":
    add_notification_columns()
