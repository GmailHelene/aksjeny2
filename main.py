import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

    # Import after environment variables are set
    from app import create_app

    # Railway typically injects PORT (often 5000). Default to 5000 for production compatibility.
    # Keep ability to override locally by exporting PORT=5002 if desired.
    port = int(os.environ.get('PORT', 5000))
    try:
        app = create_app('development')
        app.run(debug=True, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"ERROR during Flask app startup: {e}", flush=True)