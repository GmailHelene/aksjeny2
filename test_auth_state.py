#!/usr/bin/env python3
"""
Test script to deeply debug Flask-Login authentication state
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User
from flask import session
from flask_login import current_user

def test_authentication_state():
    """Simplified stable auth state test (original was an ad-hoc debug script).
    Ensures a user can be created, logged in, and current_user is authenticated.
    """
    app = create_app('testing')

    # Register diagnostic route BEFORE any requests (avoids setup finished error)
    @app.route('/test-auth-state')
    def _test_auth_state_route():  # pragma: no cover - simple diagnostic
        return 'OK'

    with app.test_client() as client, app.app_context():
        # Ensure user exists (create if missing)
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            user = User(email='test@example.com', username='testuser', password='testpassword')
            from app.extensions import db
            db.session.add(user)
            db.session.commit()

        # Initial session empty
        with client.session_transaction() as sess:
            assert '_user_id' not in sess

        # Perform login (form based)
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        resp = client.post('/auth/login', data=login_data, follow_redirects=False)
        assert resp.status_code in (302, 303, 200)

        # Session should now contain user id
        with client.session_transaction() as sess:
            assert '_user_id' in sess

        # Trigger request to load current_user
        client.get('/')
        assert current_user.is_authenticated

        # Diagnostic route reachable
        diag = client.get('/test-auth-state')
        assert diag.status_code == 200

if __name__ == '__main__':
    test_authentication_state()
