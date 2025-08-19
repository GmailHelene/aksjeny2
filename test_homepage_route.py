#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Portfolio, PortfolioStock, Watchlist
from app.models.watchlist import WatchlistItem

def test_homepage_route():
    app = create_app()
    
    with app.test_client() as client:
        # Test the homepage route
        print("Testing homepage route...")
        response = client.get('/')
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.get_data(as_text=True)
            
            # Check if we can find activity data in the response
            if 'Lagt til' in content and 'Søkte etter' in content:
                print("✅ Found activity data in homepage response!")
                
                # Check if it's dynamic or hardcoded
                if 'Din aktivitet' in content:
                    print("✅ Dashboard section found!")
                else:
                    print("❌ No dashboard section found")
                    
            else:
                print("❌ No activity data found in homepage")
                # Let's check for debug content
                if 'recent_activities' in content:
                    print("🔍 Found recent_activities variable in template")
                else:
                    print("❌ No recent_activities variable found")
                    
        else:
            print(f"❌ Homepage failed with status: {response.status_code}")
            
        # Test with a logged-in user simulation
        with app.app_context():
            user = User.query.first()
            if user:
                print(f"\n🔍 Testing with user: {user.username}")
                
                # Create mock Flask-Login current_user context
                from flask_login import login_user
                with client.session_transaction() as sess:
                    # Simulate being logged in
                    pass
                    
    return True

if __name__ == "__main__":
    test_homepage_route()
