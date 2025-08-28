from flask import Flask, render_template, request, jsonify, url_for, get_flashed_messages, g, redirect
from .config import config
from .extensions import db, login_manager, csrf, mail, socketio, cache
from .utils.market_open import is_oslo_bors_open, is_global_markets_open
from .utils.jinja_filters import jinja_filters
from flask_login import current_user
import logging
import os
from datetime import datetime
import atexit
import signal
import sys
from flask_wtf.csrf import CSRFProtect, CSRFError
from dotenv import load_dotenv
from flask_migrate import Migrate
import psutil
import time
import redis
from add_missing_columns import add_missing_columns
from add_browser_enabled_column import add_browser_enabled_column

# Load environment variables
load_dotenv()

# Export db for use in main.py
__all__ = ['create_app', 'db']

def create_app(config_class=None):
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Set strict_slashes to False globally
    app.url_map.strict_slashes = False
    
    # Set configuration
    if config_class is None:
        config_name = os.getenv('FLASK_ENV', 'default')
        app.config.from_object(config[config_name])
        app.logger.info(f"OK App created in {config_name} mode")
    elif isinstance(config_class, str):
        # Handle string config names (existing behavior)
        app.config.from_object(config[config_class])
        app.logger.info(f"OK App created in {config_class} mode")
    else:
        # Handle config class objects (for testing)
        app.config.from_object(config_class)
        app.logger.info(f"OK App created with custom config")
    
    # Initialize Flask extensions
    db.init_app(app)
    
    # Ensure notification columns exist
    with app.app_context():
        try:
            add_missing_columns()
            add_browser_enabled_column()
        except Exception as e:
            app.logger.error(f"Error adding missing columns: {e}")
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
    
    # Register WebSocket handlers
    try:
        from .routes import websocket_handlers
        app.logger.info("OK WebSocket handlers registered")
    except Exception as e:
        app.logger.warning(f"Failed to register WebSocket handlers: {e}")
    
    # Initialize Stripe before configuring stripe webhooks
    setup_stripe(app)
    
    # Initialize migrations
    migrate = Migrate(app, db)
    
    # Set up CSRF protection
    app.config['WTF_CSRF_TIME_LIMIT'] = None
    
    # Exempt API routes from CSRF protection
    csrf.exempt(lambda: request.endpoint and (
        request.endpoint.startswith('api.') or 
        '/api/' in request.path or
        request.endpoint.startswith('insider_trading.api_') or
        request.endpoint.startswith('notifications_bp.api_') or
        request.endpoint.startswith('watchlist_bp.api_') or
        request.endpoint.startswith('stocks.api_') or
        request.endpoint.startswith('news_bp.api_') or
        request.endpoint.startswith('analysis.api_') or
        request.endpoint == 'investment_analyzer.analyze_investments' or
        (request.endpoint.startswith('dashboard.') and '/api/' in request.path)
    ))
    
    # Custom unauthorized handler to redirect unauthenticated users to demo
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('main.demo'))
    
    app.logger.info("Custom unauthorized handler registered for Flask-Login")
    
    # Import models for database creation
    try:
        from . import models
        from .models import achievements  # Import achievements models explicitly
        app.logger.info("OK Database models imported successfully")
    except Exception as e:
        app.logger.error(f"ERROR Failed to import models: {e}")
        raise
    
    # Import cache service to initialize
    try:
        from .services.cache_service import cache_service
    except Exception as e:
        app.logger.warning(f"Cache service initialization failed: {e}")
    
    # Initialize price monitoring service (disabled in production to prevent context errors)
    is_railway = os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('PORT')  # Railway provides PORT
    if not is_railway:
        try:
            from .services.price_monitor_service import price_monitor
            price_monitor.start_monitoring(app)
            app.logger.info("OK Price monitoring service started")
        except Exception as e:
            app.logger.warning(f"Price monitoring service failed to start: {e}")
    else:
        app.logger.info("Price monitoring service disabled in Railway production environment")
    
    app.logger.info("DEBUG Starting try block for blueprint registration")
    try:
        # Log static endpoint
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':
                app.logger.info(f"Endpoint: {rule.endpoint} -> {rule}")
                break
        
        app.logger.info("DEBUG About to call register_blueprints")
        register_blueprints(app)
        app.logger.info("DEBUG register_blueprints completed successfully")
        setup_error_handlers(app)
        
        # Setup global access control middleware - DISABLED to fix redirect issues
        # from .middleware.access_control import apply_global_access_control
        # app.before_request(apply_global_access_control)
        
        # Import and setup security headers
        from .utils.security import setup_security_headers
        setup_security_headers(app)
        
        # Add CORS headers for GitHub Codespaces
        @app.after_request
        def after_request(response):
            """Add CORS headers to fix GitHub Codespaces issues"""
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
            return response
        
        # Register Jinja filters blueprint
        app.register_blueprint(jinja_filters)
        
        register_template_filters(app)
        
        # Add hasattr to Jinja2 globals to prevent template errors
        app.jinja_env.globals['hasattr'] = hasattr
        app.jinja_env.globals['getattr'] = getattr
        app.jinja_env.globals['isinstance'] = isinstance
        
        # Add free translation system template functions
        @app.template_global()
        def get_free_translation_js():
            from .utils.translation import get_free_translation_js
            return get_free_translation_js()
        
        @app.template_global() 
        def get_language_toggle_html():
            from .utils.translation import get_language_toggle_html
            return get_language_toggle_html()
        
        # Add translation functions to Jinja2 globals - Setup safely without app context dependency
        def setup_translation_service():
            """Setup translation service safely"""
            try:
                from .services.translation_service import t, get_current_language, get_supported_languages
                app.jinja_env.globals['t'] = t
                app.jinja_env.globals['get_current_language'] = get_current_language
                app.jinja_env.globals['get_supported_languages'] = get_supported_languages
                app.logger.info("OK Translation service integrated")
                return True
            except Exception as e:
                app.logger.warning(f"Translation service setup failed: {e}")
                return False
                
        # Try main translation service first
        translation_success = setup_translation_service()
        
        # If main service failed, setup fallbacks
        if not translation_success:
            try:
                from .utils.i18n import get_current_language as fallback_get_current_language
                app.jinja_env.globals['get_current_language'] = fallback_get_current_language
                app.logger.info("OK Fallback get_current_language added to Jinja2 globals")
            except Exception as e:
                app.logger.warning(f"Fallback get_current_language setup failed: {e}")
                # Final fallback: always provide a safe default
                def get_current_language():
                    return 'no'  # Default to Norwegian
                app.jinja_env.globals['get_current_language'] = get_current_language
                app.logger.info("OK Default get_current_language added to Jinja2 globals")
            
            # Always provide a dummy translation function if t is missing
            if 't' not in app.jinja_env.globals:
                def t(key, **kwargs):
                    fallback = kwargs.get('fallback', key)
                    return fallback
                app.jinja_env.globals['t'] = t
                app.logger.info("OK Default translation function 't' added to Jinja2 globals")

        # Add a global error handler for template rendering issues
        from jinja2 import TemplateError
        @app.errorhandler(TemplateError)
        def handle_template_error(error):
            app.logger.error(f"Template rendering error: {error}")
            # Return a safe error page instead of crashing
            return render_template('errors/500.html', error_message=str(error)), 500
        
        # Set up app context globals for templates
        @app.context_processor
        def inject_market_status():
            """Make market status, language, and translation function available in templates"""
            try:
                from .utils.i18n_simple import get_current_language, translate, _
                return {
                    'oslo_bors_open': is_oslo_bors_open(),
                    'global_markets_open': is_global_markets_open(),
                    'current_language': get_current_language(),
                    'translate': translate,
                    '_': _
                }
            except Exception as e:
                app.logger.warning(f"Error getting market status or language: {e}")
                return {
                    'oslo_bors_open': False,
                    'global_markets_open': False,
                    'current_language': 'no',
                    'translate': lambda x: x,
                    '_': lambda x: x
                }
        
        # Log all registered endpoints
        app.logger.info("Registered endpoints:")
        for rule in app.url_map.iter_rules():
            app.logger.info(f"Endpoint: {rule.endpoint} -> {rule}")
        
        # Initialize market data service
        def setup_market_data_service():
            """Setup real-time market data service safely"""
            try:
                from .services.market_data_service import MarketDataService
                # Initialize market data service
                app.market_data_service = MarketDataService()
                app.logger.info("OK Market data service initialized")
                return True
            except Exception as e:
                app.logger.warning(f"Market data service setup failed: {e}")
                return False
        
        # Setup market data service
        setup_market_data_service()
        
        app.logger.info("OK App initialization complete")
        
        # Initialize database tables within app context
        with app.app_context():
            try:
                if app.config.get('TESTING'):
                    db.create_all()
            except Exception as e:
                app.logger.warning(f"Database initialization skipped: {e}")
        
        # After app is created and configured:
        pass
    except Exception as e:
        app.logger.error(f"ERROR Critical error during app creation: {e}")
        raise
    # Register routes after try block
    from app.views.stocks import init_stocks_routes
    init_stocks_routes(app)
    from app.views.analysis import init_analysis_routes
    init_analysis_routes(app)
    from app.views.market_intel import init_market_intel_routes
    init_market_intel_routes(app)
    from app.views.profile import init_profile_routes
    init_profile_routes(app)
    # DISABLED: Conflicting with Blueprint registration - old views system
    # from app.views.advanced_analytics import init_advanced_analytics_routes
    # init_advanced_analytics_routes(app)
    
    # Registrer blueprints - FIX: Check if already registered before adding
    registered_blueprints = [bp.name for bp in app.blueprints.values()]
    
    # Only register external_data_bp if not already registered
    if 'external_data_bp' not in registered_blueprints and 'external_data' not in registered_blueprints:
        try:
            from app.views.external_data import external_data_bp
            app.register_blueprint(external_data_bp)
        except ImportError as e:
            app.logger.warning(f"Could not import external_data_bp from views: {e}")
    
    # Register other blueprints with same check
    if 'admin' not in registered_blueprints:
        from app.views.admin import admin_bp
        app.register_blueprint(admin_bp)
    
    if 'portfolio' not in registered_blueprints:
        from app.views.portfolio import portfolio_bp as views_portfolio_bp
        app.register_blueprint(views_portfolio_bp, url_prefix='/portfolio-views')
    
    if 'settings' not in registered_blueprints:
        from app.views.settings import settings_bp
        app.register_blueprint(settings_bp)
    
    if 'subscription' not in registered_blueprints:
        from app.views.subscription import subscription_bp
        app.register_blueprint(subscription_bp)
    
    return app

def register_blueprints(app):
    """Register all blueprints"""
    app.logger.info("DEBUG register_blueprints function called!")
    blueprints_registered = []
    
    # Core blueprints that must be registered
    try:
        from .routes.main import main
        app.register_blueprint(main)
        blueprints_registered.append('main')
        
        # Explicitly import and register portfolio blueprint
        from .routes.portfolio import portfolio
        app.register_blueprint(portfolio)
        blueprints_registered.append('portfolio')
        
        # Explicitly import and register pricing blueprint
        from .routes.pricing import pricing
        app.register_blueprint(pricing, url_prefix='/pricing')
        blueprints_registered.append('pricing')
        app.logger.info("OK Registered Pricing blueprint")
        
        # NOTE: stocks blueprint is registered via blueprint_configs below
        
        # Register Stripe blueprint
        try:
            from .routes.stripe_routes import stripe_bp
            app.register_blueprint(stripe_bp)
            blueprints_registered.append('stripe')
            app.logger.info("OK Registered Stripe blueprint")
        except ImportError as e:
            app.logger.warning(f"Could not import Stripe blueprint: {e}")
        
        # Register Auth blueprint  
        try:
            from .auth import auth
            app.register_blueprint(auth, url_prefix='/auth')
            blueprints_registered.append('auth')
            app.logger.info("OK Registered Auth blueprint")
        except ImportError as e:
            app.logger.warning(f"Could not import Auth blueprint: {e}")
        
        # Register Cache Management blueprint
        try:
            from .routes.cache_management import cache_bp
            app.register_blueprint(cache_bp)
            blueprints_registered.append('cache_management')
            app.logger.info("OK Registered Cache Management blueprint")
        except ImportError as e:
            app.logger.warning(f"Could not import Cache Management blueprint: {e}")
    except ImportError as e:
        app.logger.error(f"Failed to import main or portfolio blueprint: {e}")
        raise
    
    # Other blueprints with proper relative imports
    blueprint_configs = [
        ('.routes.stocks', 'stocks', '/stocks'),
        ('.routes.insider_trading', 'insider_trading', '/insider-trading'),
        ('.routes.api', 'api', None),
        ('.routes.analysis', 'analysis', '/analysis'),
        ('.routes.dashboard', 'dashboard', None),
        ('.routes.pro_tools', 'pro_tools', '/pro-tools'),
        ('.routes.market_intel', 'market_intel', '/market-intel'),
        # FIX: Comment out external_data here since it's registered later
        # ('.routes.external_data', 'external_data_bp', '/external-data'),
        ('.routes.backtest', 'backtest_bp', '/backtest'),
        ('.routes.seo_content', 'seo_content', '/content'),
        ('.routes.portfolio_advanced', 'portfolio_advanced', '/portfolio-advanced'),
        ('.routes.advanced_analytics', 'advanced_analytics', '/advanced-analytics'),
        ('.professional_analytics', 'analytics_bp', '/analytics'),
        ('.routes.news', 'news_bp', '/news'),
        ('.routes.health', 'health', '/health'),
        ('.routes.admin', 'admin', '/admin'),
        ('.routes.features', 'features', '/features'),
        ('.routes.blog', 'blog', '/blog'),
        ('.routes.investment_guides', 'investment_guides', '/investment-guides'),
        ('.routes.watchlist_advanced', 'watchlist_bp', '/watchlist'),
        ('.routes.price_alerts', 'price_alerts', '/price-alerts'),
        ('.routes.seo_sitemap', 'seo_sitemap', None),
        ('.routes.resources', 'resources_bp', '/resources'),
        ('.routes.investment_analyzer', 'investment_analyzer_bp', '/investment-analyzer'),
        ('.routes.advanced_features', 'advanced_features', '/advanced'),
        ('.routes.news_intelligence', 'news_intelligence', '/news-intelligence'),
        ('.routes.mobile_trading', 'mobile_trading', '/mobile-trading'),
        ('.routes.realtime_routes', 'realtime_bp', '/realtime'),
        ('.routes.realtime_websocket', 'realtime_data', None),
        ('.routes.portfolio_analytics', 'portfolio_analytics', '/portfolio-analytics'),
        ('.routes.notifications', 'notifications_bp', '/notifications/api'),
        ('.routes.notifications', 'notifications_web_bp', None),
        ('.routes.norwegian_intel', 'norwegian_intel', '/norwegian-intel'),
        ('.routes.daily_view', 'daily_view', '/daily-view'),
        ('.routes.forum', 'forum', '/forum'),
        ('.routes.sentiment_tracker', 'sentiment_tracker', '/sentiment'),
        ('.routes.oil_correlation', 'oil_correlation', '/oil-correlation'),
        ('.routes.achievements', 'achievements_bp', '/achievements'),
    ]
    
    app.logger.info(f"Starting to register {len(blueprint_configs)} blueprints...")
    
    for i, (module_path, blueprint_name, url_prefix) in enumerate(blueprint_configs):
        app.logger.info(f"Processing blueprint {i+1}/{len(blueprint_configs)}: {blueprint_name} from {module_path}")
        try:
            from importlib import import_module
            
            # Special debug logging for stocks and price_alerts
            if blueprint_name in ['stocks', 'price_alerts']:
                app.logger.info(f"Starting {blueprint_name} blueprint registration...")
                app.logger.info(f"Module path: {module_path}")
            
            module = import_module(module_path, package='app')
            blueprint = getattr(module, blueprint_name)
            
            # Register blueprint with appropriate prefix
            if url_prefix:
                app.register_blueprint(blueprint, url_prefix=url_prefix)
            else:
                app.register_blueprint(blueprint)
            blueprints_registered.append(blueprint_name)
            app.logger.info(f"Registered blueprint: {blueprint_name}")
            
            # Special confirmation for stocks and price_alerts
            if blueprint_name in ['stocks', 'price_alerts']:
                app.logger.info(f"{blueprint_name} blueprint registered successfully with prefix: {url_prefix}")
                
        except ImportError as e:
            app.logger.warning(f"Could not import {blueprint_name}: {e}")
            # Special error logging for stocks and price_alerts
            if blueprint_name in ['stocks', 'price_alerts']:
                app.logger.error(f"CRITICAL: {blueprint_name} blueprint import failed: {e}")
                import traceback
                app.logger.error(f"Full traceback: {traceback.format_exc()}")
        except Exception as e:
            app.logger.error(f"Error registering {blueprint_name}: {e}")
            # Special error logging for stocks and price_alerts
            if blueprint_name in ['stocks', 'price_alerts']:
                app.logger.error(f"CRITICAL: {blueprint_name} blueprint registration failed: {e}")
                import traceback
                app.logger.error(f"Full traceback: {traceback.format_exc()}")
    
    app.logger.info(f"OK Registered {len(blueprints_registered)} blueprints: {', '.join(blueprints_registered)}")
    
    # Register the realtime_api blueprint
    try:
        from .routes.realtime_api import realtime_api
        app.register_blueprint(realtime_api)
        blueprints_registered.append('realtime_api')
        app.logger.info("OK Registered realtime_api blueprint")
    except ImportError as e:
        app.logger.warning(f"Could not import realtime_api blueprint: {e}")
    
    # Register the watchlist_api blueprint
    try:
        from .routes.watchlist_api import watchlist_api
        app.register_blueprint(watchlist_api)
        blueprints_registered.append('watchlist_api')
        app.logger.info("OK Registered watchlist_api blueprint")
    except ImportError as e:
        app.logger.warning(f"Could not import watchlist_api blueprint: {e}")

def setup_production_database(app):
    """Setup database for production with proper error handling"""
    try:
        with app.app_context():
            # Create database tables if they don't exist
            db.create_all()
            app.logger.info("OK Database tables created/verified")
            
            # Set up exempt users for production
            setup_exempt_users(app)
            
    except Exception as e:
        app.logger.error(f"ERROR Production database setup failed: {e}")

def setup_exempt_users(app):
    """Set up exempt users for production"""
    try:
        from .models.user import User
        
        exempt_users = [
            {'email': 'helene721@gmail.com', 'username': 'helene721', 'password': 'aksjeradar2024'},
            {'email': 'tonjekit91@gmail.com', 'username': 'tonjekit91', 'password': 'aksjeradar2024'},
            {'email': 'helene@luxushair.com', 'username': 'helene_luxus', 'password': 'aksjeradar2024'},
            {'email': 'eiriktollan.berntsen@gmail.com', 'username': 'eirik_berntsen', 'password': 'aksjeradar2024'}
        ]
        
        for user_data in exempt_users:
            user = User.query.filter_by(email=user_data['email']).first()
            if not user:
                user = User(
                    email=user_data['email'],
                    username=user_data['username'],
                    subscription_type='premium',
                    is_admin=True,
                    trial_used=False
                )
                user.set_password(user_data['password'])
                db.session.add(user)
        
        db.session.commit()
        app.logger.info("OK Exempt users setup completed")
        
    except Exception as e:
        app.logger.error(f"ERROR Failed to setup exempt users: {e}")

def setup_stripe(app):
    """Initialize Stripe with proper error handling"""
    try:
        import stripe
        stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
        
        if stripe_secret_key:
            stripe.api_key = stripe_secret_key
            app.logger.info("OK Stripe initialized successfully")
        else:
            app.logger.warning("⚠️ Stripe secret key not found in environment")
        
        stripe_public_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
        
        if stripe_public_key:
            app.config['STRIPE_PUBLISHABLE_KEY'] = stripe_public_key
            app.logger.info("OK Stripe publishable key configured")
        else:
            app.logger.info("ℹ️ Stripe publishable key not configured - payment features disabled")
            app.config['STRIPE_PUBLISHABLE_KEY'] = None
            
    except ImportError:
        app.logger.warning("⚠️ Stripe not installed")
    except Exception as e:
        app.logger.error(f"ERROR Stripe initialization failed: {e}")

def setup_error_handlers(app):
    """Setup custom error handlers"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        # Don't handle static file 404s - let Flask handle them naturally
        if request.path.startswith('/static/'):
            return error, 404
        
        # Return JSON for API requests
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Endepunkt ikke funnet',
                'status_code': 404
            }), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        # Return JSON for API requests
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Intern serverfeil',
                'status_code': 500
            }), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(429)
    def rate_limit_error(error):
        """Handle rate limit errors"""
        app.logger.warning(f'Rate limit exceeded: {error}')
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Rate limit exceeded',
                'status_code': 429,
                'retry_after': 60
            }), 429
        else:
            return render_template('errors/500.html'), 429
    
    # Add database error handler
    from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        app.logger.error(f'Database error: {error}')
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Database feil',
                'status_code': 500
            }), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        app.logger.error(f'Database integrity error: {error}')
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Database integritets feil',
                'status_code': 500
            }), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(OperationalError)
    def operational_error(error):
        app.logger.error(f'Database operational error: {error}')
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Database operasjonsfeil',
                'status_code': 500
            }), 500
        return render_template('errors/500.html'), 500
    
    # Add TemplateNotFound error handler
    from jinja2 import TemplateNotFound
    @app.errorhandler(TemplateNotFound)
    def template_not_found_error(error):
        app.logger.error(f"Template not found: {error}")
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': f'Template ikke funnet: {error}',
                'status_code': 500
            }), 500
        return render_template('errors/500.html', 
                             error_message=f"Template ikke funnet: {error}"), 500
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        """Handle CSRFError specifically"""
        from flask import redirect, url_for, flash
        
        app.logger.warning(f'CSRFError: {str(e)}')
        
        # Return JSON for API requests
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'CSRF sikkerhetsfeil',
                'status_code': 400
            }), 400
        
        flash('Sikkerhetsfeil: Vennligst prøv igjen.', 'error')
        
        if 'checkout' in request.path:
            return redirect(url_for('main.subscription'))
        elif 'login' in request.path:
            return redirect(url_for('main.login'))
        elif 'price-alerts' in request.path:
            return redirect(url_for('price_alerts.create'))
        else:
            return redirect(url_for('main.index'))

def register_template_filters(app):
    """Register custom template filters"""
    from .utils.filters import register_filters
    
    # Register filters from utils/filters.py
    register_filters(app)
    
    @app.template_filter('currency')
    def currency_filter(value):
        """Format number as currency"""
        if value is None:
            return "—"
        try:
            return f"{float(value):,.2f} NOK"
        except (ValueError, TypeError):
            return str(value)
    
    @app.template_filter('percentage')
    def percentage_filter(value):
        """Format number as percentage"""
        if value is None:
            return "—"
        try:
            return f"{float(value):.2f}%"
        except (ValueError, TypeError):
            return str(value)

    @app.template_filter('datetimeformat')
    def datetimeformat_filter(value):
        """Format datetime for display"""
        if value is None:
            return "—"
        try:
            if isinstance(value, str):
                # Parse ISO format datetime
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            else:
                dt = value
            return dt.strftime('%d.%m.%Y kl. %H:%M')
        except (ValueError, TypeError):
            return str(value)

    @app.context_processor
    def inject_utils():
        """Make utility functions available in templates"""
        from flask_wtf.csrf import generate_csrf
        return dict(
            now=datetime.utcnow,
            datetime=datetime,
            csrf_token=generate_csrf
        )
    
    @app.template_filter('nn')
    def nn_filter(value, decimals=2, suffix=''):
        """Norwegian number formatting filter"""
        if value is None:
            return "—"
        try:
            if isinstance(value, str):
                value = float(value)
            formatted = f"{value:,.{decimals}f}".replace(',', ' ').replace('.', ',')
            if suffix:
                return f"{formatted} {suffix}"
            return formatted
        except (ValueError, TypeError):
            return str(value) if value is not None else "—"

    @app.template_filter('pct')
    def pct_filter(value):
        """Format as percentage"""
        if value is None:
            return "—"
        try:
            formatted = f"{float(value):.2f}".replace('.', ',')
            return f"{formatted} %"
        except (ValueError, TypeError):
            return str(value) if value is not None else "—"

    @app.template_filter('format_number')
    def format_number_filter(value):
        """Format number for display"""
        if value is None:
            return "—"
        try:
            if isinstance(value, str):
                value = float(value)
            
            # Handle very large numbers (millions, billions)
            if abs(value) >= 1e9:
                return f"{value/1e9:.1f}B"
            elif abs(value) >= 1e6:
                return f"{value/1e6:.1f}M"
            elif abs(value) >= 1e3:
                return f"{value/1e3:.1f}K"
            else:
                return f"{value:,.0f}"
        except (ValueError, TypeError):
            return str(value) if value is not None else "—"

## View registration now handled via init_*_routes functions after app creation

# Remove default app instance creation to prevent circular imports
# The app instance should be created explicitly in main.py or run.py
# app = create_app()

# Export only the factory function and db
__all__ = ['create_app', 'db']
