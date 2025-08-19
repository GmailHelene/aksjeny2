#!/usr/bin/env python3

"""
Test Flask-Login authentication flow to debug current_user context issue
"""

from app import create_app, db
from app.models.user import User
from flask_login import login_user, current_user
import sys

def test_authentication():
    """Test complete authentication flow with Flask-Login"""
    print("🔍 Testing Flask-Login authentication flow...")
    
    app = create_app()
    
    with app.app_context():
        # Find our test user
        user = User.query.filter_by(username='helene_luxus').first()
        if not user:
            print("❌ Test user helene_luxus not found")
            return
            
        print(f"✅ Found user: {user.username}")
        
        # Now test within a request context with login_user
        with app.test_client() as client:
            with app.test_request_context():
                # Login the user using Flask-Login
                login_user(user)
                
                print(f"🔍 After login_user:")
                print(f"   current_user: {current_user}")
                print(f"   current_user.is_authenticated: {current_user.is_authenticated}")
                print(f"   current_user.username: {getattr(current_user, 'username', 'N/A')}")
                
                # Test the index route within the same context
                print("\n📡 Testing route with authenticated user...")
                response = client.get('/')
                print(f"📊 Response status: {response.status_code}")
                
                # Check what's in the response
                content = response.get_data(as_text=True)
                
                # Look for authentication indicators
                auth_indicators = [
                    'current_user.is_authenticated',
                    'user_stats.recent_activities', 
                    'Velkommen tilbake',
                    'Din aktivitet',
                    'helene_luxus'
                ]
                
                print("\n🔍 Checking authentication indicators in response:")
                for indicator in auth_indicators:
                    found = indicator in content
                    print(f"   {'✅' if found else '❌'} {indicator}: {found}")
                
                # Look for activity stock symbols (confirms user_stats data)
                activity_symbols = ['EQNR.OL', 'DNB.OL', 'TEL.OL', 'SALM.OL', 'LSG.OL']
                print("\n🔍 Checking for activity stock symbols:")
                for symbol in activity_symbols:
                    found = symbol in content
                    print(f"   {'✅' if found else '❌'} {symbol}: {found}")
                    
                # Check for fallback welcome message
                welcome_indicators = [
                    'Velkommen til finansiell analyse',
                    'comprehensive investment platform',
                    'no recent activity'
                ]
                
                print("\n🔍 Checking for fallback welcome message:")
                for indicator in welcome_indicators:
                    found = indicator in content
                    print(f"   {'✅' if found else '❌'} {indicator}: {found}")

if __name__ == "__main__":
    test_authentication()
