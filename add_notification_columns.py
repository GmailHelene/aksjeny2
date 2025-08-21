"""Add missing notification columns to users table"""
from app.extensions import db
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def add_notification_columns():
    """Add missing notification columns to users table"""
    try:
        # Check which columns exist
        result = db.session.execute(text("PRAGMA table_info(users)"))
        existing_columns = [row[1] for row in result.fetchall()]
        
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
                    db.session.execute(text(sql))
                    db.session.commit()
                    logger.info(f"Added column {column_name} to users table")
                except Exception as e:
                    logger.error(f"Error adding column {column_name}: {e}")
                    db.session.rollback()
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding notification columns: {e}")
        return False

if __name__ == "__main__":
    add_notification_columns()
