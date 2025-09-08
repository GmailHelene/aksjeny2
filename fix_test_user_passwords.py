"""
fix_test_user_passwords.py - Updates the passwords for test users
"""

import sys
import os
from datetime import datetime, timedelta

# Add the current directory to the path to allow importing the app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from app import create_app, db
    from app.models.user import User
    from werkzeug.security import generate_password_hash, check_password_hash
    
    print("✅ Successfully imported the application")
except Exception as e:
    print(f"❌ Failed to import the application: {e}")
    sys.exit(1)

def fix_test_user_passwords():
    """Fix the passwords for test users"""
    try:
        app = create_app()
        
        with app.app_context():
            # Test emails to fix
            test_users = [
                {
                    'email': 'test@aksjeradar.trade',
                    'username': 'testuser',
                    'password': 'aksjeradar2024'
                },
                {
                    'email': 'investor@aksjeradar.trade',
                    'username': 'investor',
                    'password': 'aksjeradar2024'
                }
            ]
            
            fixed_users = []
            
            for user_data in test_users:
                email = user_data['email']
                username = user_data['username']
                password = user_data['password']
                
                # Try to find the user
                user = User.query.filter_by(email=email).first()
                
                if user:
                    print(f"\nUpdating existing user: {email}")
                    # Update username if needed
                    if user.username != username:
                        user.username = username
                        print(f"  - Updated username to {username}")
                else:
                    print(f"\nCreating new user: {email}")
                    user = User(
                        email=email,
                        username=username
                    )
                    db.session.add(user)
                    print(f"  - Added new user with username {username}")
                
                # Always update the password directly with generate_password_hash
                user.password_hash = generate_password_hash(password)
                print(f"  - Updated password hash directly")
                
                # Set premium access
                user.has_subscription = True
                user.subscription_type = 'lifetime'
                user.subscription_start = datetime.utcnow()
                user.subscription_end = None
                user.is_admin = True
                user.trial_used = True
                print(f"  - Set premium access (lifetime subscription)")
                
                # Make sure the user is verified if that attribute exists
                if hasattr(user, 'email_verified'):
                    user.email_verified = True
                    print(f"  - Marked email as verified")
                    
                # Save changes immediately for this user
                db.session.commit()
                print(f"  - Committed changes to database")
                
                # Test password verification
                fresh_user = User.query.filter_by(email=email).first()
                if fresh_user and check_password_hash(fresh_user.password_hash, password):
                    print(f"  ✅ Password verification successful!")
                else:
                    print(f"  ❌ Password verification failed!")
                
                fixed_users.append({
                    'email': email,
                    'username': username,
                    'password': password
                })
            
            print("\n===== TEST USER CREDENTIALS =====")
            for user in fixed_users:
                print(f"\nUser: {user['email']}")
                print(f"Username: {user['username']}")
                print(f"Password: {user['password']}")
            
            print("\n✅ All test user passwords have been fixed")
            print("Please restart the Flask server before trying to login again.")
    
    except Exception as e:
        print(f"❌ Error fixing test user passwords: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = fix_test_user_passwords()
    if success:
        print("\n🎉 Script completed successfully!")
    else:
        print("\n❌ Script failed!")
        sys.exit(1)
