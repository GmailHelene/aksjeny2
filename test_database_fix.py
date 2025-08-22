#!/usr/bin/env python3
"""
Test specific critical routes to identify 500 errors
"""

import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_achievement_api():
    """Test achievement tracking API directly"""
    try:
        from app import create_app
        from app.models.achievements import UserStats
        from flask import Flask
        
        app = create_app()
        
        with app.app_context():
            print("🔍 Testing Achievement API Components...")
            
            # Test 1: Check if UserStats model can be imported
            try:
                print(f"   ✅ UserStats model imported successfully")
                print(f"   📋 UserStats table name: {UserStats.__tablename__}")
            except Exception as e:
                print(f"   ❌ UserStats model error: {e}")
                return False
            
            # Test 2: Check database connection
            try:
                from app.models import db
                
                # Try to query existing tables
                result = db.engine.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in result]
                print(f"   📊 Found {len(tables)} tables in database")
                
                if 'user_stats' in tables:
                    print("   ✅ user_stats table exists")
                else:
                    print("   ❌ user_stats table MISSING - this causes 500 errors!")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Database connection error: {e}")
                return False
            
            # Test 3: Try to create a UserStats instance
            try:
                # Don't actually save, just test instantiation
                test_stats = UserStats(user_id=999)
                print("   ✅ UserStats instantiation works")
            except Exception as e:
                print(f"   ❌ UserStats instantiation error: {e}")
                return False
                
            print("   🎉 Achievement API components are working!")
            return True
            
    except Exception as e:
        print(f"❌ Critical error testing achievement API: {e}")
        return False

def test_database_tables():
    """Check which tables exist in the database"""
    try:
        import sqlite3
        
        db_path = 'app.db'
        if not os.path.exists(db_path):
            print("❌ Database file app.db not found!")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Database contains {len(tables)} tables:")
        for table in sorted(tables):
            print(f"   📋 {table}")
        
        # Check for critical missing tables
        required_tables = ['users', 'user_stats', 'achievements', 'user_achievements']
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            print(f"\n❌ CRITICAL: Missing tables: {missing}")
            print("   These missing tables cause 500 errors!")
            return False
        else:
            print("\n✅ All critical tables are present")
            return True
        
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False

def create_missing_database_tables():
    """Create missing database tables"""
    try:
        import sqlite3
        
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        print("🔧 Creating missing database tables...")
        
        # Create user_stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                predictions_made INTEGER DEFAULT 0,
                successful_predictions INTEGER DEFAULT 0,
                stocks_analyzed INTEGER DEFAULT 0,
                portfolios_created INTEGER DEFAULT 0,
                total_logins INTEGER DEFAULT 0,
                consecutive_login_days INTEGER DEFAULT 0,
                last_login_date DATE,
                forum_posts INTEGER DEFAULT 0,
                favorites_added INTEGER DEFAULT 0,
                total_points INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create achievements table  
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                icon VARCHAR(50),
                badge_color VARCHAR(20),
                points INTEGER DEFAULT 0,
                condition_type VARCHAR(50),
                condition_value INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_id INTEGER NOT NULL,
                earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (id),
                UNIQUE(user_id, achievement_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

def main():
    print("🚀 TESTING CRITICAL ROUTES AND DATABASE")
    print("=" * 50)
    
    # Test 1: Database tables
    if not test_database_tables():
        print("\n🔧 Attempting to create missing tables...")
        if create_missing_database_tables():
            print("✅ Database fixed! Re-testing...")
            test_database_tables()
        else:
            print("❌ Could not fix database!")
    
    # Test 2: Achievement API components
    test_achievement_api()
    
    print("\n🎯 NEXT STEPS:")
    print("1. If user_stats table was missing, it's now created")
    print("2. Achievement tracking API should now work")
    print("3. Test the actual /achievements/api/update_stat endpoint")
    print("4. Continue with remaining critical issues")

if __name__ == "__main__":
    main()
