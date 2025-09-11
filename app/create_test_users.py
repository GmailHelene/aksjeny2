from app import create_app
from app.extensions import db
from app.models.user import User
from datetime import datetime, timedelta

def create_test_users():
    app = create_app()
    with app.app_context():
    # Rydd opp gamle test-brukere (trial / expired) hvis de finnes
    User.query.filter(User.email.in_(['trial@example.com', 'expired@example.com'])).delete()
        
        # Opprett eller oppdater admin bruker
        admin = User.query.filter_by(email='helene721@gmail.com').first()
        if not admin:
            admin = User(
                username='helene721@gmail.com',
                email='helene721@gmail.com',
                has_subscription=True,
                subscription_type='lifetime',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        else:
            # Oppdater eksisterende admin bruker
            admin.has_subscription = True
            admin.subscription_type = 'lifetime'
            admin.is_admin = True
            admin.set_password('admin123')
        
        # Opprett / oppdater trial bruker
        trial_user = User.query.filter_by(email='trial@example.com').first()
        if not trial_user:
            trial_user = User(
                username='trial_user',
                email='trial@example.com',
                trial_used=True,
                trial_start=datetime.utcnow()
            )
            trial_user.set_password('trial123')
            db.session.add(trial_user)
        else:
            trial_user.trial_used = True
            trial_user.trial_start = datetime.utcnow()
            trial_user.set_password('trial123')
        
        # Opprett / oppdater expired (utløpt) bruker
        expired_user = User.query.filter_by(email='expired@example.com').first()
        if not expired_user:
            expired_user = User(
                username='expired_user',
                email='expired@example.com',
                trial_used=True,
                trial_start=datetime.utcnow() - timedelta(days=11)
            )
            expired_user.set_password('expired123')
            db.session.add(expired_user)
        else:
            expired_user.trial_used = True
            expired_user.trial_start = datetime.utcnow() - timedelta(days=11)
            expired_user.set_password('expired123')
        
        db.session.commit()
        print("Test users created successfully!")

if __name__ == '__main__':
    create_test_users()
