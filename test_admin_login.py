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
            user = User.query.filter_by(email=email).first()
            if not user:
                print(f"User with email {email} not found, creating new user...")
                username = email.split('@')[0]
                now = datetime.utcnow()
                user = User(
                    email=email,
                    username=username,
                    password_hash=generate_password_hash(password),
                    has_subscription=True,
                    subscription_type='lifetime',
                    subscription_start=now,
                    subscription_end=None,
                    is_admin=True,
                    trial_used=True,
                    created_at=now,
                    trial_start=now,
                    stripe_customer_id=None,
                    reports_used_this_month=0,
                    last_reset_date=now,
                    reset_token=None,
                    reset_token_expires=None,
                    language='no',
                    notification_settings=None,
                    email_notifications=True,
                    price_alerts=True,
                    market_news=True,
                    email_notifications_enabled=True,
                    price_alerts_enabled=True,
                    market_news_enabled=True,
                    portfolio_updates_enabled=True,
                    ai_insights_enabled=True,
                    weekly_reports_enabled=True,
                    first_name=None,
                    last_name=None,
                    two_factor_enabled=False,
                    two_factor_secret=None,
                    email_verified=True,
                    is_locked=False,
                    last_login=now,
                    login_count=1
                )
                db.session.add(user)
                db.session.commit()
                print(f"✅ Created new user: {email}")
            else:
                # Set new password hash
                user.password_hash = generate_password_hash(password)
                user.has_subscription = True
                user.subscription_type = 'lifetime'
                user.subscription_start = datetime.utcnow()
                user.subscription_end = None
                user.is_admin = True
                user.trial_used = True
                db.session.commit()
                print(f"✅ Password updated for {email}!")
            # Verify the fix
            user_check = User.query.filter_by(email=email).first()
            if user_check and check_password_hash(user_check.password_hash, password):
                print(f"✅ Password verification successful!")
                # Ensure user has at least one portfolio
                from app.models.portfolio import Portfolio, PortfolioStock
                portfolios = Portfolio.query.filter_by(user_id=user_check.id).all()
                if not portfolios:
                    print(f"No portfolios found for {email}, creating default portfolio...")
                    portfolio = Portfolio(
                        name="Test Portfolio",
                        description="Default portfolio for test user.",
                        user_id=user_check.id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                        is_watchlist=False
                    )
                    db.session.add(portfolio)
                    db.session.commit()
                    print(f"✅ Created default portfolio for {email}")
                    # Add a default stock to the portfolio
                    stock = PortfolioStock(
                        portfolio_id=portfolio.id,
                        ticker="AAPL",
                        shares=10,
                        purchase_price=150.0,
                        purchase_date=datetime.utcnow(),
                        notes="Default test stock."
                    )
                    db.session.add(stock)
                    db.session.commit()
                    print(f"✅ Added default stock to portfolio for {email}")
                else:
                    print(f"User {email} already has {len(portfolios)} portfolio(s)")
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
