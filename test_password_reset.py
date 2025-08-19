"""Test password reset functionality"""

import os
import jwt
import pytest
from datetime import datetime, timedelta
from password_reset_handler import PasswordResetHandler

# Test data
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "newpassword123"
TEST_TOKEN = None

@pytest.fixture
def handler(test_db):
    """Create PasswordResetHandler instance with test database"""
    os.environ['DATABASE_URL'] = test_db
    os.environ['SECRET_KEY'] = 'test-secret-key'
    return PasswordResetHandler()
    
def test_create_reset_request(handler):
    """Test creating password reset request"""
    result = handler.create_reset_request(TEST_EMAIL)
    
    assert result['success'] == True
    assert 'token' in result
    
    # Store token for next tests
    global TEST_TOKEN
    TEST_TOKEN = result['token']
    
def test_verify_reset_token(handler):
    """Test verifying reset token"""
    result = handler.verify_reset_token(TEST_TOKEN)
    
    assert result['valid'] == True
    assert result['email'] == TEST_EMAIL
    
def test_verify_expired_token(handler):
    """Test verifying expired token"""
    # Create a test user with an expired token in the database
    import sqlite3
    db_path = "/tmp/test.db"
    conn = sqlite3.connect(db_path)
    
    try:
        # Create expired token that we'll store in database
        payload = {
            'email': TEST_EMAIL,
            'exp': datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago
        }
        expired_token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        
        # Store expired token in database
        expired_time = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET reset_token = ?, reset_token_expires = ?
            WHERE email = ?
        """, (expired_token, expired_time, TEST_EMAIL))
        conn.commit()
        
        # Now test verification
        result = handler.verify_reset_token(expired_token)
        
        assert result['valid'] == False
        assert 'expired' in result['message'].lower()
        
    finally:
        conn.close()
    
def test_reset_password(handler):
    """Test resetting password"""
    # Create a fresh token for this test
    result = handler.create_reset_request(TEST_EMAIL)
    assert result['success'] == True
    fresh_token = result['token']
    
    # Now test reset
    result = handler.reset_password(fresh_token, TEST_PASSWORD)
    
    assert result['success'] == True
    
def test_reset_password_invalid_token(handler):
    """Test resetting password with invalid token"""
    result = handler.reset_password('invalid-token', TEST_PASSWORD)
    
    assert result['success'] == False
    assert 'invalid' in result['message'].lower()
    
def test_reset_password_expired_token(handler):
    """Test resetting password with expired token"""
    # Create a test user with an expired token in the database
    import sqlite3
    db_path = "/tmp/test.db"
    conn = sqlite3.connect(db_path)
    
    try:
        # Create expired token that we'll store in database
        payload = {
            'email': TEST_EMAIL,
            'exp': datetime.utcnow() - timedelta(hours=1)
        }
        expired_token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        
        # Store expired token in database
        expired_time = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET reset_token = ?, reset_token_expires = ?
            WHERE email = ?
        """, (expired_token, expired_time, TEST_EMAIL))
        conn.commit()
        
        # Now test reset
        result = handler.reset_password(expired_token, TEST_PASSWORD)
        
        assert result['success'] == False
        assert 'expired' in result['message'].lower()
        
    finally:
        conn.close()
    
def test_invalid_token_format(handler):
    """Test verifying malformed token"""
    result = handler.verify_reset_token('not-a-valid-jwt-token')
    
    assert result['valid'] == False
    assert 'invalid' in result['message'].lower()
