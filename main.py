import os
import sys
import importlib.util

if __name__ == '__main__':
    os.environ.setdefault('EMAIL_USERNAME', 'support@luxushair.com')
    os.environ.setdefault('EMAIL_PASSWORD', 'suetozoydejwntii')
    os.environ.setdefault('EMAIL_PORT', '587')
    os.environ.setdefault('EMAIL_SERVER', 'imap.gmail.com')
    os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

    print("Starting Flask app...")
    print("Access forgot password at: http://localhost:5002/forgot-password")
    print("Access reset password with token from email")
    print("\nServer starting...")

    # Import the create_app function directly from __init__.py file
    # This avoids the circular import issue
    init_path = os.path.join(os.path.dirname(__file__), 'app', '__init__.py')
    spec = importlib.util.spec_from_file_location("app_init", init_path)
    app_init = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_init)

    port = int(os.environ.get('PORT', 5002))
    try:
        app = app_init.create_app('development')
        app.run(debug=True, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"ERROR during Flask app startup: {e}", flush=True)