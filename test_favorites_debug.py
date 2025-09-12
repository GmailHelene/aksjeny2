#!/usr/bin/env python3
"""Deterministic favorites loading test (refactored)."""
import re
from app import create_app, db
from app.models import User, Favorites


def _seed_user_with_favorites():
    user = User.query.filter_by(email='test@example.com').first()
    if not user:
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
    # Ensure a couple favorites
    existing = Favorites.query.filter_by(user_id=user.id).count()
    if existing < 2:
        Favorites.add_favorite(user.id, 'AAPL', name='Apple Inc', exchange='NASDAQ')
        Favorites.add_favorite(user.id, 'EQNR.OL', name='Equinor ASA', exchange='OSLO')
    return user


def test_favorites_loading_debug():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        user = _seed_user_with_favorites()
        with app.test_client() as client:
            # Login (session injection)
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
            # Request profile
            resp = client.get('/profile/')
            assert resp.status_code in (200, 302)
            # If redirect (likely to login), follow once
            if resp.status_code == 302 and 'login' in resp.location:
                resp = client.get(resp.location)
            # Fetch favorites via ORM
            favorites = Favorites.get_user_favorites(user.id)
            assert len(favorites) >= 2, 'Expected at least two favorites' 
            # Confirm symbols appear in page if status 200
            if resp.status_code == 200:
                text = resp.get_data(as_text=True)
                # Basic sanity: at least one favorite symbol should appear
                assert any(fav.symbol in text for fav in favorites), 'Favorite symbols not rendered in profile page'

if __name__ == '__main__':  # manual execution support
    test_favorites_loading_debug()
