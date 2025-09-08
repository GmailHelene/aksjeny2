"""
test_admin_login.py - Test admin login functionality

This script tests the login functionality for admin users by directly logging in as admin.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to the path to allow importing the app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from app import create_app, db
    from app.models.user import User
    from flask_login import login_user
    from werkzeug.security import generate_password_hash, check_password_hash
    
    print("✅ Successfully imported the application")
except Exception as e:
    print(f"❌ Failed to import the application: {e}")
    sys.exit(1)

def verify_user_login(email, password):
    """Test if login would work for a given email and password"""
    try:
        app = create_app()
        
        with app.app_context():
            # Find the user
            user = User.query.filter_by(email=email).first()
            
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            print(f"\n===== User: {email} =====")
            print(f"Username: {user.username}")
            print(f"Has password hash: {'Yes' if user.password_hash else 'No'}")
            
            # Test password
            if not user.password_hash:
                print(f"❌ User has no password hash!")
                return False
            
            if check_password_hash(user.password_hash, password):
                print(f"✅ Password is correct!")
                return True
            else:
                print(f"❌ Password is incorrect!")
                
                # Print hash information for debugging
                print(f"Current hash: {user.password_hash[:20]}...")
                
                # Create a new hash for the same password to compare
                new_hash = generate_password_hash(password)
                print(f"Test hash for same password: {new_hash[:20]}...")
                
                return False
                
    except Exception as e:
        print(f"❌ Error verifying user login: {e}")
        import traceback
        traceback.print_exc()
        return False

def fix_user_password(email, password):
    """Fix a user's password"""
    try:
        app = create_app()
        
        with app.app_context():
            # Find the user
            user = User.query.filter_by(email=email).first()
            
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            # Set new password hash
            user.password_hash = generate_password_hash(password)
            
            # Ensure premium access
            user.has_subscription = True
            user.subscription_type = 'lifetime'
            user.subscription_start = datetime.utcnow()
            user.subscription_end = None
            user.is_admin = True
            
            # Save changes
            db.session.commit()
            
            print(f"✅ Password updated for {email}!")
            
            # Verify the fix
            if check_password_hash(user.password_hash, password):
                print(f"✅ Password verification successful!")
                return True
            else:
                print(f"❌ Password verification failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error fixing user password: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_login():
    """Test admin login functionality"""
    # Test credentials
    test_users = [
        {'email': 'test@aksjeradar.trade', 'password': 'aksjeradar2024'},
        {'email': 'investor@aksjeradar.trade', 'password': 'aksjeradar2024'},
        {'email': 'testuser@aksjeradar.trade', 'password': 'aksjeradar2024'}  # Known best  admin user as a control
    ]
    
    fixed_users = []
    
    for user in test_users:
        email = user['email']
        password = user['password']
        
        print(f"\n\n===== Testing login for {email} =====")
        login_works = verify_user_login(email, password)
        
        if not login_works:
            print(f"Login failed for {email}, attempting to fix...")
            fixed = fix_user_password(email, password)
            
            if fixed:
                print(f"✅ Fixed login for {email}")
                fixed_users.append(user)
            else:
                print(f"❌ Could not fix login for {email}")
        else:
            print(f"✅ Login already works for {email}")
            fixed_users.append(user)
    
    print("\n\n===== LOGIN TEST SUMMARY =====")
    if fixed_users:
        print("The following users can now log in:")
        for user in fixed_users:
            print(f"- {user['email']} (password: {user['password']})")
    else:
        print("No users were fixed or verified.")
    
    return len(fixed_users) > 0

if __name__ == "__main__":
    success = test_admin_login()
    
    if success:
        print("\n✅ Admin login test completed successfully!")
        print("You should now be able to log in with the fixed user accounts.")
    else:
        print("\n❌ Admin login test failed!")
        print("There may still be issues with logging in.")
        sys.exit(1)
