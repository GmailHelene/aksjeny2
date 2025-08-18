# Decorators module for access control and functionality
from functools import wraps
from flask import current_app, request, jsonify, redirect, url_for
from flask_login import current_user
import logging

logger = logging.getLogger(__name__)

def access_required(f):
    """
    Decorator that checks if user has access to premium features.
    For now, requires login (subscription check disabled until User model is enhanced).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # If user is not logged in, require login
            if not current_user.is_authenticated:
                if request.is_json:
                    return jsonify({'error': 'Authentication required'}), 401
                return redirect(url_for('auth.login'))
            
            # TODO: Implement proper subscription check when User model is enhanced
            # For now, require login only (security baseline)
            logger.debug(f"Access granted to authenticated user for {request.endpoint}")
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.warning(f"Access check failed: {e}")
            # Security fix: Fail closed - deny access if check fails
            if request.is_json:
                return jsonify({
                    'error': 'Access control error',
                    'message': 'Unable to verify access permissions'
                }), 500
            return redirect(url_for('main.demo'))
    
    return decorated_function