#!/usr/bin/env python3
"""
Database schema checker and fixer for critical production issues
Ensures all required tables exist and have proper structure
"""

import sqlite3
import os
from datetime import datetime

def check_database_schema():
    """Check if all required tables exist in the database"""
    db_path = 'app.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file 'app.db' not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Found {len(existing_tables)} tables in database:")
        for table in sorted(existing_tables):
            print(f"   ✅ {table}")
        
        # Required tables for critical functionality
        required_tables = {
            'users': 'User authentication and profiles',
            'user_stats': 'Achievement tracking statistics',
            'achievements': 'Achievement definitions',
            'user_achievements': 'User achievement progress',
            'favorites': 'User favorite stocks',
            'watchlist': 'User watchlists',
            'watchlist_stock': 'Stocks in watchlists',
            'portfolios': 'User portfolios',
            'portfolio_stocks': 'Stocks in portfolios',
            'notifications': 'User notifications',
            'price_alerts': 'Stock price alerts'
        }
        
        print(f"\n🔍 Checking for required tables:")
        missing_tables = []
        
        for table, description in required_tables.items():
            if table in existing_tables:
                print(f"   ✅ {table} - {description}")
            else:
                print(f"   ❌ {table} - {description} (MISSING)")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n🚨 CRITICAL: {len(missing_tables)} required tables are missing!")
            print("This explains the 500 errors in achievement tracking and other features.")
            return False
        else:
            print(f"\n✅ All required tables are present!")
            return True
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def check_user_stats_table():
    """Specifically check the user_stats table structure"""
    db_path = 'app.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user_stats table exists and get its structure
        cursor.execute("PRAGMA table_info(user_stats);")
        columns = cursor.fetchall()
        
        if not columns:
            print("❌ user_stats table does not exist!")
            return False
            
        print(f"\n📋 user_stats table structure:")
        for col in columns:
            print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
            
        # Required columns for user_stats
        required_columns = {
            'id', 'user_id', 'predictions_made', 'successful_predictions',
            'stocks_analyzed', 'portfolios_created', 'total_logins',
            'consecutive_login_days', 'forum_posts', 'favorites_added',
            'total_points', 'current_level'
        }
        
        existing_columns = {col[1] for col in columns}
        missing_columns = required_columns - existing_columns
        
        if missing_columns:
            print(f"❌ Missing columns in user_stats: {missing_columns}")
            return False
        else:
            print("✅ user_stats table has all required columns")
            return True
            
    except Exception as e:
        print(f"❌ Error checking user_stats table: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def create_missing_tables():
    """Create any missing tables required for the application"""
    db_path = 'app.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Creating missing tables...")
        
        # user_stats table for achievement tracking
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
        
        # achievements table
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
        
        # user_achievements table
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
        
        # watchlist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # watchlist_stock table  
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist_stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                watchlist_id INTEGER NOT NULL,
                ticker VARCHAR(20) NOT NULL,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (watchlist_id) REFERENCES watchlist (id),
                UNIQUE(watchlist_id, ticker)
            )
        ''')
        
        # notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type VARCHAR(50) NOT NULL,
                title VARCHAR(200) NOT NULL,
                message TEXT,
                is_read BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # price_alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                ticker VARCHAR(20) NOT NULL,
                alert_type VARCHAR(20) NOT NULL,
                target_price DECIMAL(10,2) NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                triggered_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        print("✅ All missing tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    print("🔍 DATABASE SCHEMA CHECKER")
    print("=" * 40)
    
    # Check current schema
    schema_ok = check_database_schema()
    
    if not schema_ok:
        print("\n🔧 Attempting to create missing tables...")
        if create_missing_tables():
            print("\n✅ Database schema fixed!")
            print("🔄 Rerunning schema check...")
            schema_ok = check_database_schema()
        else:
            print("\n❌ Failed to fix database schema!")
    
    # Specific check for user_stats (critical for achievement tracking)
    print("\n" + "=" * 40)
    user_stats_ok = check_user_stats_table()
    
    if schema_ok and user_stats_ok:
        print("\n🎉 DATABASE IS READY!")
        print("   • All required tables exist")
        print("   • Achievement tracking should work")
        print("   • Watchlist functionality should work") 
        print("   • No more 500 errors from missing tables")
    else:
        print("\n🚨 DATABASE ISSUES REMAIN!")
        print("   This will cause 500 errors in:")
        print("   • Achievement tracking (/achievements/api/update_stat)")
        print("   • Watchlist functionality (/portfolio/watchlist)")
        print("   • User statistics and notifications")

if __name__ == "__main__":
    main()
