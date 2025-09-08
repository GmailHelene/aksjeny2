import os
import sys
import logging
from flask import Flask, url_for
from flask_migrate import Migrate

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def create_minimal_app():
    """Create a minimal Flask app for testing"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Import blueprint here to avoid circular import
    from app.routes.profile import profile
    from app.routes.main import main
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(profile, url_prefix='/profile')
    
    return app

def test_profile_route():
    """Test the profile route redirection to identify issues"""
    try:
        # Create a minimal app
        app = create_minimal_app()
        
        # Check if the profile blueprint is registered
        print("Registered blueprints:")
        for blueprint_name in app.blueprints:
            print(f"  - {blueprint_name}")

        # Check the URL map
        print("\nURL map for profile routes:")
        for rule in app.url_map.iter_rules():
            if 'profile' in rule.endpoint or 'profile' in str(rule):
                print(f"  - {rule.endpoint} -> {rule}")
        
        # Try to generate URLs for profile routes
        with app.test_request_context():
            try:
                profile_url = url_for('profile.profile_page')
                print(f"\nURL for profile.profile_page: {profile_url}")
            except Exception as e:
                print(f"\nError generating URL for profile.profile_page: {e}")
            
            try:
                main_profile_url = url_for('main.profile')
                print(f"URL for main.profile: {main_profile_url}")
            except Exception as e:
                print(f"Error generating URL for main.profile: {e}")
            
            # Check the issue with redirecting
            print("\nSimulating redirect from main.profile to profile.profile_page...")
            try:
                # This mimics what happens in the route
                redirect_url = url_for('profile.profile_page')
                print(f"Redirect URL: {redirect_url}")
                print("Redirect appears to work correctly in test environment")
            except Exception as e:
                print(f"Error during redirect simulation: {e}")
                print("This is likely the source of the problem")
    
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    print("Testing profile route configuration...")
    test_profile_route()
