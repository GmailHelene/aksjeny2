import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # Provide sensible local fallbacks; real production should set via environment / .env
    os.environ.setdefault('EMAIL_USERNAME', 'support@example.com')
    os.environ.setdefault('EMAIL_PASSWORD', 'change-me')
    os.environ.setdefault('EMAIL_PORT', '587')
    os.environ.setdefault('EMAIL_SERVER', 'smtp.gmail.com')

    # If a DATABASE_URL isn't set locally, use sqlite instead of hard-coded prod credentials
    os.environ.setdefault('DATABASE_URL', 'sqlite:///app.db')

    # Decide environment: APP_ENV overrides FLASK_ENV. Default to development for local runs
    app_env = os.environ.get('APP_ENV') or os.environ.get('FLASK_ENV') or 'development'

    print(f"Starting Flask app with APP_ENV={app_env}...")
    from app import create_app

    port = int(os.environ.get('PORT', 5000))
    try:
        app = create_app(app_env)
        debug_enabled = app.config.get('DEBUG', False)
        app.run(debug=debug_enabled, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"ERROR during Flask app startup: {e}", flush=True)