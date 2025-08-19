#!/usr/bin/env python3
"""
Test script to verify subscription access logic works correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User

def test_subscription_access():
    """Test that subscription access logic works correctly"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing subscription access logic...")
        
        # Test 1: Free user without subscription
        print("\n📝 Test 1: User without subscription")
        user1 = User(
            username='test_free',
            email='test_free@example.com',
            has_subscription=False,
            subscription_type='free',
            subscription_end=None
        )
        
        print(f"   has_subscription: {user1.has_subscription}")
        print(f"   subscription_type: {user1.subscription_type}")
        print(f"   subscription_end: {user1.subscription_end}")
        print(f"   has_active_subscription(): {user1.has_active_subscription()}")
        print(f"   ✅ Expected: False, Got: {user1.has_active_subscription()}")
        
        # Test 2: User with active monthly subscription
        print("\n📝 Test 2: User with active monthly subscription")
        user2 = User(
            username='test_monthly',
            email='test_monthly@example.com',
            has_subscription=True,
            subscription_type='monthly',
            subscription_end=datetime.utcnow() + timedelta(days=15)  # 15 days left
        )
        
        print(f"   has_subscription: {user2.has_subscription}")
        print(f"   subscription_type: {user2.subscription_type}")
        print(f"   subscription_end: {user2.subscription_end}")
        print(f"   has_active_subscription(): {user2.has_active_subscription()}")
        print(f"   ✅ Expected: True, Got: {user2.has_active_subscription()}")
        
        # Test 3: User with expired subscription
        print("\n📝 Test 3: User with expired subscription")
        user3 = User(
            username='test_expired',
            email='test_expired@example.com',
            has_subscription=True,
            subscription_type='monthly',
            subscription_end=datetime.utcnow() - timedelta(days=5)  # Expired 5 days ago
        )
        
        print(f"   has_subscription: {user3.has_subscription}")
        print(f"   subscription_type: {user3.subscription_type}")
        print(f"   subscription_end: {user3.subscription_end}")
        print(f"   has_active_subscription(): {user3.has_active_subscription()}")
        print(f"   ✅ Expected: False, Got: {user3.has_active_subscription()}")
        
        # Test 4: User with active yearly subscription
        print("\n📝 Test 4: User with active yearly subscription")
        user4 = User(
            username='test_yearly',
            email='test_yearly@example.com',
            has_subscription=True,
            subscription_type='yearly',
            subscription_end=datetime.utcnow() + timedelta(days=300)  # 300 days left
        )
        
        print(f"   has_subscription: {user4.has_subscription}")
        print(f"   subscription_type: {user4.subscription_type}")
        print(f"   subscription_end: {user4.subscription_end}")
        print(f"   has_active_subscription(): {user4.has_active_subscription()}")
        print(f"   ✅ Expected: True, Got: {user4.has_active_subscription()}")
        
        # Test 5: User with lifetime subscription
        print("\n📝 Test 5: User with lifetime subscription")
        user5 = User(
            username='test_lifetime',
            email='test_lifetime@example.com',
            has_subscription=True,
            subscription_type='lifetime',
            subscription_end=None  # No end date for lifetime
        )
        
        print(f"   has_subscription: {user5.has_subscription}")
        print(f"   subscription_type: {user5.subscription_type}")
        print(f"   subscription_end: {user5.subscription_end}")
        print(f"   has_active_subscription(): {user5.has_active_subscription()}")
        print(f"   ✅ Expected: True, Got: {user5.has_active_subscription()}")
        
        # Summary
        test_results = [
            not user1.has_active_subscription(),  # Should be False
            user2.has_active_subscription(),       # Should be True
            not user3.has_active_subscription(),  # Should be False (expired)
            user4.has_active_subscription(),       # Should be True
            user5.has_active_subscription(),       # Should be True (lifetime)
        ]
        
        print(f"\n🎯 Test Results Summary:")
        print(f"   ✅ Passed: {sum(test_results)}/5 tests")
        print(f"   ❌ Failed: {5 - sum(test_results)}/5 tests")
        
        if all(test_results):
            print(f"\n🎉 ALL TESTS PASSED! Subscription logic works correctly.")
            print(f"   - Free users are correctly denied access")
            print(f"   - Active monthly/yearly subscribers get full access")
            print(f"   - Expired subscriptions are correctly denied")
            print(f"   - Lifetime subscriptions work indefinitely")
            return True
        else:
            print(f"\n❌ SOME TESTS FAILED! Subscription logic needs fixing.")
            return False

if __name__ == '__main__':
    success = test_subscription_access()
    sys.exit(0 if success else 1)
