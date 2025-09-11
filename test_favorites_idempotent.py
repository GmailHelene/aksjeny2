import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from flask import url_for

@pytest.fixture
def app_instance():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # Create user
        user = User(email='favtest@example.com', username='favtest', password='testpass')
        db.session.add(user)
        db.session.commit()
    yield app

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

@pytest.fixture
def auth_client(client, app_instance):
    with app_instance.app_context():
        # Login by setting session directly (simpler for test)
        with client.session_transaction() as sess:
            user = User.query.filter_by(email='favtest@example.com').first()
            sess['_user_id'] = str(user.id)
    return client

def test_favorites_add_idempotent(auth_client):
    # First add
    res1 = auth_client.post('/stocks/api/favorites/add', json={'symbol': 'EQNR.OL'}, headers={'X-CSRFToken':'test'})
    data1 = res1.get_json()
    assert data1['success'] and data1['favorited']
    # Second add (idempotent)
    res2 = auth_client.post('/stocks/api/favorites/add', json={'symbol': 'EQNR.OL'}, headers={'X-CSRFToken':'test'})
    data2 = res2.get_json()
    assert data2['success'] and data2['favorited']
    # Correlation ID present (may be None in test, but key should exist if middleware runs)
    assert 'favorite' in data2 and data2['favorite'] is True


def test_favorites_remove_idempotent(auth_client):
    # Ensure symbol not in favorites initially
    auth_client.post('/stocks/api/favorites/remove', json={'symbol': 'DNB.OL'}, headers={'X-CSRFToken':'test'})
    # First remove (idempotent when absent)
    res1 = auth_client.post('/stocks/api/favorites/remove', json={'symbol': 'DNB.OL'}, headers={'X-CSRFToken':'test'})
    data1 = res1.get_json()
    assert data1['success'] and data1['favorited'] is False
    # Add then remove
    auth_client.post('/stocks/api/favorites/add', json={'symbol': 'DNB.OL'}, headers={'X-CSRFToken':'test'})
    res2 = auth_client.post('/stocks/api/favorites/remove', json={'symbol': 'DNB.OL'}, headers={'X-CSRFToken':'test'})
    data2 = res2.get_json()
    assert data2['success'] and data2['favorited'] is False


def test_favorites_toggle(auth_client):
    # Toggle add
    res1 = auth_client.post('/stocks/api/favorites/toggle/EQNR.OL', headers={'X-CSRFToken':'test'})
    data1 = res1.get_json()
    assert data1['success'] and data1['favorited'] is True
    # Toggle remove
    res2 = auth_client.post('/stocks/api/favorites/toggle/EQNR.OL', headers={'X-CSRFToken':'test'})
    data2 = res2.get_json()
    assert data2['success'] and data2['favorited'] is False
    # Toggle add again
    res3 = auth_client.post('/stocks/api/favorites/toggle/EQNR.OL', headers={'X-CSRFToken':'test'})
    data3 = res3.get_json()
    assert data3['success'] and data3['favorited'] is True
