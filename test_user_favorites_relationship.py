#!/usr/bin/env python3

from app import create_app
from app.models import User, Favorites
from app.extensions import db
from flask_login import login_user, logout_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_profile_with_proper_login():
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            # Find our test user
            user = User.query.filter_by(username='testuser').first()
            if not user:
                logger.error("Test user not found!")
                return
                
            logger.info(f"Found test user: {user.username} (ID: {user.id})")
            
            # Check favorites directly in database
            favorites = Favorites.query.filter_by(user_id=user.id).all()
            logger.info(f"Database favorites count: {len(favorites)}")
            for fav in favorites:
                logger.info(f"  - {fav.symbol}: {fav.name}")
            
            # Test accessing the favorites relationship through the user object
            try:
                user_favorites = user.favorites.all()
                logger.info(f"User.favorites.all() count: {len(user_favorites)}")
                for fav in user_favorites:
                    logger.info(f"  - {fav.symbol}: {fav.name}")
            except Exception as e:
                logger.error(f"Error accessing user.favorites: {e}")
                
            # Test direct relationship
            try:
                # Check if the relationship is working
                logger.info(f"hasattr(user, 'favorites'): {hasattr(user, 'favorites')}")
                if hasattr(user, 'favorites'):
                    logger.info(f"type(user.favorites): {type(user.favorites)}")
                    
            except Exception as e:
                logger.error(f"Error checking user.favorites attribute: {e}")

if __name__ == "__main__":
    test_profile_with_proper_login()
