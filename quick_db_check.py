#!/usr/bin/env python3
"""
Quick Database Status Check
"""

import sqlite3
import os

def check_db_status():
    """Quick check of database status"""
    db_path = 'app.db'
    
    if not os.path.exists(db_path):
        print("❌ app.db not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table list
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Database has {len(tables)} tables:")
        
        # Check critical tables
        critical_tables = ['users', 'achievements', 'user_stats', 'user_achievements', 'portfolios', 'watchlist']
        
        for table in critical_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table} ({count} records)")
            else:
                print(f"   ❌ {table} (missing)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 QUICK DATABASE STATUS CHECK")
    print("=" * 40)
    check_db_status()
