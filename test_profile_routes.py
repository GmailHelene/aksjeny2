import os
import sys
import logging
from flask import Flask, url_for
from app import create_app, db
from app.models import User
from flask_login import login_user, current_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_profile_route():
    """
    Test the profile route redirect to identify issues
    """
    # Create an app instance
    app = create_app('testing')
    
    # Create an application context
    with app.app_context():
        # Check if the profile blueprint is registered
        logger.info("Checking registered blueprints:")
        for blueprint_name in app.blueprints:
            logger.info(f"  - {blueprint_name}")

        # Check the URL map
        logger.info("Checking URL map for profile routes:")
        for rule in app.url_map.iter_rules():
            if 'profile' in rule.endpoint or 'profile' in str(rule):
                logger.info(f"  - {rule.endpoint} -> {rule}")
        
        # Try to generate URLs for profile routes
        try:
            profile_url = url_for('profile.profile_page')
            logger.info(f"URL for profile.profile_page: {profile_url}")
        except Exception as e:
            logger.error(f"Error generating URL for profile.profile_page: {e}")
        
        try:
            main_profile_url = url_for('main.profile')
            logger.info(f"URL for main.profile: {main_profile_url}")
        except Exception as e:
            logger.error(f"Error generating URL for main.profile: {e}")

if __name__ == "__main__":
    test_profile_route()
