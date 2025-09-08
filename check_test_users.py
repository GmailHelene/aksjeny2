"""
check_test_users.py - Verifies that the test users exist in the database and have proper credentials
"""

import sys
import os

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

def check_test_users():
    """Check if the test users exist and have correct password hashes"""
    try:
        app = create_app()
        
        with app.app_context():
            # Test emails to check
            test_emails = ['test@aksjeradar.trade', 'investor@aksjeradar.trade']
            test_password = 'aksjeradar2024'
            
            for email in test_emails:
                user = User.query.filter_by(email=email).first()
                
                if user:
                    print(f"\n===== User: {email} =====")
                    print(f"Username: {user.username}")
                    print(f"Has password hash: {'Yes' if user.password_hash else 'No'}")
                    
                    # Check if the password works
                    if user.password_hash:
                        if check_password_hash(user.password_hash, test_password):
                            print(f"✅ Password hash is valid for the expected password")
                        else:
                            print(f"❌ Password hash is NOT valid for the expected password")
                            
                            # Fix the password
                            print(f"🔧 Updating password hash...")
                            user.set_password(test_password)
                            db.session.commit()
                            
                            # Verify the fix
                            if check_password_hash(user.password_hash, test_password):
                                print(f"✅ Password hash fixed successfully")
                            else:
                                print(f"❌ Failed to fix password hash")
                    else:
                        print(f"❌ User has no password hash! Setting one now...")
                        user.set_password(test_password)
                        db.session.commit()
                        print(f"✅ Password hash set")
                        
                else:
                    print(f"\n❌ User with email {email} does not exist in the database!")
    
    except Exception as e:
        print(f"❌ Error checking test users: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_test_users()
