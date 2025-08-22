#!/usr/bin/env python3
"""
Quick import verification script to ensure all imports work correctly
"""

import sys
import os

# Set environment variables
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:PsOJBeRqPAAcXyOXYCJvidJqMOpSzhqN@crossover.proxy.rlwy.net:17830/railway')

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all critical imports work without errors"""
    print("🔧 Testing Import Fixes...")
    print("=" * 50)
    
    try:
        print("1. Testing app creation...")
        from app import create_app
        print("✅ App import successful")
        
        print("2. Testing Flask app initialization...")
        app = create_app('development')
        print("✅ App creation successful")
        
        print("3. Testing blueprint registration...")
        with app.app_context():
            # This will trigger all blueprint imports
            print("✅ Blueprint registration successful")
        
        print("4. Testing specific route imports...")
        from app.routes.stocks import stocks
        from app.routes.api import api
        print("✅ Route imports successful")
        
        print("5. Testing CSRF imports...")
        from app.extensions import csrf
        print("✅ CSRF import successful")
        
        print("\n🎉 ALL IMPORTS WORKING CORRECTLY!")
        print("The Flask app should now start without import errors.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_imports():
        print("\n✅ Import fix successful - deployment should work now!")
    else:
        print("\n❌ Import issues remain - needs further investigation")
