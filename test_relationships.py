from app import create_app
from app.models.user import User
from app.models.favorites import Favorites

app = create_app()

with app.app_context():
    print('User-Favorites relationship test:')
    user = User.query.first()
    print(f'First user: {user.id if user else None}')
    if user:
        print(f'User favorites count: {user.favorites.count() if hasattr(user, "favorites") else "No favorites attribute"}')
