import pytest
from app import create_app
from app.extensions import db

@pytest.fixture(scope="session")
def app_instance():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass
        yield app

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

def test_live(client):
    r = client.get('/health/live')
    assert r.status_code == 200
    assert r.is_json
    assert r.json.get('alive') is True or r.json.get('status') == 'ok'


def test_ready(client):
    r = client.get('/health/ready')
    assert r.status_code == 200
    assert r.is_json
    assert r.json.get('status') in ['ready', 'degraded']
