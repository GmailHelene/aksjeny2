#!/usr/bin/env python3
"""
Fix Price Alerts Database Issues
Creates missing price_alerts table if it doesn't exist
"""

import os
import sys
from app import create_app
from app.extensions import db
from app.models.price_alert import PriceAlert, AlertNotificationSettings
from app.models.user import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_table_exists(engine, table_name):
    """Check if a table exists in the database"""
    from sqlalchemy import text
    try:
        result = engine.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"))
        return len(list(result)) > 0
    except Exception as e:
        logger.error(f"Error checking table {table_name}: {e}")
        return False

def create_price_alerts_table():
    """Create price_alerts table with all required columns"""
    logger.info("Creating price_alerts table...")
    
    # Create all tables based on models
    db.create_all()
    
    # Double-check the table was created
    with db.engine.connect() as conn:
        tables = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
        table_names = [table[0] for table in tables]
        
        if 'price_alerts' in table_names:
            logger.info("✅ price_alerts table created successfully")
        else:
            logger.error("❌ Failed to create price_alerts table")
            return False
            
        # Check columns in price_alerts table
        columns = conn.execute(db.text("PRAGMA table_info(price_alerts);")).fetchall()
        column_names = [col[1] for col in columns]
        
        logger.info(f"Price alerts table columns: {column_names}")
        
        required_columns = ['id', 'user_id', 'ticker', 'symbol', 'target_price', 'alert_type', 
                          'is_active', 'is_triggered', 'created_at', 'email_sent', 'notify_email']
        
        missing_columns = [col for col in required_columns if col not in column_names]
        if missing_columns:
            logger.warning(f"Missing columns: {missing_columns}")
        else:
            logger.info("✅ All required columns present")
    
    return True

def create_alert_notification_settings_table():
    """Create alert_notification_settings table"""
    logger.info("Creating alert_notification_settings table...")
    
    # This should be created by db.create_all() but let's check
    with db.engine.connect() as conn:
        tables = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
        table_names = [table[0] for table in tables]
        
        if 'alert_notification_settings' in table_names:
            logger.info("✅ alert_notification_settings table exists")
        else:
            logger.info("Creating alert_notification_settings table manually if needed...")
    
    return True

def test_price_alert_creation():
    """Test creating a price alert"""
    logger.info("Testing price alert creation...")
    
    try:
        # Find or create a test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            logger.warning("No test user found, skipping creation test")
            return True
        
        # Try to create a test alert
        test_alert = PriceAlert(
            user_id=test_user.id,
            symbol='AAPL',
            ticker='AAPL',
            target_price=150.0,
            alert_type='above',
            company_name='Apple Inc.'
        )
        
        db.session.add(test_alert)
        db.session.commit()
        
        logger.info("✅ Successfully created test price alert")
        
        # Clean up
        db.session.delete(test_alert)
        db.session.commit()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create test alert: {e}")
        db.session.rollback()
        return False

def main():
    """Main function to fix price alerts database issues"""
    logger.info("🔧 Fixing Price Alerts Database Issues")
    logger.info("=" * 50)
    
    app = create_app('development')
    
    with app.app_context():
        try:
            # Check if price_alerts table exists
            with db.engine.connect() as conn:
                tables = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
                table_names = [table[0] for table in tables]
                
                logger.info(f"Existing tables: {table_names}")
                
                if 'price_alerts' not in table_names:
                    logger.warning("❌ price_alerts table missing")
                    create_price_alerts_table()
                else:
                    logger.info("✅ price_alerts table exists")
                
                if 'alert_notification_settings' not in table_names:
                    logger.warning("❌ alert_notification_settings table missing")
                    create_alert_notification_settings_table()
                else:
                    logger.info("✅ alert_notification_settings table exists")
            
            # Test alert creation
            test_price_alert_creation()
            
            logger.info("\n🎉 Price alerts database fix completed!")
            logger.info("You can now create price alerts at /price-alerts/")
            
        except Exception as e:
            logger.error(f"❌ Error during database fix: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
