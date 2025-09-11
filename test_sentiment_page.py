import re
import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def app_instance():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        u = User(email='sent@test.com', username='sentuser', password='pw')
        db.session.add(u)
        db.session.commit()
    yield app

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

@pytest.fixture
def auth_client(client, app_instance):
    with app_instance.app_context():
        user = User.query.filter_by(email='sent@test.com').first()
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
    return client

def test_sentiment_page_basic(auth_client):
    r = auth_client.get('/analysis/sentiment?symbol=EQNR.OL')
    assert r.status_code == 200
    text = r.get_data(as_text=True)
    assert 'EQNR.OL' in text
    assert 'Correlation ID:' in text  # Ensure correlation ID rendered
    # Extract correlation id pattern (hex)
    m = re.search(r'Correlation ID:\s*([0-9a-fA-F]{32})', text)
    assert m, 'Correlation ID not found or wrong format'
