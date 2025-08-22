#!/usr/bin/env python3
"""
Create missing database tables for achievements system
"""

import sqlite3
import os

def create_achievements_tables():
    """Create achievements-related tables if they don't exist"""
    
    # Get the database path
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    try:
        print("🔧 Connecting to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = {row[0] for row in cursor.fetchall()}
        print(f"📊 Found {len(existing_tables)} existing tables")
        
        tables_created = []
        
        # Create achievements table
        if 'achievements' not in existing_tables:
            print("Creating achievements table...")
            cursor.execute('''
                CREATE TABLE achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    icon VARCHAR(50) DEFAULT 'bi-trophy',
                    badge_color VARCHAR(20) DEFAULT 'warning',
                    points INTEGER DEFAULT 10,
                    category VARCHAR(50) DEFAULT 'general',
                    requirement_type VARCHAR(50) NOT NULL,
                    requirement_count INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            tables_created.append('achievements')
        else:
            print("✅ achievements table already exists")
        
        # Create user_stats table
        if 'user_stats' not in existing_tables:
            print("Creating user_stats table...")
            cursor.execute('''
                CREATE TABLE user_stats (
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
            tables_created.append('user_stats')
        else:
            print("✅ user_stats table already exists")
        
        # Create user_achievements table
        if 'user_achievements' not in existing_tables:
            print("Creating user_achievements table...")
            cursor.execute('''
                CREATE TABLE user_achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    achievement_id INTEGER NOT NULL,
                    earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    progress INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (achievement_id) REFERENCES achievements (id),
                    UNIQUE(user_id, achievement_id)
                )
            ''')
            tables_created.append('user_achievements')
        else:
            print("✅ user_achievements table already exists")
        
        # Commit changes
        conn.commit()
        
        if tables_created:
            print(f"✅ Successfully created tables: {', '.join(tables_created)}")
        else:
            print("✅ All required tables already exist")
        
        # Add some default achievements if achievements table was just created
        if 'achievements' in tables_created:
            print("🎯 Adding default achievements...")
            default_achievements = [
                ('First Steps', 'Welcome to Aksjeradar!', 'bi-star', 'info', 10, 'general', 'login', 1),
                ('Stock Explorer', 'Analyze your first stock', 'bi-graph-up', 'primary', 25, 'analysis', 'stocks_analyzed', 1),
                ('Portfolio Builder', 'Create your first portfolio', 'bi-briefcase', 'success', 50, 'portfolio', 'portfolios_created', 1),
                ('Favorites Collector', 'Add 5 stocks to favorites', 'bi-heart', 'danger', 30, 'favorites', 'favorites_added', 5),
                ('Daily Trader', 'Login for 7 consecutive days', 'bi-calendar-check', 'warning', 75, 'engagement', 'consecutive_login_days', 7),
                ('Power User', 'Reach 1000 total points', 'bi-lightning', 'info', 200, 'points', 'total_points', 1000)
            ]
            
            for achievement in default_achievements:
                cursor.execute('''
                    INSERT OR IGNORE INTO achievements 
                    (name, description, icon, badge_color, points, category, requirement_type, requirement_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', achievement)
            
            conn.commit()
            print(f"✅ Added {len(default_achievements)} default achievements")
        
        # Verify final state
        cursor.execute("SELECT COUNT(*) FROM achievements;")
        achievement_count = cursor.fetchone()[0]
        print(f"📊 Total achievements in database: {achievement_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🚀 ACHIEVEMENTS DATABASE SETUP")
    print("=" * 40)
    
    success = create_achievements_tables()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("   Achievement tracking should now work properly.")
    else:
        print("\n❌ Database setup failed!")
        print("   Please check the errors above.")
