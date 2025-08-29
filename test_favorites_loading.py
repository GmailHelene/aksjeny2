#!/usr/bin/env python3
"""
Test script to debug favorites loading for user profile page
"""

from app import create_app
from app.models.favorites import Favorites
from app.models.user import User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    # Test the favorites loading logic for user ID 1
    user_id = 1
    
    # Get user
    user = User.query.get(user_id)
    if not user:
        logger.error(f"User {user_id} not found")
        exit(1)
    
    logger.info(f"Testing favorites for user: {user.username} (ID: {user.id})")
    
    # Test the exact same logic as in the profile route
    try:
        # Use the Favorites model
        favorites = Favorites.query.filter_by(user_id=user.id).all()
        logger.info(f"Found {len(favorites)} favorites for user {user.id}")
        
        user_favorites = []
        
        for fav in favorites:
            favorite_info = {
                'symbol': fav.symbol,
                'name': fav.name or fav.symbol,
                'exchange': fav.exchange or 'Unknown',
                'created_at': fav.created_at
            }
            user_favorites.append(favorite_info)
            logger.info(f"  - {fav.symbol}: {fav.name or 'No name'}")
            
        logger.info(f"Built user_favorites list with {len(user_favorites)} items")
        
        # Test the template condition
        if user_favorites and len(user_favorites) > 0:
            logger.info("✅ Template condition user_favorites and user_favorites|length > 0 would be TRUE")
        else:
            logger.warning("❌ Template condition user_favorites and user_favorites|length > 0 would be FALSE")
            
        # Show what would be passed to template
        logger.info(f"user_favorites would contain: {len(user_favorites)} items")
        for i, fav in enumerate(user_favorites[:5]):  # Show first 5
            logger.info(f"  [{i}] {fav}")
            
    except Exception as e:
        logger.error(f"Error loading favorites: {e}")
        import traceback
        traceback.print_exc()
