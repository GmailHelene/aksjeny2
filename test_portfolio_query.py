from main import create_app
from app.models.portfolio import Portfolio
from flask_login import login_user
from app.models.user import User

app = create_app()

# Opprett en testbruker
with app.app_context():
    test_user = User.query.filter_by(id=1).first()
    if test_user:
        login_user(test_user)

    portfolios = Portfolio.query.filter_by(user_id=1).all()
    print(f"Portfolios for user_id=1: {portfolios}")

    # Test `/portfolio/overview`
    with app.test_client() as client:
        response = client.get('/portfolio/overview')
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data.decode('utf-8')}")
