#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

def create_test_user():
    app = create_app()
    
    with app.app_context():
        try:
            # Check if user exists
            existing_user = User.query.filter_by(email='test@example.com').first()
            if existing_user:
                print(f"User already exists: {existing_user.email}")
                return existing_user
            
            # Create new user
            user = User(
                email='test@example.com',
                password_hash=generate_password_hash('password123'),
                is_active=True,
                subscription_status='active',
                subscription_type='pro'
            )
            
            db.session.add(user)
            db.session.commit()
            
            print(f"✅ Created test user: {user.email} with ID: {user.id}")
            return user
            
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            db.session.rollback()
            return None

if __name__ == '__main__':
    create_test_user()
