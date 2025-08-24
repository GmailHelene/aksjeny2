"""Setup database with Flask-Migrate

Run this script to:
1. Create the database tables if they don't exist
2. Create and apply migrations for any missing tables
3. Initialize achievement system
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.models.achievements import Achievement, UserAchievement, UserStats

def setup_database():
    """Create and setup the database"""
    # Create Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    # Import models
    from app.models.user import User
    from app.models.portfolio import Portfolio, PortfolioStock
    from app.models.watchlist import Watchlist, WatchlistStock
    from app.models.notifications import (
        Notification, PriceAlert, NotificationSettings,
        AIModel, PredictionLog
    )
    from app.models.achievements import (
        Achievement, UserAchievement, UserStats
    )
    
    with app.app_context():
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Get list of tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print("Created tables:", ", ".join(tables))
        
        # Initialize achievements if needed
        if 'achievements' in tables and Achievement.query.count() == 0:
            print("\nInitializing default achievements...")
            achievements = [
                {
                    'name': 'Første innlogging',
                    'description': 'Velkommen til Aksjeradar!',
                    'icon': 'bi-door-open',
                    'badge_color': 'success',
                    'points': 10,
                    'category': 'general',
                    'requirement_type': 'logins',
                    'requirement_count': 1
                },
                {
                    'name': 'Trofas bruker',
                    'description': 'Logget inn 7 dager på rad',
                    'icon': 'bi-calendar-check',
                    'badge_color': 'primary',
                    'points': 50,
                    'category': 'general',
                    'requirement_type': 'consecutive_logins',
                    'requirement_count': 7
                },
                {
                    'name': 'Aksje-entusiast',
                    'description': 'Lagt til 10 aksjer i favoritter',
                    'icon': 'bi-star-fill',
                    'badge_color': 'warning',
                    'points': 25,
                    'category': 'trading',
                    'requirement_type': 'favorites',
                    'requirement_count': 10
                },
                {
                    'name': 'Portefølje-mester',
                    'description': 'Opprettet din første portefølje',
                    'icon': 'bi-briefcase-fill',
                    'badge_color': 'info',
                    'points': 30,
                    'category': 'trading',
                    'requirement_type': 'portfolios',
                    'requirement_count': 1
                },
                {
                    'name': 'Analysator',
                    'description': 'Analysert 50 forskjellige aksjer',
                    'icon': 'bi-graph-up',
                    'badge_color': 'danger',
                    'points': 75,
                    'category': 'analysis',
                    'requirement_type': 'stocks_analyzed',
                    'requirement_count': 50
                }
            ]
            
            for ach_data in achievements:
                achievement = Achievement(**ach_data)
                db.session.add(achievement)
            
            db.session.commit()
            print(f"Added {len(achievements)} default achievements")
        
        # Create user_stats records for any users without them
        print("\nChecking user stats...")
        users = User.query.all()
        created_count = 0
        for user in users:
            stats = UserStats.query.filter_by(user_id=user.id).first()
            if not stats:
                stats = UserStats(user_id=user.id)
                db.session.add(stats)
                created_count += 1
        
        if created_count > 0:
            db.session.commit()
            print(f"Created missing user_stats records for {created_count} users")
        
        print("\nDatabase setup complete!")

if __name__ == '__main__':
    setup_database()
