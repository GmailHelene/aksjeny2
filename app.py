import os
import sys
import importlib.util

# Railway production startup script
os.environ.setdefault('EMAIL_USERNAME', 'support@luxushair.com')
os.environ.setdefault('EMAIL_PASSWORD', 'suetozoydejwntii')
os.environ.setdefault('EMAIL_PORT', '587')
os.environ.setdefault('EMAIL_SERVER', 'imap.gmail.com')
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

print("Starting Flask app for Railway deployment...")

# Import the create_app function directly from __init__.py file
# This avoids the circular import issue
init_path = os.path.join(os.path.dirname(__file__), 'app', '__init__.py')
spec = importlib.util.spec_from_file_location("app_init", init_path)
app_init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_init)

# Create the Flask app using the imported function
app = app_init.create_app('production')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=False, host='0.0.0.0', port=port)
else:
    # For Railway/WSGI deployment
    application = app