#!/usr/bin/env python3
"""
Check real subscription behavior by examining existing users in database.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User

def check_real_subscription_behavior():
    """Check actual subscription behavior with database users"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking real subscription behavior with database users...")
        
        # Get first few users from database
        users = User.query.limit(5).all()
        
        if not users:
            print("❌ No users found in database")
            return False
            
        for user in users:
            print(f"\n👤 User: {user.username} ({user.email})")
            print(f"   has_subscription: {getattr(user, 'has_subscription', 'N/A')}")
            print(f"   subscription_type: {getattr(user, 'subscription_type', 'N/A')}")
            print(f"   subscription_end: {getattr(user, 'subscription_end', 'N/A')}")
            print(f"   is_in_trial_period(): {user.is_in_trial_period()}")
            print(f"   has_active_subscription(): {user.has_active_subscription()}")
            
        # Test current system intention
        print(f"\n💡 Current System Design Analysis:")
        print(f"   is_in_trial_period() always returns True")
        print(f"   This means ALL users get access regardless of subscription status")
        print(f"   This appears to be designed as 'free platform with paid plans available'")
        print(f"   Not 'freemium with subscription-gated content'")
        
        return True

if __name__ == '__main__':
    check_real_subscription_behavior()
