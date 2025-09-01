#!/usr/bin/env python3
import sys
sys.path.insert(0, '/workspaces/aksjeny2')

from app import create_app
from app.models.user import User
from flask_login import login_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

with app.test_request_context():
    with app.app_context():
        # Find the first user
        user = User.query.first()
        print(f"First user: {user.id if user else None}")
        
        if user:
            # Try to log in
            login_user(user)
            print(f"Logged in user: {user.username}")
            
            # Import the profile function
            from app.routes.main import profile
            print("Profile function imported successfully")
            
            # Try calling it
            try:
                result = profile()
                print(f"Profile function returned: {result[:100]}...")
            except Exception as e:
                print(f"Error in profile function: {e}")
        else:
            print("No users found in database")
