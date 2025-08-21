"""Simple test to verify app loads without errors"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    from app.extensions import db
    
    print("✓ Successfully imported app modules")
    
    app = create_app()
    print("✓ Successfully created app instance")
    
    with app.app_context():
        print("✓ App context works")
        
        # Try importing all main blueprints
        from app.routes.main import main
        from app.routes.auth import auth
        from app.routes.portfolio import portfolio
        from app.routes.stocks import stocks
        print("✓ All blueprints imported successfully")
        
        # Try importing models
        from app.models.user import User
        from app.models.forum import ForumPost
        print("✓ All models imported successfully")
        
    print("\n🎉 ALL TESTS PASSED - App loads without errors!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    pass
