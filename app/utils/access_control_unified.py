"""
Fixes demo redirect issues by creating a unified access control system.
This replaces conflicting access control systems that cause redirect loops.
"""

from flask import current_app, redirect, url_for, request, flash
from flask_login import current_user
from functools import wraps
import logging

# Exempt users who always get full access
EXEMPT_EMAILS = {
    'helene@luxushair.com', 
    'helene721@gmail.com', 
    'eiriktollan.berntsen@gmail.com',
    'tonjekit91@gmail.com'
}

# Always accessible endpoints (no authentication required)
ALWAYS_ACCESSIBLE = {
    'main.index',
    'main.demo', 
    'main.login',
    'main.register',
    'main.logout',
    'main.privacy',
    'main.privacy_policy',
    'main.contact',
    'main.contact_submit',
    'main.forgot_password',
    'main.reset_password',
    'main.terms',
    'main.about',
    'main.help',
    'main.features',
    'main.translation_help',
    'main.set_language',
    'static',
    'main.service_worker',
    'main.manifest',
    'main.favicon',
    'main.offline',
    'main.offline_html'
}

# Demo accessible endpoints (available for trial users)
DEMO_ACCESSIBLE = {
    'stocks.index',
    'stocks.search', 
    'stocks.list_currency',
    'analysis.index',
    'analysis.warren_buffett',  # Moved from premium to demo
    'market.overview',
    'market.sectors',
    'market_intel.insider_trading',
    'portfolio.portfolio_index',  # Basic portfolio view
    'portfolio.index',  # Basic portfolio access
    'main.profile',  # Profile page access
    'price_alerts.index'  # Basic alerts view
}

# Premium endpoints (require active subscription)
PREMIUM_ONLY = {
    'stocks.details',
    'stocks.list_stocks', 
    'stocks.list_oslo',
    'stocks.global_list',
    'stocks.list_crypto',
    'stocks.compare',
    'analysis.ai',
    'analysis.technical',
    'analysis.prediction',
    'analysis.market_overview',
    'portfolio.create_portfolio',
    'portfolio.view_portfolio',
    'portfolio.transactions',
    'market_intel.index'
}


def is_exempt_user():
    """Check if current user is exempt from access restrictions"""
    return (current_user.is_authenticated and 
            hasattr(current_user, 'email') and 
            current_user.email in EXEMPT_EMAILS)


def has_active_subscription():
    """Check if current user has an active subscription"""
    if not current_user.is_authenticated:
        return False
        
    # Exempt users always have access
    if is_exempt_user():
        return True
        
    # Check subscription methods
    if hasattr(current_user, 'has_active_subscription'):
        return current_user.has_active_subscription()
        
    if hasattr(current_user, 'subscription_type'):
        return current_user.subscription_type in ['premium', 'pro', 'yearly', 'lifetime', 'active']
        
    return False


def get_access_level():
    """
    Get current user's access level
    Returns: 'admin', 'premium', 'demo', or 'none'
    """
    if is_exempt_user():
        return 'admin'
        
    if has_active_subscription():
        return 'premium'
        
    if current_user.is_authenticated:
        return 'demo'  # Authenticated users get demo access
        
    return 'none'


def check_endpoint_access(endpoint):
    """
    Check if current user can access the given endpoint
    Returns: (allowed: bool, redirect_to: str|None, message: str|None)
    """
    # Always accessible endpoints
    if endpoint in ALWAYS_ACCESSIBLE:
        return True, None, None
        
    access_level = get_access_level()
    
    # Admin/exempt users can access everything
    if access_level == 'admin':
        return True, None, None
        
    # Premium users can access everything except admin-only
    if access_level == 'premium':
        return True, None, None
        
    # Demo users can access demo endpoints
    if access_level == 'demo':
        if endpoint in DEMO_ACCESSIBLE:
            return True, None, None
        elif endpoint in PREMIUM_ONLY:
            return False, 'pricing.index', 'Denne funksjonen krever premium-abonnement'
        else:
            # Unknown endpoint - allow for backwards compatibility
            return True, None, None
            
    # Unauthenticated users - redirect to demo for most things
    if access_level == 'none':
        if endpoint in DEMO_ACCESSIBLE or endpoint in PREMIUM_ONLY:
            return False, 'main.demo', 'Vennligst logg inn eller prøv demo-versjonen'
        else:
            return False, 'main.login', 'Vennligst logg inn for å fortsette'


def unified_access_required(f):
    """
    Unified access control decorator that replaces all other access decorators
    Prevents redirect loops by using consistent logic
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip check if we're already on an always-accessible page
        if request.endpoint in ALWAYS_ACCESSIBLE:
            return f(*args, **kwargs)
            
        # Prevent redirect loops for demo page
        if request.endpoint == 'main.demo':
            return f(*args, **kwargs)
            
        # Check access
        allowed, redirect_to, message = check_endpoint_access(request.endpoint)
        
        if allowed:
            return f(*args, **kwargs)
        else:
            if message:
                flash(message, 'info')
            
            # Prevent infinite redirects
            if redirect_to and redirect_to != request.endpoint:
                try:
                    current_app.logger.info(f"Access denied for {request.endpoint}, redirecting to {redirect_to}")
                    return redirect(url_for(redirect_to))
                except Exception as e:
                    current_app.logger.error(f"Redirect error: {e}")
                    # Fallback to safe redirect
                    return redirect(url_for('main.index'))
            else:
                # Fallback for edge cases
                return redirect(url_for('main.index'))
                
    return decorated_function


def safe_demo_access(f):
    """
    Safe demo access decorator that prevents redirect loops
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Always allow access to demo page to prevent loops
        if request.endpoint == 'main.demo':
            return f(*args, **kwargs)
            
        # Check if user should have access to this demo feature
        access_level = get_access_level()
        
        if access_level in ['admin', 'premium', 'demo']:
            return f(*args, **kwargs)
        else:
            # Unauthenticated users can still access demo pages
            return f(*args, **kwargs)
            
    return decorated_function


def premium_required(f):
    """
    Decorator for premium-only features - redirects to pricing
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_level = get_access_level()
        
        if access_level in ['admin', 'premium']:
            return f(*args, **kwargs)
        else:
            flash('Denne funksjonen krever premium-abonnement', 'warning')
            if current_user.is_authenticated:
                return redirect(url_for('pricing.index'))
            else:
                return redirect(url_for('main.login', next=request.url))
                
    return decorated_function


def api_access_required(f):
    """
    API-specific access control with JSON responses
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import jsonify
        
        access_level = get_access_level()
        
        # API endpoints require at least demo access
        if access_level == 'none':
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please log in to access this API',
                'code': 'LOGIN_REQUIRED'
            }), 401
            
        # Check specific endpoint requirements
        allowed, _, _ = check_endpoint_access(request.endpoint)
        
        if not allowed:
            return jsonify({
                'error': 'Access denied',
                'message': 'This feature requires premium subscription',
                'code': 'PREMIUM_REQUIRED'
            }), 403
            
        return f(*args, **kwargs)
        
    return decorated_function


# Logging function for debugging
def log_access_attempt(endpoint, user_id=None, access_level=None):
    """Log access attempts for debugging"""
    try:
        current_app.logger.info(
            f"Access attempt: endpoint={endpoint}, "
            f"user_id={user_id or 'anonymous'}, "
            f"access_level={access_level or get_access_level()}"
        )
    except Exception:
        pass  # Don't break on logging errors


# Export commonly used functions
__all__ = [
    'unified_access_required',
    'safe_demo_access', 
    'premium_required',
    'api_access_required',
    'get_access_level',
    'check_endpoint_access',
    'is_exempt_user',
    'has_active_subscription'
]
