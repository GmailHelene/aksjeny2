#!/usr/bin/env python3
"""
Quick test to verify the deployment error is fixed
"""
import sys
import os

def test_stocks_import():
    """Test that stocks blueprint can be imported without NameError"""
    try:
        # Add current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Test importing the stocks blueprint
        from app.routes.stocks import stocks
        print("✅ SUCCESS: stocks blueprint imported successfully!")
        print(f"✅ Blueprint name: {stocks.name}")
        print(f"✅ Blueprint url_prefix: {stocks.url_prefix}")
        return True
        
    except NameError as e:
        print(f"❌ FAILED: NameError still exists: {e}")
        return False
    except ImportError as e:
        print(f"❌ FAILED: ImportError: {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {e}")
        return False

def test_app_creation():
    """Test that Flask app can be created"""
    try:
        from app import create_app
        app = create_app('development')
        print("✅ SUCCESS: Flask app created successfully!")
        return True
    except Exception as e:
        print(f"❌ FAILED: App creation failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing deployment fix...")
    print("=" * 50)
    
    success1 = test_stocks_import()
    success2 = test_app_creation()
    
    print("=" * 50)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED! Deployment error is fixed!")
        sys.exit(0)
    else:
        print("💥 TESTS FAILED! Deployment error still exists!")
        sys.exit(1)
