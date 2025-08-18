from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, make_response, jsonify, send_from_directory, g
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import text
from ..models import User
from ..models.favorites import Favorites
from ..extensions import db
from ..utils.market_open import is_market_open, is_oslo_bors_open
from ..utils.access_control import access_required
from ..services.dashboard_service import DashboardService
import logging
import logging
import hashlib
import time
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
import hashlib
import time
import os

# Import performance optimizations
try:
    from ..services.simple_cache import simple_cache
except ImportError:
    # Fallback if cache not available
    class DummyCache:
        def get(self, key, cache_type='default'): return None
        def set(self, key, value, cache_type='default'): pass
    simple_cache = DummyCache()

# Import column fallbacks for database compatibility
try:
    from ..utils.column_fallbacks import apply_column_fallbacks
    apply_column_fallbacks()
except ImportError:
    pass  # Fallbacks not available

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

def get_time_ago(dt):
    """Helper function to get human-readable time ago"""
    if not dt:
        return "Ukjent tid"
    
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 7:
        return f"{diff.days} dager siden"
    elif diff.days > 0:
        return f"{diff.days} dag{'er' if diff.days > 1 else ''} siden"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} time{'r' if hours > 1 else ''} siden"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutt{'er' if minutes > 1 else ''} siden"
    else:
        return "Nå nettopp"

from werkzeug.security import check_password_hash
from ..extensions import db, login_manager

def has_active_subscription():
    """Check if current user has active subscription"""
    if not current_user.is_authenticated:
        return False
    
    try:
        # Check exempt users first
        if hasattr(current_user, 'email') and current_user.email in EXEMPT_EMAILS:
            return True
            
        # Check subscription status
        if hasattr(current_user, 'has_active_subscription'):
            return current_user.has_active_subscription()
            
        # Fallback check
        if hasattr(current_user, 'subscription_type') and current_user.subscription_type:
            return current_user.subscription_type in ['premium', 'pro', 'yearly', 'lifetime']
            
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        
    return False
from ..utils.subscription import subscription_required
from ..utils.access_control import access_required
from ..utils.access_control import access_required, demo_access, is_demo_user, is_trial_active, api_login_required
from ..utils.i18n_simple import set_language, get_available_languages
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta, time as dt_time
import time
import os
import hashlib
from flask import g
from itsdangerous import URLSafeTimedSerializer
from flask_mailman import EmailMessage
from ..extensions import mail
from flask_wtf.csrf import CSRFProtect

# Lazy imports - only import when needed
def get_user_model():
    """Lazily import and return the User model."""
    from ..models.user import User
    return User

def get_data_service():
    """Lazily import and return the DataService class with error handling."""
    try:
        from ..services.data_service import DataService
        return DataService
    except ImportError as e:
        logger.warning(f"DataService not available: {e}")
        # Return a mock service for fallback
        class MockDataService:
            @staticmethod
            def get_oslo_stocks():
                return {}
            @staticmethod
            def get_global_stocks():
                return {}
            @staticmethod
            def get_crypto_data():
                return {}
            @staticmethod
            def get_currency_overview():
                return {}
        return MockDataService

def get_referral_service():
    """Lazily import and return the ReferralService class."""
    from ..services.referral_service import ReferralService
    return ReferralService

def get_forms():
    """Lazily import and return all forms used in this module."""
    from ..forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm, ReferralForm
    return LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm, ReferralForm

def get_performance_monitor():
    """Lazily import and return the performance monitor decorator."""
    try:
        from ..services.performance_monitor import monitor_performance
        return monitor_performance
    except ImportError:
        # Return a dummy decorator if performance monitor is not available
        def dummy_decorator(f):
            return f
        return dummy_decorator

# Lazy import stripe only when needed
def get_stripe():
    """Lazily import and return the Stripe module with error handling."""
    try:
        import stripe
        # Ensure API key is set
        if not stripe.api_key:
            stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
            if not stripe.api_key:
                current_app.logger.warning("No Stripe API key configured")
                return None
        return stripe
    except ImportError:
        current_app.logger.warning("Stripe not available - import failed")
        return None
    except Exception as e:
        current_app.logger.warning(f"Stripe setup failed: {e}")
        return None

def get_pytz():
    """Lazily import and return the pytz module."""
    try:
        import pytz
        return pytz
    except ImportError:
        current_app.logger.warning("pytz not available - import failed")
        return None

main = Blueprint('main', __name__)

EXEMPT_EMAILS = {'helene@luxushair.com', 'helene721@gmail.com', 'eiriktollan.berntsen@gmail.com', 'tonjekit91@gmail.com'}

# Always accessible endpoints (authentication, basic info, etc.)
EXEMPT_ENDPOINTS = {
    'main.login', 'main.register', 'main.logout', 'main.privacy', 'main.privacy_policy',
    'main.offline', 'main.offline_html', 'static', 'favicon',
    'main.service_worker', 'main.manifest', 'main.version', 'main.contact', 'main.contact_submit',
    'main.subscription', 'main.subscription_plans', 'main.payment_success', 'main.payment_cancel',
    'main.forgot_password', 'main.reset_password', 'main.demo',
    'main.terms', 'main.about', 'main.help', 'main.features',  # General info pages
    'pricing.index', 'pricing.pricing_page', 'pricing.subscription', 'pricing.manage_subscription',  # Pricing pages
    'stocks.index', 'stocks.search', 'stocks.list_currency', 'analysis.index', 'main.referrals', 'main.send_referral'
}

# Premium features that require subscription after trial
PREMIUM_ENDPOINTS = {
    # Stocks endpoints - Remove basic endpoints from premium
    'stocks.details',
    'stocks.list_stocks',
    'stocks.list_oslo',
    'stocks.global_list',
    'stocks.list_crypto',
    # 'stocks.list_currency', # MOVED TO EXEMPT - should be accessible 
    'stocks.compare',
    'stocks.list_stocks_by_category',
    
    # Analysis endpoints
    'analysis.ai',
    'analysis.technical',
    'analysis.warren_buffett',
    'analysis.prediction',
    'analysis.market_overview',
    
    # Portfolio endpoints
    'portfolio.portfolio_index',
    'portfolio.create_portfolio',
    'portfolio.view_portfolio',
    'portfolio.edit_stock',
    'portfolio.remove_stock',
    'portfolio.add_stock_to_portfolio',
    'portfolio.remove_stock_from_portfolio',
    'portfolio.watchlist',
    'portfolio.stock_tips',
    'portfolio.transactions',
    'portfolio.add_stock',
    'portfolio.overview'
}

def url_is_safe(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def init_stripe():
    """Non-blocking Stripe initialization"""
    try:
        stripe = get_stripe()
        if current_app.config.get('STRIPE_SECRET_KEY'):
            stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
            current_app.logger.info('Stripe initialized successfully')
        else:
            current_app.logger.warning('Stripe not configured - using fallback mode')
    except Exception as e:
        current_app.logger.error(f'Stripe initialization failed: {str(e)}')
        # Don't raise - allow app to continue without Stripe

# Initialize Stripe when the blueprint is registered
@main.record_once
def on_register(state):
    """Initialize Stripe when blueprint is registered - non-blocking"""
    try:
        # Import stripe only when needed and safely
        stripe = __import__('stripe')
        
        # Set Stripe API key with safe fallback
        stripe_key = state.app.config.get('STRIPE_SECRET_KEY', 'sk_test_fallback_key')
        if stripe_key:
            stripe.api_key = stripe_key
            state.app.logger.info('✅ Stripe initialized successfully')
        else:
            state.app.logger.warning('⚠️ Stripe not configured (key missing)')
    except ImportError:
        state.app.logger.warning('⚠️ Stripe initialization skipped (module not available)')
    except Exception as e:
        state.app.logger.warning(f'⚠️ Stripe initialization failed: {e}')

@main.before_app_request
def restrict_non_subscribed_users():
    """
    LEGACY: This function is being replaced by the new @access_required decorator system.
    Only keeping it for exempt user privilege updates.
    """
    try:
        # Skip if login_manager is not initialized (for testing)
        if not hasattr(current_app, 'login_manager'):
            return
        
        # Only handle exempt user privilege updates now
        # Access control is handled by @access_required decorator
        if current_user.is_authenticated and current_user.email in EXEMPT_EMAILS:
            try:
                if not current_user.has_subscription:
                    current_user.has_subscription = True
                    current_user.subscription_type = 'lifetime'
                    db.session.commit()
            except Exception as e:
                current_app.logger.error(f"Error updating exempt user: {str(e)}")
            return

    except Exception as e:
        current_app.logger.error(f"Error in access restriction: {str(e)}")
        # On error, allow access to prevent breaking the app
        return None

# Device fingerprinting for trial tracking
def get_device_fingerprint(request):
    """Create a device fingerprint based on IP, User-Agent, and Accept headers"""
    components = [
        request.remote_addr,
        request.headers.get('User-Agent', ''),
        request.headers.get('Accept-Language', ''),
        request.headers.get('Accept-Encoding', ''),
        request.headers.get('Accept', ''),
    ]
    fingerprint = hashlib.sha256('|'.join(components).encode()).hexdigest()
    return fingerprint[:16]  # Use first 16 characters for storage efficiency

def track_device_trial(fingerprint):
    """Track trial usage for a device fingerprint"""
    from app.models.user import DeviceTrialTracker
    from app.extensions import db
    
    # Check if device has already used trial
    tracker = DeviceTrialTracker.query.filter_by(device_fingerprint=fingerprint).first()
    if tracker:
        return tracker.trial_start_time, tracker.trial_used
    
    # Create new trial tracker
    now = datetime.utcnow()
    tracker = DeviceTrialTracker(
        device_fingerprint=fingerprint,
        trial_start_time=now,
        trial_used=True
    )
    db.session.add(tracker)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving device trial tracker: {e}")
    
    return now, True

@main.before_app_request
def before_request():
    """Initialize session and handle trial logic before each request"""
    # Skip if login_manager is not initialized (for testing)
    if not hasattr(current_app, 'login_manager'):
        return
    
    # Make sure sessions are permanent for trial tracking
    session.permanent = True
    
    # Store current time for template usage
    g.current_time = int(time.time())
    
    # Ensure login state consistency across all pages
    if current_user.is_authenticated:
        # Update session with current user info for consistency
        session['user_logged_in'] = True
        session['user_id'] = current_user.id
        session['user_email'] = current_user.email
        
        # Make user info available globally for templates
        g.current_user = current_user
        g.user_logged_in = True
        g.user_email = current_user.email
        
        # Ensure exempt users have correct permissions
        if current_user.email in EXEMPT_EMAILS:
            try:
                if not current_user.has_subscription:
                    current_user.has_subscription = True
                    current_user.subscription_type = 'lifetime'
                    current_user.is_admin = True
                    db.session.commit()
            except Exception as e:
                current_app.logger.error(f"Error updating exempt user: {str(e)}")
    else:
        # Clear user session data if not authenticated
        session.pop('user_logged_in', None)
        session.pop('user_id', None)
        session.pop('user_email', None)
        
        # Clear global user info
        g.current_user = None
        g.user_logged_in = False
        g.user_email = None

    # 1. Device fingerprinting and trial tracking
    # DISABLED: Using @trial_required decorator instead for consistent trial logic
    # try:
    #     fingerprint = get_device_fingerprint(request)
    #     session['device_fingerprint'] = fingerprint
    #     
    #     # Track trial usage for the device
    #     trial_start, trial_used = track_device_trial(fingerprint)
    #     session['trial_start_time'] = trial_start.isoformat()
    #     session['trial_used'] = trial_used
    # except Exception as e:
    #     current_app.logger.error(f"Error in device fingerprinting/trial tracking: {str(e)}")
    
    # 2. Restrict access for non-subscribed users
    try:
        restrict_non_subscribed_users()
    except Exception as e:
        current_app.logger.error(f"Error in restrict_non_subscribed_users: {str(e)}")
        # Allow access if there's an error to prevent app from breaking
        return

@main.route('/')
@main.route('/index')
def index():
    """Fast-loading homepage - heavy data loaded via API endpoints"""
    import logging
    from datetime import datetime

    logger = logging.getLogger(__name__)
    logger.info("🚀 Homepage route accessed (fast-loading version)")

    # Temporarily disable demo redirect for testing - TODO: Re-enable after fixing demo data issues
    # Quick check for authentication first
    # if not current_user.is_authenticated:
    #     logger.info("👤 Public user accessing homepage - redirecting to demo")
    #     return redirect(url_for('main.demo'))

    # Initialize with lightweight real market data for instant loading
    market_data = {
        'osebx': {'value': 1300, 'change': 5.2, 'change_percent': 0.4},
        'usd_nok': {'rate': 10.8, 'change': 0.05},
        'btc': {'price': 45000, 'change': 1200},
        'market_open': True,
        'last_update': datetime.now().isoformat(),
        'oslo_stocks': [],
        'global_stocks': [],
        'crypto_stocks': [],
        'currency': {}
    }

    # Only try cached data for instant loading - no API calls on page load
    try:
        cached_oslo = simple_cache.get('homepage_oslo_data', 'market_data')
        if cached_oslo:
            market_data['oslo_stocks'] = cached_oslo[:5]  # Limit for faster rendering
        cached_global = simple_cache.get('homepage_global_data', 'market_data')
        if cached_global:
            market_data['global_stocks'] = cached_global[:5]
        cached_crypto = simple_cache.get('homepage_crypto_data', 'market_data')
        if cached_crypto:
            market_data['crypto_stocks'] = cached_crypto[:5]
    except Exception as e:
        logger.error(f"Error loading cached market data: {str(e)}")
    # Render homepage with fast-loading market data
    return render_template('index.html', market_data=market_data)

@main.route('/debug-status')
def debug_status():
    return render_template('debug_status.html')

@main.route('/feedback')
def feedback():
    return render_template('feedback.html')

@main.route('/demo/ping')
def demo_ping():
    return 'pong', 200

@main.route('/demo/echo')
def demo_echo():
    return 'echo', 200

@main.route('/account/settings')
def account_settings():
    return render_template('account_settings.html')
@main.route('/demo')
@demo_access
def demo():
    """Demo page with full functionality preview"""
    try:
        # Get real data for demo stocks
        data_service = get_data_service()
        oslo_stocks = ['EQNR.OL', 'DNB.OL', 'TEL.OL']
        stocks_data = []
        for symbol in oslo_stocks:
            stock_info = data_service.get_stock_info(symbol)
            if stock_info:
                stocks_data.append(stock_info)
        # If no real data available, use minimal fallback
        if not stocks_data:
            stocks_data = [
                {'symbol': 'EQNR.OL', 'name': 'Equinor ASA', 'price': 'Demo', 'change': 'Demo', 'signal': 'DEMO', 'analysis': 'Demo data - registrer for ekte data'},
                {'symbol': 'DNB.OL', 'name': 'DNB Bank ASA', 'price': 'Demo', 'change': 'Demo', 'signal': 'DEMO', 'analysis': 'Demo data - registrer for ekte data'},
                {'symbol': 'TEL.OL', 'name': 'Telenor ASA', 'price': 'Demo', 'change': 'Demo', 'signal': 'DEMO', 'analysis': 'Demo data - registrer for ekte data'}
            ]
        demo_data = {
            'demo_mode': True,
            'stocks': stocks_data,
            'analysis': {
                'recommendation': 'KJØP',
                'confidence': '85%',
                'target_price': '320 NOK',
                'risk_level': 'Moderat',
                'time_horizon': '6-12 måneder',
                'signals': [
                    'Sterk teknisk momentum',
                    'Positiv fundamental utvikling',
                    'Økende institusjonell interesse'
                ]
            },
            'portfolio': {
                'total_value': 'Varierer med markedet',
                'daily_change': 'Sanntids beregning',
                'daily_change_percent': 'Live data',
                'holdings': [
                    {'symbol': 'EQNR.OL', 'name': 'Equinor', 'quantity': 100, 'value': 'Live data', 'change': 'Live data'},
                    {'symbol': 'DNB.OL', 'name': 'DNB Bank', 'quantity': 200, 'value': 'Live data', 'change': 'Live data'},
                    {'symbol': 'TEL.OL', 'name': 'Telenor', 'quantity': 50, 'value': 'Live data', 'change': 'Live data'}
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error getting real data for demo page: {e}")
        # Fallback with clear indication it's demo data
        demo_data = {
            'demo_mode': True,
            'stocks': [
                {'symbol': 'EQNR.OL', 'name': 'Equinor ASA', 'price': 'Demo', 'change': 'Demo', 'signal': 'DEMO', 'analysis': 'Demo data - registrer for ekte data'},
                {'symbol': 'DNB.OL', 'name': 'DNB Bank ASA', 'price': 'Demo', 'change': 'Demo', 'signal': 'DEMO', 'analysis': 'Demo data - registrer for ekte data'},
                {'symbol': 'TEL.OL', 'name': 'Telenor ASA', 'price': 'Demo', 'change': 'Demo', 'signal': 'DEMO', 'analysis': 'Demo data - registrer for ekte data'}
            ],
            'analysis': {
                'recommendation': 'DEMO',
                'confidence': 'Demo',
                'target_price': 'Demo data',
                'risk_level': 'Demo',
                'time_horizon': 'Demo',
                'signals': [
                    'Dette er demo data',
                    'Registrer for ekte markedsdata',
                    'Live priser og analyse'
                ]
            },
            'portfolio': {
                'total_value': 'Demo data',
                'daily_change': 'Demo data',
                'daily_change_percent': 'Demo',
                'holdings': [
                    {'symbol': 'EQNR.OL', 'name': 'Equinor', 'quantity': 100, 'value': 'Demo', 'change': 'Demo'},
                    {'symbol': 'DNB.OL', 'name': 'DNB Bank', 'quantity': 200, 'value': 'Demo', 'change': 'Demo'},
                    {'symbol': 'TEL.OL', 'name': 'Telenor', 'quantity': 50, 'value': 'Demo', 'change': 'Demo'}
                ]
            }
        }
    return render_template('demo.html', **demo_data)

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard for authenticated users"""
    try:
        # Check if user has active subscription
        user_has_subscription = False
        if current_user.is_authenticated:
            user_has_subscription = getattr(current_user, 'has_subscription', False) or \
                                  getattr(current_user, 'subscription_type', None) in ['premium', 'pro', 'yearly', 'lifetime']
        
        # Get dashboard data 
        dashboard_data = {
            'user': current_user,
            'has_subscription': user_has_subscription,
            'market_status': 'Open' if is_market_open() else 'Closed',
            'oslo_status': 'Open' if is_oslo_bors_open() else 'Closed'
        }
        
        # Add some basic market data for dashboard
        try:
            dashboard_service = DashboardService()
            market_data = dashboard_service.get_basic_market_data()
            dashboard_data.update(market_data)
        except Exception as e:
            logger.warning(f"Could not load dashboard market data: {e}")
            dashboard_data.update({
                'market_summary': {},
                'top_movers': [],
                'user_favorites': [],
                'recent_news': []
            })
        
        return render_template('dashboard.html', **dashboard_data)
        
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        flash('Det oppstod en feil ved lasting av dashboard.', 'error')
        return redirect(url_for('main.index'))

# Portfolio routes moved to portfolio blueprint

# Ensure all templates are functioning and accessible
# This includes checking for duplicates and ensuring correct URLs are set
# Additional checks for mobile and desktop navigation links

# Pricing route handled by pricing blueprint (/pricing/)

@main.route('/search')
@access_required
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
     
    # Use DataService.search_stocks for real data
    from ..services.data_service import DataService
    results = DataService.search_stocks(query)
    return render_template('search_results.html', results=results, query=query)

# # Prices route moved to stocks.py to avoid conflicts
# # @main.route('/prices')
# # @access_required
# # def prices():
#     """Comprehensive market prices overview"""
#     try:
#         # Lazy import DataService
#         DataService = get_data_service()
#         
#         # Get data for all markets with fallback
#         oslo_stocks = DataService.get_oslo_bors_overview() or {}
#         global_stocks = DataService.get_global_stocks_overview() or {}
#         crypto = DataService.get_crypto_overview() or {}
#         currency = DataService.get_currency_overview() or {}
#         
#         # Calculate statistics
#         stats = {
#             'total_stocks': len(oslo_stocks) + len(global_stocks),
#             'total_crypto': len(crypto),
#             'total_currency': len(currency),
#             'total_instruments': len(oslo_stocks) + len(global_stocks) + len(crypto) + len(currency)
#         }
#         
#         return render_template('stocks/prices.html', 
#                              market_data={
#                                  'oslo_stocks': oslo_stocks,
#                                  'global_stocks': global_stocks,
#                                  'crypto': crypto,
#                                  'currency': currency
#                              },
#                              stats=stats)
#     except Exception as e:
#         current_app.logger.error(f"Error in prices route: {e}")
#         # Return template with fallback data instead of redirect
#         fallback_stats = {
#             'total_stocks': 250,
#             'total_crypto': 50,
#             'total_currency': 30,
#             'total_instruments': 330
#         }
#         return render_template('stocks/prices.html', 
#                              market_data={
#                                  'oslo_stocks': {},
#                                  'global_stocks': {},
#                                  'crypto': {},
#                                  'currency': {}
#                              },
#                              stats=fallback_stats,
#                              error="Det oppstod en feil ved henting av prisdata, viser fallback-data")
# 
# @main.route('/login', methods=['GET', 'POST'])
# def login():
    """Login page with proper form handling and database error recovery"""
    from flask import request
    from ..models import User
    from ..forms import LoginForm
    from werkzeug.security import check_password_hash
    from sqlalchemy.exc import OperationalError, ProgrammingError
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            # Try to find user by email
            user = User.query.filter_by(email=form.email.data.lower().strip()).first()
            
            if user and user.password_hash and check_password_hash(user.password_hash, form.password.data):
                # Update last login if column exists
                try:
                    user.last_login = datetime.utcnow()
                    if hasattr(user, 'login_count'):
                        user.login_count = (user.login_count or 0) + 1
                    db.session.commit()
                except Exception as update_error:
                    current_app.logger.warning(f'Could not update login stats: {update_error}')
                    db.session.rollback()
                
                login_user(user, remember=form.remember_me.data)
                
                next_page = request.args.get('next')
                if not next_page or urlparse(next_page).netloc != '':
                    next_page = url_for('main.index')
                
                current_app.logger.info(f'Successful login for user: {user.email}')
                flash('Innlogging vellykket!', 'success')
                return redirect(next_page)
            else:
                current_app.logger.warning(f'Failed login attempt for email: {form.email.data}')
                flash('Ugyldig e-post eller passord.', 'danger')
                
        except (OperationalError, ProgrammingError) as db_error:
            current_app.logger.error(f'Database error during login: {db_error}')
            flash('Database-feil. Kontakt support hvis problemet vedvarer.', 'danger')
            
        except Exception as e:
            current_app.logger.error(f'Unexpected login error: {e}')
            flash('En feil oppstod under innloggingen. Prøv igjen.', 'danger')
    
    return render_template('login.html', title='Logg inn', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - redirect to auth blueprint"""
    return redirect(url_for('auth.login'))

@main.route('/logout', methods=['GET', 'POST'])
def logout():
    user_email = current_user.email if current_user.is_authenticated else 'Unknown'
    
    # First logout the user
    if current_user.is_authenticated:
        logout_user()
    
    # Clear all session data completely
    session.clear()
    
    current_app.logger.info(f'User logged out: {user_email}')
    
    # Flash message that will show on homepage
    flash('Du er nå utlogget.', 'success')
    
    # Create simple response with minimal headers
    response = make_response(redirect(url_for('main.index')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Clear only essential cookies
    response.set_cookie('session', '', expires=0, max_age=0, path='/')
    response.set_cookie('remember_token', '', expires=0, max_age=0, path='/')
    response.set_cookie('user_logged_in', '', expires=0, max_age=0, path='/')
    
    return response

def unauthorized_handler():
    # For API requests, return JSON error instead of redirect
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Authentication required'}), 401
    flash('Du må logge inn for å få tilgang til denne siden.', 'warning')
    return redirect(url_for('main.login', next=request.url))

# Register unauthorized handler (this will override the one in __init__.py)
login_manager.unauthorized_handler(unauthorized_handler)

@main.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page with proper form handling"""
    from flask import request
    from ..models import User
    from ..extensions import db
    from ..forms import RegistrationForm
    from werkzeug.security import generate_password_hash
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('En bruker med denne e-postadressen eksisterer allerede.', 'danger')
                return render_template('register.html', title='Registrer deg', form=form)
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registreringen var vellykket! Du kan nå logge inn.', 'success')
            return redirect(url_for('main.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration error: {e}')
            flash('En feil oppstod under registreringen. Prøv igjen.', 'danger')
    
    return render_template('register.html', title='Registrer deg', form=form)

@main.route('/share-target')
@access_required
def handle_share():
    """Handle content shared to the app"""
    shared_text = request.args.get('text', '')
    shared_url = request.args.get('url', '')
    
    # Hvis delt innhold ser ut som en aksjeticker (f.eks. "AAPL")
    if shared_text and len(shared_text.strip()) < 10 and shared_text.strip().isalpha():
        return redirect(url_for('stocks.details', ticker=shared_text.strip()))
    
    # Ellers, bruk søkefunksjonen
    return redirect(url_for('stocks.search', query=shared_text.strip()))

# Market overview route moved to analysis.py to avoid conflicts

@main.route('/service-worker.js')
def service_worker():
    """Serve the service worker from the root"""
    return current_app.send_static_file('service-worker.js')

@main.route('/manifest.json')
def manifest():
    """Serve the manifest.json file for PWA support"""
    try:
        manifest_path = os.path.join(current_app.root_path, 'static', 'manifest.json')
        
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                manifest_content = f.read()
            
            response = make_response(manifest_content)
            response.headers['Content-Type'] = 'application/manifest+json'
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        else:
            current_app.logger.error(f"Manifest file not found at: {manifest_path}")
            return jsonify({'error': 'Manifest not found'}), 404
            
    except Exception as e:
        current_app.logger.error(f"Error serving manifest.json: {str(e)}")
        return jsonify({'error': 'Manifest not found'}), 404

@main.route('/offline')
def offline():
    """Offline page for PWA"""
    return render_template('offline.html')

@main.route('/offline.html')
def offline_html():
    """Offline HTML page for PWA"""
    return render_template('offline.html')

@main.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        return contact_submit()
    return render_template('contact.html')
@main.route('/contact/submit', methods=['POST'])
def contact_submit():
    """Handle contact form submission"""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not name or not email or not message:
            flash('Alle felt må fylles ut.', 'error')
            return redirect(url_for('main.contact'))
        
        # Here you would normally send an email or save to database
        current_app.logger.info(f"Contact form submitted by {email}")
        
        flash('Takk for din henvendelse! Vi vil svare deg så snart som mulig.', 'success')
        return redirect(url_for('main.contact'))
        
    except Exception as e:
        current_app.logger.error(f"Error in contact form: {e}")
        flash('Det oppstod en feil. Vennligst prøv igjen senere.', 'error')
        return redirect(url_for('main.contact'))

@main.route('/subscription')
@main.route('/subscription/')
@login_required
def subscription():
    """Subscription management page"""
    try:
        # Redirect to pricing page for subscription plans
        return redirect(url_for('pricing.index'))
    except Exception as e:
        current_app.logger.error(f"Error redirecting to pricing: {e}")
        flash('Kunne ikke laste prissiden.', 'error')
        return redirect(url_for('main.index'))

@main.route('/subscription/plans')
@login_required
def subscription_plans():
    """Subscription plans page"""
    try:
        # Redirect to pricing page since that's where plans are shown
        return redirect(url_for('pricing.index'))
    except Exception as e:
        current_app.logger.error(f"Error redirecting to pricing: {e}")
        flash('Kunne ikke laste prissiden.', 'error')
        return redirect(url_for('main.index'))

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password reset request"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm, ReferralForm = get_forms()
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        User = get_user_model()
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # Generate reset token
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(user.email, salt='password-reset-salt')
            
            # Send reset email
            try:
                msg = EmailMessage(
                    'Tilbakestill passord - Aksjeradar',
                    sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@aksjeradar.trade'),
                    recipients=[user.email]
                )
                reset_url = url_for('main.reset_password', token=token, _external=True)
                msg.body = f'''Hei {user.username},

Du har bedt om å tilbakestille passordet ditt på Aksjeradar.

Klikk på følgende lenke for å tilbakestille passordet:
{reset_url}

Hvis du ikke har bedt om dette, kan du ignorere denne e-posten.

Med vennlig hilsen,
Aksjeradar-teamet'''
                
                mail.send(msg)
                flash('En e-post med instruksjoner for å tilbakestille passordet har blitt sendt.', 'info')
            except Exception as e:
                current_app.logger.error(f"Failed to send reset email: {e}")
                flash('Kunne ikke sende e-post. Vennligst prøv igjen senere.', 'error')
        else:
            # Don't reveal if email exists or not
            flash('Hvis e-postadressen finnes i systemet, vil du motta en e-post med instruksjoner.', 'info')
        
        return redirect(url_for('main.login'))
    
    return render_template('forgot_password.html', form=form)

@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm, ReferralForm = get_forms()
    form = ResetPasswordForm()
    
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hour expiry
    except:
        flash('Ugyldig eller utløpt lenke for tilbakestilling av passord.', 'error')
        return redirect(url_for('main.login'))
    
    if form.validate_on_submit():
        User = get_user_model()
        user = User.query.filter_by(email=email).first()
        
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Passordet ditt har blitt oppdatert! Du kan nå logge inn.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Bruker ikke funnet.', 'error')
            return redirect(url_for('main.login'))
    
    return render_template('reset_password.html', form=form, token=token)

@main.route('/referrals')
@login_required
def referrals():
    """Referral program page"""
    ReferralService = get_referral_service()
    
    # Get user's referral code
    referral_code = ReferralService.get_or_create_referral_code(current_user)
    
    # Get referral stats
    stats = ReferralService.get_referral_stats(current_user)
    
    # Generate referral link
    referral_link = url_for('main.register', ref=referral_code, _external=True)
    
    return render_template('referrals.html',
                         referral_code=referral_code,
                         referral_link=referral_link,
                         stats=stats)

@main.route('/referrals/send', methods=['POST'])
@login_required
def send_referral():
    """Send referral invitation"""
    email = request.form.get('email')
    
    if not email:
        flash('E-postadresse er påkrevd.', 'error')
        return redirect(url_for('main.referrals'))
    
    ReferralService = get_referral_service()
    referral_code = ReferralService.get_or_create_referral_code(current_user)
    referral_link = url_for('main.register', ref=referral_code, _external=True)
    
    try:
        msg = EmailMessage(
            f'{current_user.username} inviterer deg til Aksjeradar',
            sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@aksjeradar.trade'),
            recipients=[email]
        )
        msg.body = f'''Hei!

{current_user.username} har invitert deg til å prøve Aksjeradar - Norges smarteste aksjeplattform.

Registrer deg med denne lenken for å få spesielle fordeler:
{referral_link}

Med Aksjeradar får du:
- AI-drevne aksjeanalyser
- Sanntids markedsdata
- Porteføljeovervåking
- Ekspertanbefalinger

Bli med i dag!

Med vennlig hilsen,
Aksjeradar-teamet'''
        
        mail.send(msg)
        flash(f'Invitasjon sendt til {email}!', 'success')
    except Exception as e:
        current_app.logger.error(f"Failed to send referral email: {e}")
        flash('Kunne ikke sende invitasjon. Vennligst prøv igjen senere.', 'error')
    
    return redirect(url_for('main.referrals'))

@main.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('terms.html', now=datetime.now())

@main.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html', now=datetime.now())

@main.route('/about')
def about():
    """About page"""
    return render_template('about.html', 
                         title="Om Aksjeradar",
                         now=datetime.now())

@main.route('/help')
def help():
    """Help and FAQ page"""
    return render_template('help.html', 
                         title="Hjelp og FAQ",
                         now=datetime.now())

@main.route('/settings', methods=['GET', 'POST'])
@demo_access 
def settings():
    """User settings page"""
    if request.method == 'POST' and current_user.is_authenticated:
        try:
            # Handle form submission for authenticated users
            full_name = request.form.get('full_name')
            email = request.form.get('email') 
            phone = request.form.get('phone')
            
            # Update user profile
            current_user.full_name = full_name
            current_user.email = email
            current_user.phone = phone
            
            # Commit changes
            db.session.commit()
            
            flash('Profil oppdatert!', 'success')
            return redirect(url_for('main.settings'))
            
        except Exception as e:
            flash('Feil ved oppdatering av profil.', 'error')
            db.session.rollback()
    
    return render_template('settings.html', 
                         title="Innstillinger",
                         now=datetime.now())

@main.route('/update_notifications', methods=['POST'])
@login_required
def update_notifications():
    """Update user notification settings"""
    try:
        # Get notification preferences from form
        email_notifications = request.form.get('email_notifications') == 'on'
        price_alerts = request.form.get('price_alerts') == 'on'
        market_news = request.form.get('market_news') == 'on'

        # Update user preferences
        if hasattr(current_user, 'email_notifications'):
            current_user.email_notifications = email_notifications
        if hasattr(current_user, 'price_alerts'):
            current_user.price_alerts = price_alerts
        if hasattr(current_user, 'market_news'):
            current_user.market_news = market_news

        # Commit changes
        db.session.commit()

        flash('Varselinnstillinger oppdatert!', 'success')
        return redirect(url_for('main.settings'))

    except Exception as e:
        logger.error(f"Error updating notification settings: {e}")
        flash('Feil ved oppdatering av varselinnstillinger.', 'error')
        db.session.rollback()
        return redirect(url_for('main.settings'))

@main.route('/features')
def features():
    """Features overview page"""
    return render_template('features.html', 
                         title="Funksjoner",
                         now=datetime.now())

# Error handlers
@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@main.route('/favorites')
@access_required
def favorites():
    """User favorites page"""
    try:
        # @access_required guarantees authenticated user with subscription
        user_favorites = Favorites.get_user_favorites(current_user.id)
        
        return render_template('favorites.html',
                             favorites=user_favorites,
                             page_title="Mine Favoritter",
                             favorites_count=len(user_favorites) if user_favorites else 0)
    except Exception as e:
        logger.error(f"Error loading favorites: {e}")
        return render_template('favorites.html',
                             favorites=[],
                             page_title="Mine Favoritter",
                             favorites_count=0)

@main.route('/profile')
@access_required
def profile():
    """User profile page with proper error handling"""
    try:
        # @access_required guarantees authenticated user with subscription
        # Safely get user subscription info
        subscription = None
        subscription_status = 'free'
        
        if hasattr(current_user, 'subscription') and current_user.subscription:
            subscription = current_user.subscription
            subscription_status = getattr(subscription, 'status', 'free')
        
        # Get user stats safely
        user_stats = {
            'member_since': getattr(current_user, 'created_at', datetime.now()),
            'last_login': getattr(current_user, 'last_login', None),
            'total_searches': getattr(current_user, 'search_count', 0),
            'favorite_stocks': getattr(current_user, 'favorite_count', 0)
        }
        
        # Get referral stats safely
        referral_stats = {
            'referrals_made': getattr(current_user, 'referrals_made', 0),
            'referral_earnings': getattr(current_user, 'referral_earnings', 0),
            'referral_code': getattr(current_user, 'referral_code', f'REF{current_user.id}' if hasattr(current_user, 'id') else 'REF001')
        }
        
        # Get user preferences safely
        user_preferences = current_user.get_notification_settings() if hasattr(current_user, 'get_notification_settings') else {}
        user_language = current_user.get_language() if hasattr(current_user, 'get_language') else 'nb'
        
        user_favorites = Favorites.get_user_favorites(current_user.id)
        return render_template('profile.html',
            user=current_user,
            subscription=subscription,
            subscription_status=subscription_status,
            user_stats=user_stats,
            user_language=user_language,
            user_display_mode=user_preferences.get('display_mode', 'light'),
            user_number_format=user_preferences.get('number_format', 'norwegian'),
            user_dashboard_widgets=user_preferences.get('dashboard_widgets', '[]'),
            user_favorites=user_favorites,
            **referral_stats)
                             
    except Exception as e:
        logger.error(f"Error in profile page for user {getattr(current_user, 'id', 'unknown')}: {e}")
        flash('Kunne ikke laste profilsiden. Prøv igjen senere.', 'error')
    return render_template('profile.html',
                 user=current_user,
                 subscription=None,
                 subscription_status='free',
                 user_stats={},
                 user_language='nb',
                 user_display_mode='light',
                 user_number_format='norwegian',
                 user_dashboard_widgets='[]',
                 user_favorites=user_favorites,
                 referrals_made=0,
                 referral_earnings=0,
                 referral_code='REF001',
                             error=True)

@main.route('/mitt-abonnement')
@main.route('/my-subscription')
@login_required
def my_subscription():
    """Dedicated user subscription management page"""
    try:
        # Check actual user subscription status
        user_subscription = current_user.subscription_status if current_user.is_authenticated else 'free'
        is_premium = user_subscription == 'active'
        
        # Get detailed subscription info based on actual status
        if is_premium:
            subscription_info = {
                'status': 'active',
                'plan_name': 'Premium',
                'plan_description': 'Full tilgang til alle analyser og funksjoner',
                'start_date': current_user.created_at if hasattr(current_user, 'created_at') else None,
                'end_date': None,
                'next_billing': None,
                'price': 399,
                'currency': 'NOK',
                'features': [
                    'Ubegrenset tilgang til alle aksjer',
                    'Avanserte analyser (Warren Buffett, Benjamin Graham)',
                    'AI-drevne anbefalinger',
                    'Innsidehandel-overvåkning',
                    'Sanntids prisdata',
                    'Porteføljeoptimalisering',
                    'Backtesting av strategier'
                ],
                'upgrade_options': []
            }
        else:
            subscription_info = {
                'status': 'free',
                'plan_name': 'Gratis',
                'plan_description': 'Grunnleggende tilgang til aksjedata og analyser',
                'start_date': None,
                'end_date': None,
                'next_billing': None,
                'price': 0,
                'currency': 'NOK',
                'features': [
                    'Begrenset tilgang til aksjedata',
                    'Grunnleggende teknisk analyse',
                    'Daglig markedsoversikt'
                ],
                'upgrade_options': [
                {
                    'name': 'Premium',
                    'price': 399,
                    'billing': 'monthly',
                    'features': [
                        'Ubegrenset tilgang til alle aksjer',
                        'Avanserte analyser (Warren Buffett, Benjamin Graham)',
                        'AI-drevne anbefalinger',
                        'Innsidehandel-overvåkning',
                        'Sanntids prisdata',
                        'Porteføljeoptimalisering og backtesting'
                    ]
                },
                {
                    'name': 'Premium',
                    'price': 2999,
                    'billing': 'yearly',
                    'features': [
                        'Alt i månedspakken',
                        'Årlig rabatt (spare 1789 kr)',
                        'Prioritert kundestøtte',
                        'Tidlig tilgang til nye funksjoner',
                        'API-tilgang',
                        'Avanserte screener-filter'
                    ]
                }
            ]
        }
        
        # Check if user has active subscription or is exempt
        is_exempt_user = current_user.email in {
            'helene@luxushair.com', 
            'helene721@gmail.com', 
            'eiriktollan.berntsen@gmail.com',
            'tonjekit91@gmail.com'
        }
        
        if is_exempt_user:
            subscription_info.update({
                'status': 'active',
                'plan_name': 'Premium',
                'plan_description': 'Full tilgang til alle funksjoner som premium bruker',
                'start_date': datetime.now().date(),
                'end_date': None,  # No end date for exempt users
                'next_billing': None,  # No billing for exempt users
                'price': 0,  # Free for exempt users
                'currency': 'NOK',
                'features': [
                    'Ubegrenset tilgang til alle aksjer og analyser',
                    'Avanserte analyser (Warren Buffett, Benjamin Graham)',
                    'AI-drevne anbefalinger og porteføljeoptimalisering',
                    'Innsidehandel-overvåkning og sanntids data',
                    'Backtesting og screener-funksjoner',
                    'API-tilgang og prioritert support',
                    'Premium bruker (livstid tilgang)'
                ],
                'is_exempt': True
            })
        elif hasattr(current_user, 'subscription') and current_user.subscription:
            subscription = current_user.subscription
            if hasattr(subscription, 'status') and subscription.status == 'active':
                subscription_info.update({
                    'status': 'active',
                    'plan_name': getattr(subscription, 'plan_name', 'Pro'),
                    'start_date': getattr(subscription, 'start_date', None),
                    'end_date': getattr(subscription, 'end_date', None),
                    'next_billing': getattr(subscription, 'next_billing_date', None),
                    'price': getattr(subscription, 'price', 299),
                    'features': [
                        'Ubegrenset tilgang til alle aksjer',
                        'Avanserte analyser',
                        'AI-drevne anbefalinger',
                        'Sanntids prisdata'
                    ]
                })
        
        return render_template('subscription_management.html',
                             subscription=subscription_info,
                             user=current_user)
                             
    except Exception as e:
        logger.error(f"Error in subscription page for user {getattr(current_user, 'id', 'unknown')}: {e}")
        flash('Kunne ikke laste abonnementssiden. Prøv igjen senere.', 'error')
        return redirect(url_for('main.profile'))

@main.route('/set_language/<language>')
def set_language(language=None):
    """Set user language preference"""
    if language in ['no', 'en']:
        session['language'] = language
        flash(f'Språk endret til {"Norsk" if language == "no" else "English"}', 'success')
    
    # Redirect back to referring page or home
    return redirect(request.referrer or url_for('main.index'))

@main.route('/admin/cache')
def cache_management():
    """Cache management interface"""
    return render_template('cache_management.html')

@main.route('/admin/api/cache/bust', methods=['POST'])
def bust_cache():
    """API endpoint to trigger cache busting"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        return jsonify({
            'success': True,
            'timestamp': timestamp,
            'message': 'Cache busted successfully',
            'reload_recommended': True
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/admin/api/cache/status')
def cache_status():
    """Check current cache version"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return jsonify({
            'cache_version': timestamp,
            'last_updated': timestamp,
            'status': 'active'
        })
    except Exception as e:
        return jsonify({
            'cache_version': 'unknown',
            'last_updated': 'never',
            'status': 'error',
            'error': str(e)
        })

# Stripe Integration Routes
@main.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    try:
        from ..services.stripe_service import stripe_service
        
        payload = request.get_data(as_text=True)
        signature = request.headers.get('Stripe-Signature')
        
        if not signature:
            logger.error("Missing Stripe signature header")
            return jsonify({'error': 'Missing signature'}), 400
        
        success = stripe_service.handle_webhook(payload, signature)
        
        if success:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'error': 'Webhook processing failed'}), 400
            
    except Exception as e:
        logger.error(f"Error in Stripe webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/subscription/checkout/<plan>')
@access_required
def subscription_checkout(plan):
    """Create Stripe checkout session for subscription"""
    try:
        from ..services.stripe_service import stripe_service
        
        # Define price IDs for different plans (these are test values)
        price_ids = {
            'monthly': 'price_test_monthly_99nok',     # Test price ID
            'yearly': 'price_test_yearly_990nok',      # Test price ID
            'lifetime': 'price_test_lifetime_2990nok'  # Test price ID
        }
        
        if plan not in price_ids:
            flash('Ugyldig abonnementsplan.', 'error')
            return redirect(url_for('main.pricing'))
        
        # For now, redirect to a coming soon page since Stripe is not fully configured
        flash('Stripe betalinger kommer snart! Kontakt support for å få tilgang.', 'info')
        return redirect(url_for('main.pricing'))
        
        # Uncomment when Stripe is properly configured:
        # checkout_url = stripe_service.create_checkout_session(
        #     user=current_user,
        #     price_id=price_ids[plan]
        # )
        # if checkout_url:
        #     return redirect(checkout_url)
        # else:
        #     flash('Kunne ikke opprette betalingslink. Prøv igjen senere.', 'error')
        #     return redirect(url_for('main.pricing'))
            
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        flash('Feil ved opprettelse av betaling. Prøv igjen senere.', 'error')
        return redirect(url_for('main.pricing'))

@main.route('/subscription/success')
@access_required
def subscription_success():
    """Handle successful subscription payment"""
    try:
        session_id = request.args.get('session_id')
        demo_mode = request.args.get('demo')
        
        if demo_mode:
            flash('Demo modus: I en reell implementering ville abonnementet ditt nå være aktivt. Dette er kun for demonstrasjon.', 'info')
            return render_template('subscription_demo_success.html')
        elif session_id:
            flash('Takk for kjøpet! Ditt Pro-abonnement er nå aktivt.', 'success')
        else:
            flash('Betaling fullført! Velkommen til Pro.', 'success')
        
        return redirect(url_for('main.account_settings'))
        
    except Exception as e:
        logger.error(f"Error in subscription success: {e}")
        flash('Abonnement aktivert!', 'success')
        return redirect(url_for('main.index'))

@main.route('/subscription/manage')
@access_required
def manage_subscription():
    """Redirect to Stripe Customer Portal for subscription management"""
    try:
        from ..services.stripe_service import stripe_service
        
        portal_url = stripe_service.create_customer_portal_session(current_user)
        
        if portal_url:
            return redirect(portal_url)
        else:
            flash('Kunne ikke åpne abonnementshåndtering. Kontakt support.', 'error')
            return redirect(url_for('main.account_settings'))
            
    except Exception as e:
        logger.error(f"Error creating portal session: {e}")
        flash('Feil ved åpning av abonnementshåndtering.', 'error')
        return redirect(url_for('main.account_settings'))

@main.route('/update-preferences', methods=['POST'])
@login_required
def update_preferences():
    """Update user preferences"""
    try:
        # Get form data
        language = request.form.get('language', 'nb')
        display_mode = request.form.get('display_mode', 'light')
        number_format = request.form.get('number_format', 'norwegian')
        dashboard_widgets = request.form.get('dashboard_widgets', '[]')
        
        # Validate preferences
        valid_languages = ['nb', 'en']
        valid_display_modes = ['auto', 'light', 'dark']
        valid_number_formats = ['norwegian', 'us']
        
        if language not in valid_languages:
            language = 'nb'
        if display_mode not in valid_display_modes:
            display_mode = 'light'
        if number_format not in valid_number_formats:
            number_format = 'norwegian'
        
        # Update user language
        if hasattr(current_user, 'set_language'):
            current_user.set_language(language)
        
        # Update notification settings with preferences
        if hasattr(current_user, 'get_notification_settings') and hasattr(current_user, 'update_notification_settings'):
            current_settings = current_user.get_notification_settings()
            current_settings.update({
                'display_mode': display_mode,
                'number_format': number_format,
                'dashboard_widgets': dashboard_widgets
            })
            success = current_user.update_notification_settings(current_settings)
            
            if success:
                flash('Preferanser lagret!', 'success')
            else:
                flash('Feil ved lagring av preferanser. Prøv igjen.', 'error')
        else:
            # Fallback to session storage
            session['user_language'] = language
            session['user_display_mode'] = display_mode
            session['user_number_format'] = number_format
            session['user_dashboard_widgets'] = dashboard_widgets
            flash('Preferanser lagret (midlertidig)!', 'success')
        
        return redirect(url_for('main.profile'))
        
    except Exception as e:
        logger.error(f"Error updating preferences: {e}")
        flash('Feil ved lagring av preferanser. Prøv igjen.', 'error')
        return redirect(url_for('main.profile'))

@main.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    try:
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        
        # Update user profile fields that exist
        if email and email != current_user.email:
            # Check if email is already taken
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != current_user.id:
                flash('E-post adresse er allerede i bruk.', 'error')
                return redirect(url_for('main.settings'))
            current_user.email = email
        
        # Add first_name and last_name fields if they don't exist
        if not hasattr(current_user, 'first_name'):
            try:
                db.session.execute(text('ALTER TABLE users ADD COLUMN first_name VARCHAR(50)'))
                db.session.commit()
            except Exception:
                pass  # Column might already exist
                
        if not hasattr(current_user, 'last_name'):
            try:
                db.session.execute(text('ALTER TABLE users ADD COLUMN last_name VARCHAR(50)'))
                db.session.commit()
            except Exception:
                pass  # Column might already exist
        
        # Update name fields if they exist
        if hasattr(current_user, 'first_name'):
            current_user.first_name = first_name
        if hasattr(current_user, 'last_name'):
            current_user.last_name = last_name
            
        db.session.commit()
        flash('Profil oppdatert!', 'success')
        
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        flash('Feil ved oppdatering av profil.', 'error')
        db.session.rollback()
        
    return redirect(url_for('main.settings'))

@main.route('/testindex')
def testindex():
    """Test homepage layout for development"""
    try:
        # Get real market data for testing
        data_service = get_data_service()
        
        # Oslo Børs data (returns list)
        oslo_data = data_service.get_oslo_stocks()
        logger.info(f"Oslo data type: {type(oslo_data)}, length: {len(oslo_data) if oslo_data else 'None'}")
        
        # Global stocks data (returns list)  
        global_data = data_service.get_global_stocks()
        logger.info(f"Global data type: {type(global_data)}, length: {len(global_data) if global_data else 'None'}")
        
        # Crypto data (returns dict)
        crypto_data = data_service.get_crypto_overview()
        logger.info(f"Crypto data type: {type(crypto_data)}")
        
        # Convert crypto dict to list if needed
        crypto_list = []
        if isinstance(crypto_data, dict):
            crypto_list = list(crypto_data.values())[:10]
        elif isinstance(crypto_data, list):
            crypto_list = crypto_data[:10]
        
        # Ensure we have safe data for template
        oslo_stocks = oslo_data[:10] if oslo_data else []
        global_stocks = global_data[:10] if global_data else []
        
        logger.info(f"Passing to template - Oslo: {len(oslo_stocks)}, Global: {len(global_stocks)}, Crypto: {len(crypto_list)}")
        
        return render_template('test/testindex.html', 
                             oslo_stocks=oslo_stocks,
                             global_stocks=global_stocks, 
                             crypto_data=crypto_list)
    except Exception as e:
        logger.error(f"Error in testindex: {e}", exc_info=True)
        return f"Error loading test page: {e}", 500

@main.route('/testindex2')
def testindex2():
    """Alternative test homepage layout"""
    try:
        # Get comprehensive market data
        data_service = get_data_service()
        
        # Get data from service
        oslo_stocks = data_service.get_oslo_stocks()
        global_stocks = data_service.get_global_stocks()
        crypto_overview = data_service.get_crypto_overview()
        
        # Convert crypto dict to list if needed
        crypto_list = []
        if isinstance(crypto_overview, dict):
            crypto_list = list(crypto_overview.values())[:10]
        elif isinstance(crypto_overview, list):
            crypto_list = crypto_overview[:10]
        
        # Get trending stocks (check if method exists)
        trending_stocks = []
        try:
            trending_stocks = data_service.get_trending_stocks()[:8] if hasattr(data_service, 'get_trending_stocks') else []
        except Exception as e:
            logger.error(f"Error getting trending stocks: {e}")
            trending_stocks = []
        
        market_data = {
            'oslo_stocks': oslo_stocks[:15] if oslo_stocks else [],
            'global_stocks': global_stocks[:15] if global_stocks else [],
            'crypto_data': crypto_list,
            'trending_stocks': trending_stocks,
        }
        
        return render_template('test/testindex2.html', **market_data)
    except Exception as e:
        logger.error(f"Error in testindex2: {e}")
        return f"Error loading test page 2: {e}", 500


@main.route('/testindex3')
def testindex3():
    """Test market overview layout"""
    try:
        # Get comprehensive market data
        data_service = get_data_service()
        
        # Get data from service
        oslo_stocks = data_service.get_oslo_stocks()
        global_stocks = data_service.get_global_stocks()
        crypto_overview = data_service.get_crypto_overview()
        
        # Convert crypto dict to list if needed
        crypto_list = []
        if isinstance(crypto_overview, dict):
            crypto_list = list(crypto_overview.values())[:10]
        elif isinstance(crypto_overview, list):
            crypto_list = crypto_overview[:10]
        
        # Get trending stocks (check if method exists)
        trending_stocks = []
        try:
            trending_stocks = data_service.get_trending_stocks()[:8] if hasattr(data_service, 'get_trending_stocks') else []
        except:
            trending_stocks = []
        
        market_data = {
            'oslo_stocks': oslo_stocks[:15] if oslo_stocks else [],
            'global_stocks': global_stocks[:15] if global_stocks else [],
            'crypto_data': crypto_list,
            'trending_stocks': trending_stocks,
        }
        
        return render_template('testindex3.html', **market_data)
    except Exception as e:
        logger.error(f"Error in testindex3: {e}")
        return f"Error loading test page 3: {e}", 500