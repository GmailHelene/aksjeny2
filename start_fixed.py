#!/usr/bin/env python3
"""
Fixed deployment starter for Flask app that avoids circular imports
"""
import os
import sys

# Add the current directory to the Python path
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)

# Set required environment variables
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('EMAIL_USERNAME', 'support@luxushair.com')
os.environ.setdefault('EMAIL_PASSWORD', 'suetozoydejwntii')
os.environ.setdefault('EMAIL_PORT', '587')
os.environ.setdefault('EMAIL_SERVER', 'imap.gmail.com')
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

print("Starting Flask app with fixed import system...")

# Import modules before importing app
# This prevents the circular import issue
import flask
import flask_login
import flask_wtf
from flask import Flask

# Import the create_app function from the app package
# We're using a specific import technique to avoid conflicts
sys.path.remove(base_path)  # Temporarily remove base path
from app.__init__ import create_app  # Import from package

# Create the application
app = create_app('production')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=False, host='0.0.0.0', port=port)
else:
    # For WSGI deployment
    application = app
