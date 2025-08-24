"""
Database verification script
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models
class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='bi-trophy')
    badge_color = db.Column(db.String(20), default='warning')
    points = db.Column(db.Integer, default=10)
    category = db.Column(db.String(50), default='general')
    requirement_type = db.Column(db.String(50), nullable=False)
    requirement_count = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    earned_at = db.Column(db.DateTime, server_default=db.func.now())
    progress = db.Column(db.Integer, default=1)

class UserStats(db.Model):
    __tablename__ = 'user_stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    predictions_made = db.Column(db.Integer, default=0)
    successful_predictions = db.Column(db.Integer, default=0)
    stocks_analyzed = db.Column(db.Integer, default=0)
    portfolios_created = db.Column(db.Integer, default=0)
    total_logins = db.Column(db.Integer, default=0)
    consecutive_login_days = db.Column(db.Integer, default=0)
    last_login_date = db.Column(db.Date)
    forum_posts = db.Column(db.Integer, default=0)
    favorites_added = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)
    current_level = db.Column(db.Integer, default=1)

def init_db():
    """Initialize the database"""
    try:
        # Create database file if it doesn't exist
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        
        # Create tables
        db.create_all()
        logger.info("Database tables created successfully")
        
        # Add default achievements if needed
        achievement_count = Achievement.query.count()
        if achievement_count == 0:
            # Add default achievements
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
                }
            ]
            
            for ach_data in achievements:
                achievement = Achievement(**ach_data)
                db.session.add(achievement)
            db.session.commit()
            logger.info("Default achievements added")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == '__main__':
    with app.app_context():
        init_db()
