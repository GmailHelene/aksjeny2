"""Simple test to verify notification settings route works"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from flask import url_for
import json

def test_notification_settings():
    """Test the notification settings route"""
    app = create_app()
    
    with app.app_context():
        with app.test_client() as client:
            # Test accessing the route (should require login)
            response = client.post('/update-notification-settings', 
                                 json={'setting': 'emailNotifications', 'enabled': True})
            
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")
            
            if response.status_code == 302:
                print("✓ Route exists and redirects (login required)")
            elif response.status_code == 401:
                print("✓ Route exists and requires authentication")
            else:
                print(f"Route response: {response.status_code}")
                
if __name__ == "__main__":
    test_notification_settings()
