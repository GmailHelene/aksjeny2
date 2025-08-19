"""Password Reset Handler for managing password reset requests"""

import os
import jwt
import sqlite3
import psycopg2
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

class PasswordResetHandler:
    """Handles password reset functionality"""
    
    def __init__(self):
        """Initialize with database connection"""
        self.db_url = os.getenv('DATABASE_URL')
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
        
    def _get_connection(self):
        """Get appropriate database connection"""
        if self.db_url.startswith('sqlite:'):
            db_path = self.db_url.replace('sqlite:///', '')
            return sqlite3.connect(db_path)
        else:
            return psycopg2.connect(self.db_url)
        
    def create_reset_request(self, email):
        """Create a password reset request"""
        try:
            # Generate reset token
            token = self._generate_reset_token(email)
            expires = datetime.utcnow() + timedelta(hours=24)
            
            # Store token in database
            conn = self._get_connection()
            
            try:
                if self.db_url.startswith('sqlite:'):
                    # SQLite version
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users 
                        SET reset_token = ?, reset_token_expires = ?
                        WHERE email = ?
                    """, (token, expires.isoformat(), email))
                    
                    if cursor.rowcount == 0:
                        return {'success': False}
                    
                    conn.commit()
                else:
                    # PostgreSQL version
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE users 
                            SET reset_token = %s, reset_token_expires = %s
                            WHERE email = %s
                            RETURNING id
                        """, (token, expires, email))
                        
                        user = cur.fetchone()
                        
                        if not user:
                            return {'success': False}
                            
                        conn.commit()
                        
            finally:
                conn.close()
                    
            return {
                'success': True,
                'token': token
            }
            
        except Exception as e:
            print(f"Error creating reset request: {e}")
            return {'success': False}
            
    def verify_reset_token(self, token):
        """Verify reset token is valid"""
        try:
            conn = self._get_connection()
            
            try:
                if self.db_url.startswith('sqlite:'):
                    # SQLite version
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT email, reset_token_expires
                        FROM users
                        WHERE reset_token = ?
                    """, (token,))
                    
                    result = cursor.fetchone()
                else:
                    # PostgreSQL version
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT email, reset_token_expires
                            FROM users
                            WHERE reset_token = %s
                        """, (token,))
                        
                        result = cur.fetchone()
                        
                if not result:
                    return {'valid': False, 'message': 'Invalid reset token - no matching token found'}
                    
                email, expires_str = result
                
                # Parse datetime for SQLite
                if self.db_url.startswith('sqlite:'):
                    expires = datetime.fromisoformat(expires_str.replace('Z', '+00:00'))
                else:
                    expires = expires_str
                
                # Check if token has expired
                if expires < datetime.utcnow():
                    return {'valid': False, 'message': 'Reset token has expired'}
                    
                return {'valid': True, 'email': email}
                
            finally:
                conn.close()
                    
        except Exception as e:
            print(f"Error verifying reset token: {e}")
            return {'valid': False, 'message': 'Invalid or expired token'}
            
    def reset_password(self, token, new_password):
        """Reset user's password with valid token"""
        try:
            # First verify token
            verify_result = self.verify_reset_token(token)
            if not verify_result['valid']:
                return {'success': False, 'message': verify_result['message']}
                
            # Hash new password    
            password_hash = generate_password_hash(new_password)
            
            conn = self._get_connection()
            
            try:
                if self.db_url.startswith('sqlite:'):
                    # SQLite version
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE users
                        SET password = ?,
                            reset_token = NULL,
                            reset_token_expires = NULL
                        WHERE reset_token = ?
                    """, (password_hash, token))
                    
                    conn.commit()
                else:
                    # PostgreSQL version
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE users
                            SET password = %s,
                                reset_token = NULL,
                                reset_token_expires = NULL
                            WHERE reset_token = %s
                        """, (password_hash, token))
                        
                        conn.commit()
                        
            finally:
                conn.close()
                    
            return {'success': True}
                    
        except Exception as e:
            print(f"Error resetting password: {e}")
            return {'success': False, 'message': 'Error resetting password'}
            
    def _generate_reset_token(self, email):
        """Generate JWT reset token"""
        try:
            payload = {
                'email': email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            return jwt.encode(payload, self.secret_key, algorithm='HS256')
            
        except Exception as e:
            print(f"Error generating reset token: {e}")
            return None
