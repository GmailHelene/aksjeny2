"""
Initialize database and create missing tables
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)

class Achievement(db.Model):
    """Achievement definitions"""
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

class UserAchievement(db.Model):
    """User achievements tracking"""
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    earned_at = db.Column(db.DateTime)
    progress = db.Column(db.Integer, default=1)

class UserStats(db.Model):
    """User activity statistics for achievements"""
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Trading/Analysis stats
    predictions_made = db.Column(db.Integer, default=0)
    successful_predictions = db.Column(db.Integer, default=0)
    stocks_analyzed = db.Column(db.Integer, default=0)
    portfolios_created = db.Column(db.Integer, default=0)
    
    # Platform engagement
    total_logins = db.Column(db.Integer, default=0)
    consecutive_login_days = db.Column(db.Integer, default=0)
    last_login_date = db.Column(db.Date)
    forum_posts = db.Column(db.Integer, default=0)
    favorites_added = db.Column(db.Integer, default=0)
    
    # Points and level
    total_points = db.Column(db.Integer, default=0)
    current_level = db.Column(db.Integer, default=1)

# Create tables
if __name__ == '__main__':
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")
    
    # List all tables
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print("\nCreated tables:")
    for table in tables:
        print(f"- {table}")
