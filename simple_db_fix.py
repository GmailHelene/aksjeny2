import sqlite3
import os

def fix_database():
    print("🔧 Starting database fix...")
    # Use full path to database file
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'app.db')
    
    if not os.path.exists(db_path):
        print("❌ app.db not found in current directory")
        return False
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Creating user_stats table...")
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
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("Creating achievements table...")
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
        
        print("Creating user_achievements table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_id INTEGER NOT NULL,
                unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                progress INTEGER DEFAULT 0,
                is_completed BOOLEAN DEFAULT 0,
                UNIQUE(user_id, achievement_id)
            )
        ''')
        
        conn.commit()
        
        # Check tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"✅ Database fix completed! Found {len(tables)} tables.")
        if 'user_stats' in tables:
            print("✅ user_stats table exists")
        if 'achievements' in tables:
            print("✅ achievements table exists")
        if 'user_achievements' in tables:
            print("✅ user_achievements table exists")
            
        return True
        
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
