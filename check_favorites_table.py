#!/usr/bin/env python3
"""Simple database checker for favorites table"""

import sqlite3
import os

# Assuming SQLite database
db_path = "/workspaces/aksjeny/app/app.db"

if os.path.exists(db_path):
    print(f"Database found at: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")
        
        # Check if favorites table exists
        if ('favorites',) in tables:
            print("✅ Favorites table exists!")
            cursor.execute("SELECT * FROM favorites LIMIT 5;")
            favorites = cursor.fetchall()
            print(f"Sample favorites: {favorites}")
        else:
            print("❌ Favorites table does not exist!")
            
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")
else:
    print(f"Database not found at: {db_path}")
    # Try instance directory
    instance_db_path = "/workspaces/aksjeny/instance/app.db"
    if os.path.exists(instance_db_path):
        print(f"Found database in instance directory: {instance_db_path}")
    else:
        print("No database found")
