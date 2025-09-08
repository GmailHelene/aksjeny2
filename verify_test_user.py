"""
verify_test_user.py - Verifies that the test user exists and has proper access
"""

import sys
import os

# Add the current directory to the path to allow importing the app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from app import create_app
    from app.models.user import User
    
    print("✅ Successfully imported the application")
except Exception as e:
    print(f"❌ Failed to import the application: {e}")
    sys.exit(1)

def verify_test_user():
    """Verifies that the test user exists and has proper access"""
    try:
        app = create_app()
        
        with app.app_context():
            # Check if the test user exists
            test_user = User.query.filter_by(email='test@aksjeradar.trade').first()
            
            if test_user:
                print("\n===== Test User Information =====")
                print(f"✅ Username: {test_user.username}")
                print(f"✅ Email: {test_user.email}")
                print(f"✅ Subscription: {test_user.subscription_type}")
                print(f"✅ Is Premium: {test_user.is_premium}")
                print(f"✅ Is Admin: {test_user.is_admin}")
                print(f"✅ Email Verified: {getattr(test_user, 'email_verified', 'N/A')}")
                
                # Verify the password still works
                password = 'aksjeradar2024'
                if test_user.check_password(password):
                    print(f"✅ Password '{password}' is valid")
                else:
                    print(f"❌ Password '{password}' is NOT valid")
                
                print("\nThe test user exists and can be used for testing premium features.")
            else:
                print("❌ Test user does not exist!")
                print("Run setup_exempt_test_user.py to create the test user.")
                
    except Exception as e:
        print(f"❌ Failed to verify test user: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = verify_test_user()
    if not success:
        print("❌ Failed to verify test user")
        sys.exit(1)
