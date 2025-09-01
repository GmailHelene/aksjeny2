#!/usr/bin/env python3

"""Test script for Warren Buffett analysis route"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_login import LoginManager

def create_test_app():
    """Create a minimal Flask app to test warren buffett route"""
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
        user.email = 'test@example.com'
        return user
    
    # Test route to check analysis blueprint import
    @app.route('/test-warren-buffett-import')
    def test_warren_buffett_import():
        try:
            from app.routes.analysis import analysis
            app.register_blueprint(analysis, url_prefix='/analysis')
            return {'status': 'OK', 'message': 'Warren Buffett analysis blueprint registered successfully'}
        except Exception as e:
            import traceback
            return {'status': 'ERROR', 'message': str(e), 'traceback': traceback.format_exc()}, 500
    
    # Test route to directly test warren buffett function
    @app.route('/test-warren-buffett-function')
    def test_warren_buffett_function():
        try:
            from app.routes.analysis import warren_buffett
            return {'status': 'OK', 'message': 'Warren Buffett function imported successfully'}
        except Exception as e:
            import traceback
            return {'status': 'ERROR', 'message': str(e), 'traceback': traceback.format_exc()}, 500
    
    return app

if __name__ == '__main__':
    app = create_test_app()
    print("Starting Warren Buffett test server on http://localhost:5005...")
    app.run(host='0.0.0.0', port=5005, debug=True)
