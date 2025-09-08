#!/usr/bin/env python3
"""
Test the profile route directly with proper authentication context
"""

from app import create_app
from app.models.user import User
from flask import url_for
from flask_login import login_user
import logging

# Set up logging to see our debug messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

with app.test_client() as client:
    with app.app_context():
        # Get the test user
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            logger.error("Test user not found!")
            exit(1)
        
        logger.info(f"Found test user: {test_user.username} (ID: {test_user.id})")
        
        # Login the test user
        with client.session_transaction() as sess:
            sess['_user_id'] = str(test_user.id)
            sess['_fresh'] = True
        
        # Make request to profile page
        logger.info("Making request to profile page...")
        
        # Test both /profile and /profile/ to ensure both work
        for path in ['/profile', '/profile/']:
            response = client.get(path)
            
            logger.info(f"Request to {path} - Response status: {response.status_code}")
            if response.status_code == 302:
                logger.info(f"Redirected to: {response.location}")
            
            # Check if the response contains our favorites
            if response.status_code == 200:
                content = response.get_data(as_text=True)
                
                # Check for the specific template content
                if 'Du har ingen favoritter ennå' in content:
                    logger.info("Page shows 'no favorites' message")
                elif 'AAPL' in content or 'TSLA' in content:
                    logger.info("✅ Page shows favorites content")
                else:
                    logger.info("Page loaded but did not find favorites content")
                    
                if 'Brukerinformasjon' in content:
                    logger.info("✅ Profile page content loaded correctly")
                else:
                    logger.error("❌ Profile page content missing!")
            else:
                logger.error(f"❌ Failed to load {path}: Status code {response.status_code}")
                logger.warning("⚠️  Cannot determine favorites status from page content")
                
            # Look for any error messages in the page
            if 'favorites_failed' in content:
                logger.error("❌ Found 'favorites_failed' error in page")
            
            # Save the response for inspection
            with open('/tmp/profile_response.html', 'w') as f:
                f.write(content)
            logger.info("Saved full response to /tmp/profile_response.html")
        
        else:
            logger.error(f"Failed to get profile page: {response.status_code}")
