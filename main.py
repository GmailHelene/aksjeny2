"""
Migration: Add reset token columns to users table
Date: 2025-01-21
"""

# SQL migrations to execute
MIGRATIONS = [
    # Ensure the reset_token column exists in the users table
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR;",
    
    # Ensure the reset_token_expires column exists in the users table  
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP;"
]

def up():
    """Apply the migration"""
    return MIGRATIONS

def down():
    """Rollback the migration"""
    return [
        "ALTER TABLE users DROP COLUMN IF EXISTS reset_token;",
        "ALTER TABLE users DROP COLUMN IF EXISTS reset_token_expires;"
    ]



# --- NEW ENTRYPOINT LOGIC ---
import os
from app import create_app

if __name__ == '__main__':
    os.environ.setdefault('EMAIL_USERNAME', 'support@luxushair.com')
    os.environ.setdefault('EMAIL_PASSWORD', 'suetozoydejwntii')
    os.environ.setdefault('EMAIL_PORT', '587')
    os.environ.setdefault('EMAIL_SERVER', 'imap.gmail.com')
    os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

    print("Starting Flask app...")
    print("Access forgot password at: http://localhost:5002/forgot-password")
    print("Access reset password with token from email")
    print("\nServer starting...")

    port = int(os.environ.get('PORT', 5002))
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=port)