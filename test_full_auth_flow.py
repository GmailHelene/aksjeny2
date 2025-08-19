#!/usr/bin/env python3

"""
Test complete authentication flow through login route to fix session persistence
"""

from app import create_app, db
from app.models.user import User
import sys

def test_full_authentication_flow():
    """Test complete authentication flow through actual login route"""
    print("🔍 Testing complete authentication flow through login route...")
    
    app = create_app()
    
    with app.app_context():
        # Find our test user 
        user = User.query.filter_by(username='helene_luxus').first()
        if not user:
            print("❌ Test user helene_luxus not found")
            return
            
        print(f"✅ Found user: {user.username}")
        print(f"   User ID: {user.id}")
        print(f"   User email: {user.email}")
        
        # Test authentication through login route
        with app.test_client() as client:
            # First get the login page to establish session
            print("\n🔍 Step 1: Getting login page...")
            response = client.get('/login')
            print(f"   Login page status: {response.status_code}")
            
            # Now attempt to login with credentials
            print("\n🔍 Step 2: Attempting login...")
            login_data = {
                'username': 'helene_luxus',
                'password': 'password123'  # From our creation script
            }
            
            response = client.post('/login', data=login_data, follow_redirects=True)
            print(f"   Login response status: {response.status_code}")
            print(f"   Final URL: {response.request.path if hasattr(response, 'request') else 'Unknown'}")
            
            # Check if login was successful by looking at response content
            content = response.get_data(as_text=True)
            
            # Look for login success indicators
            login_success_indicators = [
                'logout',  # Logout link appears when logged in
                'helene_luxus',  # Username appears when logged in
                'Din aktivitet',  # Norwegian for "Your activity"
                'Velkommen tilbake'  # Norwegian for "Welcome back"
            ]
            
            print("\n🔍 Checking login success indicators:")
            for indicator in login_success_indicators:
                found = indicator in content
                print(f"   {'✅' if found else '❌'} {indicator}: {found}")
            
            # Check for login failure indicators
            login_failure_indicators = [
                'Invalid username or password',
                'Login failed',
                'error',
                'form-control-error'
            ]
            
            print("\n🔍 Checking login failure indicators:")
            for indicator in login_failure_indicators:
                found = indicator.lower() in content.lower()
                print(f"   {'✅' if not found else '❌'} {indicator}: {'Not Found' if not found else 'Found - Problem!'}")
            
            # Now test the homepage after login
            print("\n🔍 Step 3: Testing homepage after login...")
            response = client.get('/')
            print(f"   Homepage status: {response.status_code}")
            
            content = response.get_data(as_text=True)
            
            # Look for authenticated homepage content
            auth_indicators = [
                'current_user.is_authenticated',
                'user_stats.recent_activities', 
                'Din aktivitet',
                'helene_luxus'
            ]
            
            print("\n🔍 Checking authenticated homepage content:")
            for indicator in auth_indicators:
                found = indicator in content
                print(f"   {'✅' if found else '❌'} {indicator}: {found}")
            
            # Look for activity stock symbols
            activity_symbols = ['EQNR.OL', 'DNB.OL', 'TEL.OL', 'SALM.OL', 'LSG.OL']
            print("\n🔍 Checking for activity stock symbols:")
            for symbol in activity_symbols:
                found = symbol in content
                print(f"   {'✅' if found else '❌'} {symbol}: {found}")
                
            # Check for generic welcome message (should NOT appear when authenticated)
            fallback_indicators = [
                'Velkommen til finansiell analyse',
                'comprehensive investment platform',
                'no recent activity'
            ]
            
            print("\n🔍 Checking for fallback welcome message (should NOT appear):")
            for indicator in fallback_indicators:
                found = indicator in content
                print(f"   {'✅' if not found else '❌'} {indicator}: {'Not Found (Good!)' if not found else 'Found (Problem!)'}")
                
            # Save a snippet of the response for debugging
            print(f"\n📄 Response snippet (first 500 chars):")
            print(content[:500])

if __name__ == "__main__":
    test_full_authentication_flow()
