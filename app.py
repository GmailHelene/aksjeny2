import os
from app.__init__ import create_app

# Railway production startup script
os.environ.setdefault('EMAIL_USERNAME', 'support@luxushair.com')
os.environ.setdefault('EMAIL_PASSWORD', 'suetozoydejwntii')
os.environ.setdefault('EMAIL_PORT', '587')
os.environ.setdefault('EMAIL_SERVER', 'imap.gmail.com')
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

print("Starting Flask app for Railway deployment...")

# Create the Flask app
app = create_app('production')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=False, host='0.0.0.0', port=port)
else:
    # For Railway/WSGI deployment
    application = app