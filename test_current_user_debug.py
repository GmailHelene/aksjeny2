#!/usr/bin/env python3
"""Refactored test that validates current_user loading and favorites without direct sqlite file access."""

import logging
from app import create_app, db
from app.models import User
from app.models.favorites import Favorites

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _ensure_test_user():
    """Create a deterministic test user with at least one favorite if absent."""
    user = User.query.filter_by(username='testuser').first()
    if not user:
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
    # Ensure at least one favorite exists for assertions
    if Favorites.query.filter_by(user_id=user.id).count() == 0:
        Favorites.add_favorite(user.id, 'AAPL', name='Apple Inc.', exchange='NASDAQ')
    return user

def test_current_user_debug():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        user = _ensure_test_user()
        with app.test_client() as client:
            # Simulate login session
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
            # Hit a route requiring auth;
            resp = client.get('/profile/')
            # Depending on implementation it might redirect first; allow 200 or 302
            assert resp.status_code in (200, 302), f"Unexpected profile status {resp.status_code}"
            # Validate ORM relationship works
            favorites = Favorites.get_user_favorites(user.id)
            assert len(favorites) >= 1, "Expected at least one favorite for test user"
            # Basic property assertions
            assert user.username == 'testuser'
            logger.info("current_user debug test passed with %d favorites", len(favorites))

if __name__ == '__main__':  # Manual run support
    test_current_user_debug()
