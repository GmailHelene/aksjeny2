#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User
from flask_login import login_user

def test_logged_in_dashboard():
    from app.config import DevelopmentConfig
    from app.extensions import db
    app = create_app(DevelopmentConfig)
    
    with app.test_client() as client:
        with app.app_context():
            # Ensure all tables exist (do not recreate to avoid wiping test data)
            # Get a user from database
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return False
            
            print(f"✅ Found user: {user.username}")
            
            # Simulate login by setting session
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
                
            # Test the homepage route with logged-in user
            print("🔍 Testing homepage with logged-in user...")
            response = client.get('/')
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                content = response.get_data(as_text=True)
                
                # Check for user dashboard elements
                dashboard_indicators = [
                    'Din aktivitet',
                    'Dine investeringer', 
                    'recent_activities',
                    'user_stats'
                ]
                
                found_indicators = []
                for indicator in dashboard_indicators:
                    if indicator in content:
                        found_indicators.append(indicator)
                        print(f"✅ Found: {indicator}")
                    else:
                        print(f"❌ Missing: {indicator}")
                
                # Check specifically for activity section
                if 'Din aktivitet' in content:
                    print("✅ Activity section found in template")
                    
                    # Check if we have real user activities or fallback
                    if 'Velkommen til Aksjeradar!' in content:
                        print("ℹ️ Showing fallback welcome message (no real activities)")
                    elif any(word in content for word in ['Lagt til', 'Overvåker', 'Søkte etter']):
                        print("✅ Real user activities found!")
                    else:
                        print("❌ No activities found")
                else:
                    print("❌ No activity section found")
                    
                return len(found_indicators) >= 2
            else:
                print(f"❌ Homepage failed with status: {response.status_code}")
                return False

if __name__ == "__main__":
    success = test_logged_in_dashboard()
    print(f"\n{'✅ Test passed' if success else '❌ Test failed'}")
