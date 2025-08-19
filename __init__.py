from flask import Flask
from .routes import main as main_blueprint
from .api import api as api_blueprint

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Configure CSRF for AJAX requests
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for now to fix issues
    
    return app