#!/usr/bin/env python3

import sqlite3
from app import create_app
from app.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_current_user_debug():
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            # Find our test user
            user = User.query.filter_by(username='testuser').first()
            if not user:
                logger.error("Test user not found!")
                return
                
            logger.info(f"Found test user: {user.username} (ID: {user.id})")
            
            # Check favorites in database directly
            conn = sqlite3.connect('/workspaces/aksjeny2/app.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_favorites WHERE user_id = ?", (user.id,))
            favorites = cursor.fetchall()
            logger.info(f"Database favorites for user {user.id}: {favorites}")
            conn.close()
            
            # Check if user has favorites attribute
            logger.info(f"User object has 'favorites' attribute: {hasattr(user, 'favorites')}")
            if hasattr(user, 'favorites'):
                logger.info(f"User favorites count: {len(user.favorites)}")
            
            # Login and test session
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
                
            # Test if current_user is properly loaded
            from flask_login import current_user
            logger.info(f"Current user type: {type(current_user)}")
            logger.info(f"Current user authenticated: {current_user.is_authenticated}")
            if hasattr(current_user, 'id'):
                logger.info(f"Current user ID: {current_user.id}")
                logger.info(f"Current user username: {current_user.username}")
                
                # Check if current_user has favorites
                logger.info(f"Current user has 'favorites' attr: {hasattr(current_user, 'favorites')}")
                if hasattr(current_user, 'favorites'):
                    logger.info(f"Current user favorites count: {len(current_user.favorites)}")
                    for fav in current_user.favorites:
                        logger.info(f"Favorite: {fav.symbol}")
            else:
                logger.error("Current user has no 'id' attribute!")
                
            # Test the profile route
            response = client.get('/profile')
            logger.info(f"Profile response status: {response.status_code}")

if __name__ == "__main__":
    test_current_user_debug()
