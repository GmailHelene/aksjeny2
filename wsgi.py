#!/usr/bin/env python3
"""
WSGI entry point for Railway deployment
"""
import os
import sys
import importlib.util

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set production environment
os.environ.setdefault('FLASK_ENV', 'production')

try:
    # Import the create_app function directly from __init__.py file
    # This avoids the circular import issue
    init_path = os.path.join(os.path.dirname(__file__), 'app', '__init__.py')
    spec = importlib.util.spec_from_file_location("app_init", init_path)
    app_init = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_init)
    
    # Create the Flask app using the imported function
    app = app_init.create_app('production')
    
    # Ensure app is ready
    with app.app_context():
        from app.extensions import db
        # Create tables if they don't exist
        try:
            db.create_all()
            print("✅ Database tables initialized")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
    
    print("✅ WSGI app initialized successfully")

except Exception as e:
    print(f"❌ WSGI app initialization failed: {e}")
    import traceback
    traceback.print_exc()
    raise

# Export for gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
