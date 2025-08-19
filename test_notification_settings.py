"""Script to test notification settings functionality"""
from app import create_app
from app.models.user import User
from app.extensions import db

def test_notifications():
    """Test notification settings"""
    app = create_app()
    with app.app_context():
        # Find a user
        user = User.query.first()
        if not user:
            print("No users found")
            return
        
        # Get current settings
        print("Current settings:", user.get_notification_settings())
        
        # Try updating settings
        new_settings = {
            'email_enabled': True,
            'push_enabled': False,
            'inapp_enabled': True,
            'email_price_alerts': True,
            'email_market_news': False
        }
        
        result = user.update_notification_settings(new_settings)
        print(f"Update result: {result}")
        
        # Get updated settings
        updated = user.get_notification_settings()
        print("Updated settings:", updated)
        
        # Verify specific values
        print(f"email_enabled = {updated.get('email_enabled')}")
        print(f"push_enabled = {updated.get('push_enabled')}")
        print(f"email_price_alerts = {updated.get('email_price_alerts')}")

if __name__ == "__main__":
    test_notifications()
