#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.abspath('.'))

from app import create_app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_test_users():
    """Create test users for authentication testing"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if test user already exists
            existing_user = User.query.filter_by(email='test@example.com').first()
            if existing_user:
                print("✅ Test user already exists")
                return True
            
            # Create test user
            test_user = User(
                email='test@example.com',
                username='testuser',
                password_hash=generate_password_hash('testpass123'),
                is_active=True,
                is_premium=True,  # Give premium access for testing
                demo_mode=False
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Test user created successfully")
            print("   Email: test@example.com")
            print("   Password: testpass123")
            return True
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = create_test_users()
    sys.exit(0 if success else 1)
