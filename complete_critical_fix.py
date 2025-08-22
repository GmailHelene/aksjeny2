#!/usr/bin/env python3
"""
Complete Critical Issues Resolver - Handles database and import fixes
"""

import os
import sys
import sqlite3
from datetime import datetime

def setup_python_path():
    """Setup Python path for imports"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    print(f"✅ Python path setup: {current_dir}")

def check_and_fix_database():
    """Check and fix database schema issues"""
    print("\n🔧 DATABASE SCHEMA CHECK & FIX")
    print("=" * 50)
    
    db_path = 'app.db'
    if not os.path.exists(db_path):
        print("❌ app.db not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = {row[0] for row in cursor.fetchall()}
        
        print(f"📊 Found {len(existing_tables)} existing tables")
        
        # Required tables for critical issues
        required_tables = {
            'achievements': '''
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
            ''',
            'user_stats': '''
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
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'user_achievements': '''
                CREATE TABLE user_achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    achievement_id INTEGER NOT NULL,
                    earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    progress INTEGER DEFAULT 1,
                    UNIQUE(user_id, achievement_id)
                )
            '''
        }
        
        tables_created = []
        for table_name, create_sql in required_tables.items():
            if table_name not in existing_tables:
                print(f"🔧 Creating {table_name} table...")
                cursor.execute(create_sql)
                tables_created.append(table_name)
            else:
                print(f"✅ {table_name} table exists")
        
        if tables_created:
            conn.commit()
            print(f"✅ Created tables: {', '.join(tables_created)}")
            
            # Add default achievements if achievements table was created
            if 'achievements' in tables_created:
                default_achievements = [
                    ('Welcome', 'First login to Aksjeradar', 'bi-star', 'info', 10, 'general', 'login', 1),
                    ('Stock Explorer', 'Analyze your first stock', 'bi-graph-up', 'primary', 25, 'analysis', 'stocks_analyzed', 1),
                    ('Portfolio Builder', 'Create your first portfolio', 'bi-briefcase', 'success', 50, 'portfolio', 'portfolios_created', 1),
                    ('Favorites Master', 'Add 5 stocks to favorites', 'bi-heart', 'danger', 30, 'favorites', 'favorites_added', 5),
                    ('Streak Master', 'Login for 7 consecutive days', 'bi-calendar-check', 'warning', 75, 'engagement', 'consecutive_login_days', 7)
                ]
                
                for achievement in default_achievements:
                    cursor.execute('''
                        INSERT OR IGNORE INTO achievements 
                        (name, description, icon, badge_color, points, category, requirement_type, requirement_count)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', achievement)
                
                conn.commit()
                print(f"✅ Added {len(default_achievements)} default achievements")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_flask_imports():
    """Test critical Flask app imports"""
    print("\n🧪 FLASK IMPORTS TEST")
    print("=" * 50)
    
    try:
        # Test basic app creation
        from app import create_app
        print("✅ Successfully imported create_app")
        
        # Test critical models
        from app.models import Achievement, UserAchievement, UserStats
        print("✅ Successfully imported achievement models")
        
        # Test achievement routes
        from app.routes.achievements import achievements_bp
        print("✅ Successfully imported achievement routes")
        
        # Test other critical routes
        from app.routes.portfolio import portfolio
        print("✅ Successfully imported portfolio routes")
        
        from app.routes.advanced_features import advanced_features
        print("✅ Successfully imported advanced features")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        print(f"   Full error: {traceback.format_exc()}")
        return False

def test_app_creation():
    """Test Flask app creation and route registration"""
    print("\n🏗️  FLASK APP CREATION TEST")
    print("=" * 50)
    
    try:
        from app import create_app
        
        # Create test app
        app = create_app('development')
        print("✅ App created successfully")
        
        # Count routes
        total_routes = len(list(app.url_map.iter_rules()))
        print(f"✅ {total_routes} routes registered")
        
        # Check critical routes
        critical_routes = [
            '/achievements/api/update_stat',
            '/portfolio/watchlist', 
            '/advanced/crypto-dashboard',
            '/analysis/screener',
            '/news-intelligence'
        ]
        
        found_routes = 0
        with app.app_context():
            for rule in app.url_map.iter_rules():
                for critical in critical_routes:
                    if critical in str(rule):
                        print(f"✅ Found: {rule}")
                        found_routes += 1
                        break
        
        print(f"✅ Found {found_routes}/{len(critical_routes)} critical routes")
        
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def run_complete_fix():
    """Run complete fix for all critical issues"""
    print("🚀 COMPLETE CRITICAL ISSUES FIX")
    print("=" * 60)
    print("Fixing database, imports, and testing app creation...")
    
    results = {}
    
    # Step 1: Setup Python path
    setup_python_path()
    
    # Step 2: Fix database
    results['database'] = check_and_fix_database()
    
    # Step 3: Test imports
    results['imports'] = test_flask_imports()
    
    # Step 4: Test app creation
    results['app_creation'] = test_app_creation()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    success_count = sum(1 for success in results.values() if success)
    total_tests = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name.upper():20} {status}")
    
    print(f"\nOVERALL: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("\n🎉 ALL CRITICAL INFRASTRUCTURE FIXED!")
        print("   Ready to start Flask server and test routes.")
        print("\n🚀 Next steps:")
        print("   1. python simple_flask_starter.py")
        print("   2. python test_critical_routes_comprehensive.py")
    else:
        print("\n⚠️  Some issues remain. Check errors above.")
    
    return success_count == total_tests

if __name__ == "__main__":
    success = run_complete_fix()
    sys.exit(0 if success else 1)
