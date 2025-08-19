"""Test fixtures and setup for password reset tests using SQLite"""

import os
import pytest
import sqlite3
from datetime import datetime

@pytest.fixture(scope="session")
def test_db():
    """Create test database and tables"""
    db_path = "/tmp/test.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create new database and tables
    conn = sqlite3.connect(db_path)
    try:
        with conn:
            # Create users table
            conn.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    reset_token TEXT,
                    reset_token_expires TIMESTAMP
                )
            """)
            
            # Add test user
            conn.execute("""
                INSERT INTO users (email, password)
                VALUES (?, ?)
            """, ('test@example.com', 'testpassword'))
            
    finally:
        conn.close()
        
    return f"sqlite:///{db_path}"
