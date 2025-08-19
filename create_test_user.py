#!/usr/bin/env python3
"""
Create test user for testing price alerts functionality
"""

import os
import sys
from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_user():
    """Create a test user for testing purposes"""
    logger.info("Creating test user for price alerts testing...")
    
    # Check if test user already exists
    test_user = User.query.filter_by(email='test@example.com').first()
    if test_user:
        logger.info("✅ Test user already exists")
        return test_user
    
    # Create new test user
    try:
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123'),
            email_verified=True
        )
        
        db.session.add(test_user)
        db.session.commit()
        
        logger.info("✅ Test user created successfully")
        logger.info(f"   Email: test@example.com")
        logger.info(f"   Password: password123")
        logger.info(f"   User ID: {test_user.id}")
        
        return test_user
        
    except Exception as e:
        logger.error(f"❌ Failed to create test user: {e}")
        db.session.rollback()
        return None

def main():
    """Main function"""
    logger.info("🔧 Creating Test User for Price Alerts")
    logger.info("=" * 50)
    
    app = create_app('development')
    
    with app.app_context():
        try:
            user = create_test_user()
            if user:
                logger.info("\n🎉 Test user setup completed!")
                logger.info("You can now login and test price alerts at:")
                logger.info("  Login: http://localhost:5002/login")
                logger.info("  Email: test@example.com")
                logger.info("  Password: password123")
                logger.info("  Price Alerts: http://localhost:5002/price-alerts/")
                return 0
            else:
                logger.error("❌ Failed to create test user")
                return 1
                
        except Exception as e:
            logger.error(f"❌ Error during test user creation: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
