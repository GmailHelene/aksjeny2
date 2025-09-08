"""
comprehensive_test_user_fix.py - A comprehensive fix for test user login issues
"""

import os
import sys
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash
from datetime import datetime

def find_database_file():
    """Find the database file used by the application"""
    # Check in the current directory first
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'app.db')
    
    if os.path.exists(db_path):
        print(f"Database found at: {db_path}")
        return db_path
    
    print(f"Database not found at expected location: {db_path}")
    
    # Fallback - search for .db files in various directories
    possible_locations = [
        current_dir,
        os.path.join(current_dir, 'app'),
        os.path.join(current_dir, 'instance')
    ]
    
    for location in possible_locations:
        if os.path.isdir(location):
            for file in os.listdir(location):
                if file.endswith('.db'):
                    db_path = os.path.join(location, file)
                    print(f"Found database at: {db_path}")
                    return db_path
    
    print("No database file found!")
    return None

def fix_test_users(db_path):
    """Fix test users in the database"""
    if not db_path or not os.path.exists(db_path):
        print(f"Database file not found at: {db_path}")
        return False
    
    # Test user data
    test_users = [
        {
            'email': 'test@aksjeradar.trade',
            'username': 'testuser',
            'password': 'aksjeradar2024'
        },
        {
            'email': 'investor@aksjeradar.trade',
            'username': 'investor',
            'password': 'aksjeradar2024'
        }
    ]
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("Users table not found in database!")
            return False
        
        # Process each test user
        for user_data in test_users:
            email = user_data['email']
            username = user_data['username']
            password = user_data['password']
            
            # Generate password hash
            password_hash = generate_password_hash(password)
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if user:
                user_id = user[0]
                print(f"\nUpdating existing user: {email} (ID: {user_id})")
                
                # Update user data
                cursor.execute("""
                    UPDATE users SET 
                        username = ?,
                        password_hash = ?,
                        has_subscription = 1,
                        subscription_type = 'lifetime',
                        subscription_start = ?,
                        subscription_end = NULL,
                        is_admin = 1,
                        trial_used = 1
                    WHERE id = ?
                """, (username, password_hash, datetime.utcnow().isoformat(), user_id))
                
                print(f"- Updated username, password and subscription details")
            else:
                print(f"\nCreating new user: {email}")
                
                # Insert new user
                current_time = datetime.utcnow().isoformat()
                cursor.execute("""
                    INSERT INTO users (
                        username, email, password_hash, created_at,
                        has_subscription, subscription_type, subscription_start,
                        is_admin, trial_used
                    ) VALUES (?, ?, ?, ?, 1, 'lifetime', ?, 1, 1)
                """, (username, email, password_hash, current_time, current_time))
                
                print(f"- Created new user with username {username}")
        
        # Commit changes
        conn.commit()
        print("\nChanges committed to database")
        
        # Verify changes
        print("\n===== VERIFICATION =====")
        for user_data in test_users:
            email = user_data['email']
            cursor.execute("""
                SELECT id, username, email, password_hash, has_subscription, 
                       subscription_type, is_admin 
                FROM users WHERE email = ?
            """, (email,))
            user = cursor.fetchone()
            
            if user:
                user_id, db_username, db_email, pwd_hash, has_sub, sub_type, is_admin = user
                print(f"\nUser: {db_email}")
                print(f"- ID: {user_id}")
                print(f"- Username: {db_username}")
                print(f"- Has password hash: {'Yes' if pwd_hash else 'No'}")
                print(f"- Has subscription: {'Yes' if has_sub else 'No'}")
                print(f"- Subscription type: {sub_type}")
                print(f"- Is admin: {'Yes' if is_admin else 'No'}")
            else:
                print(f"\nUser not found: {email} - Something went wrong!")
                return False
        
        return True
    
    except Exception as e:
        print(f"Error fixing test users: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Close connection
        if 'conn' in locals():
            conn.close()
            print("\nDatabase connection closed")

if __name__ == "__main__":
    print("\n===== COMPREHENSIVE TEST USER FIX =====")
    
    # Find database
    db_path = find_database_file()
    
    if db_path:
        # Fix test users
        success = fix_test_users(db_path)
        
        if success:
            print("\n✅ TEST USER FIX COMPLETED SUCCESSFULLY!")
            print("\nTest User Credentials:")
            print("1. Email: test@aksjeradar.trade")
            print("   Username: testuser")
            print("   Password: aksjeradar2024")
            print("\n2. Email: investor@aksjeradar.trade")
            print("   Username: investor")
            print("   Password: aksjeradar2024")
            print("\nPlease restart the Flask server before trying to login again.")
        else:
            print("\n❌ TEST USER FIX FAILED!")
    else:
        print("\n❌ DATABASE NOT FOUND!")
        sys.exit(1)
