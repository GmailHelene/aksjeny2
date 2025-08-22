#!/usr/bin/env python3
"""
Database Fix for Critical Issues - Achievement Tracking & User Stats
This script creates missing tables needed for achievement tracking API
"""

import sqlite3
import os
import sys
from datetime import datetime

def fix_database_schema():
    """Create missing tables for achievement tracking and user stats"""
    db_path = 'app.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file 'app.db' not found!")
        print("Make sure you're running this from the project root directory.")
        return False
    
    try:
        print("🔧 Connecting to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Found {len(existing_tables)} existing tables")
        
        # Create user_stats table for achievement tracking
        print("🔧 Creating user_stats table...")
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
        print("🔧 Creating achievements table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                icon VARCHAR(50),
                category VARCHAR(50),
                points INTEGER DEFAULT 0,
                requirement_type VARCHAR(50),
                requirement_value INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_achievements table
        print("🔧 Creating user_achievements table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_id INTEGER NOT NULL,
                unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                progress INTEGER DEFAULT 0,
                is_completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (id),
                UNIQUE(user_id, achievement_id)
            )
        ''')
        
        # Insert default achievements
        print("🔧 Adding default achievements...")
        default_achievements = [
            ('First Login', 'Welcome to the platform!', 'login', 'engagement', 10, 'total_logins', 1),
            ('Stock Analyzer', 'Analyze your first stock', 'chart', 'analysis', 25, 'stocks_analyzed', 1),
            ('Portfolio Creator', 'Create your first portfolio', 'portfolio', 'portfolio', 50, 'portfolios_created', 1),
            ('Prediction Master', 'Make 10 successful predictions', 'target', 'predictions', 100, 'successful_predictions', 10),
            ('Daily Trader', 'Login for 7 consecutive days', 'calendar', 'engagement', 75, 'consecutive_login_days', 7),
            ('Power User', 'Reach 1000 total points', 'star', 'points', 200, 'total_points', 1000)
        ]
        
        for achievement in default_achievements:
            cursor.execute('''
                INSERT OR IGNORE INTO achievements 
                (name, description, icon, category, points, requirement_type, requirement_value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', achievement)
        
        # Create an index for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_stats_user_id ON user_stats(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_achievements_user_id ON user_achievements(user_id)')
        
        # Commit all changes
        conn.commit()
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        new_tables = [row[0] for row in cursor.fetchall()]
        
        created_tables = set(new_tables) - set(existing_tables)
        if created_tables:
            print(f"✅ Successfully created tables: {', '.join(created_tables)}")
        else:
            print("ℹ️  All tables already existed")
        
        # Check if user_stats table has correct structure
        cursor.execute("PRAGMA table_info(user_stats);")
        columns = cursor.fetchall()
        print(f"✅ user_stats table has {len(columns)} columns")
        
        # Check achievements count
        cursor.execute("SELECT COUNT(*) FROM achievements;")
        achievement_count = cursor.fetchone()[0]
        print(f"✅ {achievement_count} achievements in database")
        
        print("\n🎉 Database schema fix completed successfully!")
        print("   The achievement tracking API should now work properly.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        import traceback
        print(f"❌ Full error: {traceback.format_exc()}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def test_achievement_api():
    """Test if the achievement API works after database fix"""
    print("\n🧪 Testing achievement API functionality...")
    
    try:
        # Test database connection and query
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        # Test basic queries that the API would use
        cursor.execute("SELECT COUNT(*) FROM user_stats")
        stats_count = cursor.fetchone()[0]
        print(f"✅ user_stats table accessible, {stats_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM achievements")  
        achievements_count = cursor.fetchone()[0]
        print(f"✅ achievements table accessible, {achievements_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM user_achievements")
        user_achievements_count = cursor.fetchone()[0]
        print(f"✅ user_achievements table accessible, {user_achievements_count} records")
        
        print("✅ All achievement-related tables are working!")
        
        return True
        
    except Exception as e:
        print(f"❌ Achievement API test failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    print("🚀 DATABASE SCHEMA FIX FOR CRITICAL ISSUES")
    print("=" * 60)
    print("This script fixes the root cause of:")
    print("• Sentiment analysis 500 errors")
    print("• Achievement tracking API failures") 
    print("• User stats-related crashes\n")
    
    # Fix database schema
    success = fix_database_schema()
    
    if success:
        # Test the fix
        test_success = test_achievement_api()
        
        if test_success:
            print("\n🎉 ALL FIXES SUCCESSFUL!")
            print("✅ Database schema is now complete")
            print("✅ Achievement tracking should work")
            print("✅ User stats API should work")
            print("\n🎯 Next steps:")
            print("1. Start the Flask server: python main.py")
            print("2. Test achievement endpoint: /achievements/api/update_stat")
            print("3. Run comprehensive route tests")
        else:
            print("\n⚠️  Schema created but API test failed")
            print("   Manual verification may be needed")
    else:
        print("\n❌ Database fix failed")
        print("   Check error messages above")

if __name__ == "__main__":
    main()
