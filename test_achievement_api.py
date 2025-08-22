#!/usr/bin/env python3
"""
Test script to check achievement API functionality
"""

import os
import sys
import traceback

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_achievement_imports():
    """Test if we can import achievement models"""
    try:
        print("🔍 Testing achievement model imports...")
        
        # Test basic imports
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models.achievements import UserStats, Achievement, UserAchievement
            from app import db
            
            print("✅ Achievement models imported successfully")
            
            # Check if tables exist
            try:
                # Test UserStats table
                result = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_stats';")
                if result.fetchone():
                    print("✅ user_stats table exists")
                else:
                    print("❌ user_stats table missing")
                
                # Test Achievement table
                result = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='achievements';")
                if result.fetchone():
                    print("✅ achievements table exists")
                else:
                    print("❌ achievements table missing")
                
                # Test UserAchievement table
                result = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_achievements';")
                if result.fetchone():
                    print("✅ user_achievements table exists")
                else:
                    print("❌ user_achievements table missing")
                    
            except Exception as e:
                print(f"❌ Database table check failed: {e}")
                # Try to create tables
                try:
                    print("🔧 Attempting to create missing tables...")
                    db.create_all()
                    print("✅ Tables created successfully")
                except Exception as create_error:
                    print(f"❌ Table creation failed: {create_error}")
            
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        traceback.print_exc()

def test_achievement_api_logic():
    """Test the achievement API logic without HTTP request"""
    try:
        print("\n🔍 Testing achievement API logic...")
        
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models.achievements import UserStats, check_user_achievements
            from app import db
            
            # Test creating a UserStats record
            test_user_id = 1  # Assuming user 1 exists
            
            # Check if user stats exist
            user_stats = UserStats.query.filter_by(user_id=test_user_id).first()
            if not user_stats:
                print("📝 Creating test UserStats record...")
                user_stats = UserStats(user_id=test_user_id)
                db.session.add(user_stats)
                db.session.flush()
                print("✅ UserStats record created")
            else:
                print("✅ UserStats record found")
            
            # Test updating stats
            print("📈 Testing stat updates...")
            original_favorites = user_stats.favorites_added
            user_stats.favorites_added += 1
            new_value = user_stats.favorites_added
            
            # Test achievement checking
            print("🏆 Testing achievement checking...")
            new_achievements = check_user_achievements(test_user_id, 'favorites', new_value)
            print(f"✅ Achievement check completed. New achievements: {len(new_achievements)}")
            
            # Rollback to not affect database
            db.session.rollback()
            print("✅ Achievement API logic test completed successfully")
            
    except Exception as e:
        print(f"❌ Achievement API logic test failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Achievement API Test Suite")
    print("=" * 50)
    
    test_achievement_imports()
    test_achievement_api_logic()
    
    print("\n✅ Test suite completed")
