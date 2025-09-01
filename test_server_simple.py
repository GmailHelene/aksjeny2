#!/usr/bin/env python3

"""Simple test server to verify portfolio route functionality"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_login import LoginManager

def create_test_app():
    """Create a minimal Flask app to test portfolio routes"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True
    
    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        # Mock user loader for testing
        from types import SimpleNamespace
        user = SimpleNamespace()
        user.id = user_id
        user.is_authenticated = True
        user.is_active = True
        user.is_anonymous = False
        return user
    
    # Test route to verify server works
    @app.route('/test')
    def test_route():
        return {'status': 'OK', 'message': 'Test server is running'}
    
    # Test route to check portfolio module import
    @app.route('/test-portfolio-import')
    def test_portfolio_import():
        try:
            from app.routes.portfolio import portfolio
            return {'status': 'OK', 'message': 'Portfolio module imported successfully'}
        except Exception as e:
            return {'status': 'ERROR', 'message': str(e)}, 500
    
    return app

if __name__ == '__main__':
    app = create_test_app()
    print("Starting test server on http://localhost:5003...")
    app.run(host='0.0.0.0', port=5003, debug=True)
