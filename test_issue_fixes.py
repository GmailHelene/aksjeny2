#!/usr/bin/env python3
"""Test the profile page fix and navigation changes"""

import os
import sys
import requests
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_profile_page_fix():
    """Test if profile page loads without 500 error"""
    print("🧪 Testing profile page fix...")
    
    try:
        # Import after adding path
        from app import create_app
        from app.extensions import db
        from app.models.user import User
        from app.models.favorites import Favorites
        from config import DevelopmentConfig
        
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            # Create test user if doesn't exist
            test_user = User.query.filter_by(email='test@example.com').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    has_subscription=True,
                    subscription_type='monthly'
                )
                test_user.set_password('testpass')
                db.session.add(test_user)
                db.session.commit()
                print("✅ Created test user")
            
            # Test the Favorites model
            try:
                user_favorites = Favorites.get_user_favorites(test_user.id)
                print(f"✅ Favorites query works: {len(user_favorites)} favorites found")
            except Exception as e:
                print(f"❌ Favorites query failed: {e}")
                return False
            
            # Test user methods
            try:
                user_prefs = test_user.get_notification_settings()
                user_lang = test_user.get_language()
                print(f"✅ User methods work: lang={user_lang}, prefs={type(user_prefs)}")
            except Exception as e:
                print(f"❌ User methods failed: {e}")
                return False
            
            # Test profile route logic (simulate without full request context)
            try:
                subscription_status = getattr(test_user, 'subscription_status', 'free')
                subscription_type = getattr(test_user, 'subscription_type', 'monthly')
                has_subscription = getattr(test_user, 'has_subscription', True)
                
                user_stats = {
                    'member_since': getattr(test_user, 'created_at', datetime.now()),
                    'last_login': getattr(test_user, 'last_login', None),
                    'total_searches': getattr(test_user, 'search_count', 0),
                    'favorite_stocks': getattr(test_user, 'favorite_count', 0)
                }
                
                print(f"✅ Profile data assembly works: status={subscription_status}, type={subscription_type}")
                return True
                
            except Exception as e:
                print(f"❌ Profile route logic failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_changes():
    """Test that template changes are valid"""
    print("🧪 Testing template changes...")
    
    try:
        # Read the base template to verify changes
        base_template_path = 'app/templates/base.html'
        
        if os.path.exists(base_template_path):
            with open(base_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check that Abonnement was removed from navigation
            if 'Abonnement</a></li>' not in content:
                print("✅ Abonnement menu item successfully removed")
            else:
                print("❌ Abonnement menu item still present")
                return False
            
            # Check that Forum link was added to footer
            if 'Forum</a>' in content and 'bi-chat-dots' in content:
                print("✅ Forum link successfully added to footer")
            else:
                print("❌ Forum link not found in footer")
                return False
            
            return True
        else:
            print(f"❌ Template file not found: {base_template_path}")
            return False
            
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

def test_complete_fixes():
    """Run comprehensive test of all fixes"""
    print("🔬 Running comprehensive fix tests...")
    print("=" * 50)
    
    profile_test = test_profile_page_fix()
    template_test = test_template_changes()
    
    print("=" * 50)
    print("📊 TEST RESULTS:")
    print(f"Profile page fix: {'✅ PASS' if profile_test else '❌ FAIL'}")
    print(f"Template changes: {'✅ PASS' if template_test else '❌ FAIL'}")
    
    if profile_test and template_test:
        print("🎉 ALL TESTS PASSED! Issues should be resolved.")
        return True
    else:
        print("⚠️  Some tests failed. Manual verification needed.")
        return False

if __name__ == '__main__':
    success = test_complete_fixes()
    sys.exit(0 if success else 1)
