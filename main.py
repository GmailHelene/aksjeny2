import os
from app import create_app

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

    port = int(os.environ.get('PORT', 5002))
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=port)