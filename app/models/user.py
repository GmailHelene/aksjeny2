from ..extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import text

# Import backup column handling
try:
    from .backup_columns import add_missing_column_properties
    add_missing_column_properties()
except:
    pass  # Fail silently if backup not available

class DeviceTrialTracker(db.Model):
    """Track trial usage per device to prevent abuse by clearing cookies"""
    __tablename__ = 'device_trial_tracker'
    
    id = db.Column(db.Integer, primary_key=True)
    device_fingerprint = db.Column(db.String(32), unique=True, index=True, nullable=False)
    trial_start_time = db.Column(db.DateTime, default=datetime.utcnow)
    trial_used = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DeviceTrialTracker {self.device_fingerprint}>'
    
    def trial_expired(self):
        """Check if trial period has expired - Always returns False as trials are permanently disabled"""
        return False

class User(UserMixin, db.Model):
    @property
    def is_premium(self):
        """Return True if user has an active paid subscription"""
        if not self.has_subscription:
            return False
        if self.subscription_type in ['monthly', 'yearly', 'lifetime']:
            if self.subscription_type == 'lifetime':
                return True
            if self.subscription_end:
                return datetime.utcnow() <= self.subscription_end
        return False
    __tablename__ = 'users'  # <-- Viktig!
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - using backref instead of back_populates to avoid conflicts
    portfolios = db.relationship('Portfolio', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    watchlists = db.relationship('Watchlist', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    # Subscription fields
    has_subscription = db.Column(db.Boolean, default=False)
    subscription_type = db.Column(db.String(20), default='free')  # 'free', 'monthly', 'yearly', 'lifetime'
    subscription_start = db.Column(db.DateTime, nullable=True)
    subscription_end = db.Column(db.DateTime, nullable=True)
    trial_used = db.Column(db.Boolean, default=False)
    trial_start = db.Column(db.DateTime, nullable=True)
    stripe_customer_id = db.Column(db.String(128), nullable=True)  # For å lagre Stripe Customer ID
    reports_used_this_month = db.Column(db.Integer, default=0)  # Track consultant report usage
    last_reset_date = db.Column(db.DateTime, default=datetime.utcnow)  # Track monthly reset
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag
    
    # Password reset fields
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)  # Added missing column
    
    # Internationalization and settings
    language = db.Column(db.String(10), default='no')  # Language preference (no, en, etc.)
    notification_settings = db.Column(db.Text, nullable=True)  # JSON string for notification preferences
    
    # User notification preferences
    email_notifications = db.Column(db.Boolean, default=True, nullable=True)
    price_alerts = db.Column(db.Boolean, default=True, nullable=True)
    market_news = db.Column(db.Boolean, default=True, nullable=True)
    
    # Extended notification preferences  
    email_notifications_enabled = db.Column(db.Boolean, default=True, nullable=True)
    price_alerts_enabled = db.Column(db.Boolean, default=True, nullable=True)
    market_news_enabled = db.Column(db.Boolean, default=True, nullable=True)
    portfolio_updates_enabled = db.Column(db.Boolean, default=True, nullable=True)
    ai_insights_enabled = db.Column(db.Boolean, default=True, nullable=True)
    weekly_reports_enabled = db.Column(db.Boolean, default=True, nullable=True)
    
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    
    # Enhanced authentication fields
    two_factor_enabled = db.Column(db.Boolean, default=False, nullable=False)
    two_factor_secret = db.Column(db.String(32), nullable=True)
    email_verified = db.Column(db.Boolean, default=True, nullable=False)  # Default to True for existing users
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, default=0, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def __getattribute__(self, name):
        """Handle missing database columns gracefully with comprehensive fallbacks"""
        try:
            return super().__getattribute__(name)
        except AttributeError:
            # Provide fallback values for missing columns
            fallback_values = {
                # Basic user info
                'username': 'Guest',
                'email': None,
                'first_name': None,
                'last_name': None,
                
                # Authentication
                'reset_token': None,
                'reset_token_expires': None,
                'two_factor_enabled': False,
                'two_factor_secret': None,
                'email_verified': True,
                'is_locked': False,
                'last_login': datetime.utcnow(),
                'login_count': 0,
                
                # Subscription
                'has_subscription': False,
                'subscription_type': 'free',
                'subscription_start': None,
                'subscription_end': None,
                'trial_used': False,
                'trial_start': None,
                'stripe_customer_id': None,
                'reports_used_this_month': 0,
                'last_reset_date': datetime.utcnow(),
                'is_admin': False,
                
                # Preferences
                'language': 'no',
                'notification_settings': None,
                'email_notifications': True,
                'price_alerts': True,
                'market_news': True,
                'email_notifications_enabled': True,
                'price_alerts_enabled': True,
                'market_news_enabled': True,
                'portfolio_updates_enabled': True,
                'ai_insights_enabled': True,
                'weekly_reports_enabled': True,
                'email_notifications_enabled': True,
                'price_alerts_enabled': True,
                'market_news_enabled': True,
                'portfolio_updates_enabled': True,
                'ai_insights_enabled': True,
                'weekly_reports_enabled': True,
                'email_notifications': True,
                'price_alerts': True,
                'market_news': True,
                'email_notifications': True,
                'price_alerts': True,
                'market_news': True,
                'email_notifications_enabled': True,
                'price_alerts_enabled': True,
                'market_news_enabled': True,
                'portfolio_updates_enabled': True,
                'ai_insights_enabled': True,
                'weekly_reports_enabled': True,
                'first_name': None,
                'last_name': None,
                'two_factor_enabled': False,
                'two_factor_secret': None,
                'email_verified': True,
                'is_locked': False,
                'last_login': None,
                'login_count': 0,
                'reports_used_this_month': 0,
                'last_reset_date': datetime.utcnow(),
                'is_admin': False
            }
            
            if name in fallback_values:
                return fallback_values[name]
            
            # Re-raise the AttributeError for non-fallback attributes
            raise

    def has_subscription_level(self, required_level: str) -> bool:
        """Check if user has required subscription level"""
        levels = ['free', 'basic', 'premium', 'enterprise']
        try:
            current_level = getattr(self, 'subscription_level', 'free')
            user_level_index = levels.index(current_level)
            required_level_index = levels.index(required_level)
            return user_level_index >= required_level_index
        except (ValueError, AttributeError):
            return False
    
    def set_password(self, password):
        """Set password hash"""
        if not hasattr(self, 'password_hash'):
            # Add password_hash field if it doesn't exist
            self.password_hash = None
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        if not hasattr(self, 'password_hash') or not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def start_free_trial(self):
        """Start the free trial for this user"""
        if not self.trial_used:
            self.trial_used = True
            self.trial_start = datetime.utcnow()
            return True
        return False
    
    def is_in_trial_period(self):
        """Check if the user is in their free trial period - Always returns True as trials are permanently disabled"""
        return True
    
    def has_active_subscription(self):
        """Check if the user has an active subscription"""
        # If user has a subscription and it's not expired
        if self.has_subscription and self.subscription_end:
            return datetime.utcnow() <= self.subscription_end
        
        # Or if they have a lifetime subscription
        if self.has_subscription and self.subscription_type == 'lifetime':
            return True
        
        # Or if they're in trial period
        return self.is_in_trial_period()
    
    def subscription_days_left(self):
        """Return the number of days left in the subscription"""
        if not self.has_subscription or not self.subscription_end:
            return 0
        
        delta = self.subscription_end - datetime.utcnow()
        return max(0, delta.days)
    
    def get_referral_code(self):
        """Get or create a referral code for this user"""
        from ..models.referral import Referral
        
        # Check if user already has a referral code
        existing_referral = Referral.query.filter_by(referrer_id=self.id).first()
        
    def update_notification_settings(self, settings):
        """Update notification settings for the user"""
        try:
            # Update notification settings JSON
            if isinstance(settings, dict):
                import json
                self.notification_settings = json.dumps(settings)
            
            # Update individual boolean columns if provided
            boolean_fields = [
                'email_notifications_enabled',
                'price_alerts_enabled',
                'market_news_enabled',
                'portfolio_updates_enabled',
                'ai_insights_enabled',
                'weekly_reports_enabled',
                'email_notifications',
                'price_alerts',
                'market_news'
            ]
            
            for field in boolean_fields:
                if field in settings:
                    value = settings[field]
                    if isinstance(value, str):
                        value = value.lower() == 'true'
                    setattr(self, field, bool(value))
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating notification settings: {e}")
            return False
        if existing_referral:
            return existing_referral.referral_code
        
        # Create new referral code
        new_referral = Referral(
            referrer_id=self.id,
            referral_code=Referral.generate_referral_code()
        )
        db.session.add(new_referral)
        db.session.commit()
        return new_referral.referral_code
    
    def get_completed_referrals_count(self):
        """Get number of successful referrals"""
        from ..models.referral import Referral
        return Referral.query.filter_by(referrer_id=self.id, is_completed=True).count()
    
    def get_available_referral_discounts(self):
        """Get available referral discounts for this user"""
        from ..models.referral import ReferralDiscount
        return ReferralDiscount.query.filter_by(
            user_id=self.id, 
            is_used=False
        ).all()
    
    def has_referral_discount(self):
        """Check if user has any available referral discounts"""
        discounts = self.get_available_referral_discounts()
        return len([d for d in discounts if d.is_valid()]) > 0

    def generate_reset_token(self):
        """Generate a unique reset token and set its expiry to 24 hours from now"""
        import secrets
        from datetime import datetime, timedelta
        
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=24)
        db.session.commit()
        return self.reset_token

    def validate_reset_token(self, token):
        """Check if the token is valid and not expired"""
        if not self.reset_token or not self.reset_token_expires:
            return False
        
        if token != self.reset_token:
            return False
        
        if datetime.utcnow() > self.reset_token_expires:
            return False
        
        return True

    def clear_reset_token(self):
        """Clear the reset token after use"""
        self.reset_token = None
        self.reset_token_expires = None
        db.session.commit()

    @property
    def subscription_status(self):
        """Get subscription status for display"""
        if self.has_subscription:
            if self.subscription_type == 'lifetime':
                return 'lifetime'
            elif self.has_active_subscription():
                return 'premium'
            else:
                return 'expired'
        elif self.is_in_trial_period():
            return 'trial'
        else:
            return 'free'

    def get_notification_settings(self):
        """Get notification settings as dictionary"""
        import json
        if self.notification_settings:
            try:
                return json.loads(self.notification_settings)
            except (json.JSONDecodeError, TypeError):
                # Return default settings if JSON is invalid
                return self._get_default_notification_settings()
        return self._get_default_notification_settings()
    
    def _get_default_notification_settings(self):
        """Get default notification settings"""
        return {
            'email_enabled': getattr(self, 'email_notifications', True),
            'push_enabled': False,
            'inapp_enabled': True,
            'email_price_alerts': getattr(self, 'price_alerts', True),
            'email_market_news': getattr(self, 'market_news', True),
            'push_price_alerts': False,
            'push_market_news': False,
            'inapp_price_alerts': True,
            'inapp_market_news': True,
            'daily_summary': False,
            'quiet_hours_enabled': False,
            'quiet_hours_start': '22:00',
            'quiet_hours_end': '08:00',
            'timezone': 'Europe/Oslo'
        }

    def update_notification_settings(self, settings_dict):
        """Update notification settings from dictionary"""
        import json
        try:
            # Convert all boolean values to actual booleans
            for key in settings_dict:
                if isinstance(settings_dict[key], str) and settings_dict[key].lower() in ['true', 'false']:
                    settings_dict[key] = settings_dict[key].lower() == 'true'
                    
            # Update the notification_settings attribute
            self.notification_settings = json.dumps(settings_dict)
            
            # Also update legacy attributes for backwards compatibility
            if 'email_enabled' in settings_dict:
                self.email_notifications = bool(settings_dict['email_enabled'])
            if 'email_price_alerts' in settings_dict:
                self.price_alerts = bool(settings_dict['email_price_alerts'])
            if 'email_market_news' in settings_dict:
                self.market_news = bool(settings_dict['email_market_news'])
                
            db.session.add(self)
            return True
        except Exception as e:
            import logging
            logging.error(f"Error updating notification settings: {e}")
            return False

    def get_language(self):
        """Get user's preferred language"""
        return self.language or 'no'

    def set_language(self, language_code):
        """Set user's preferred language"""
        # Validate language code
        valid_languages = ['no', 'en', 'da', 'sv']  # Norwegian, English, Danish, Swedish
        if language_code in valid_languages:
            self.language = language_code
            db.session.commit()
            return True
        return False

# NOTE: Portfolio and Watchlist relationships are defined in the models themselves
# No need to import them here as SQLAlchemy will resolve relationships automatically

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login with error handling"""
    try:
        # Use a simple query first to avoid column errors
        user = db.session.execute(
            text("SELECT id, username, email, password_hash, has_subscription FROM users WHERE id = :user_id"),
            {'user_id': int(user_id)}
        ).fetchone()
        
        if user:
            # Create a minimal user object
            user_obj = User()
            user_obj.id = user[0]
            user_obj.username = user[1] 
            user_obj.email = user[2]
            user_obj.password_hash = user[3]
            user_obj.has_subscription = user[4] if user[4] is not None else False
            
            # Set safe defaults for other fields
            user_obj.subscription_type = 'free'
            user_obj.is_admin = False
            user_obj.email_verified = True
            
            return user_obj
        return None
    except Exception as e:
        print(f"Error loading user {user_id}: {e}")
        return None

# Database table creation is handled in main.py and app initialization
# No need to create tables at import time