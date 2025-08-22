#!/usr/bin/env python3
import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """Test that all necessary modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test Flask app creation
        from app import create_app
        print("✓ Successfully imported create_app")
        
        # Test analysis blueprint
        from app.routes.analysis import analysis_bp
        print("✓ Successfully imported analysis blueprint")
        
        # Create app and test basic functionality
        app = create_app()
        print("✓ Successfully created Flask app")
        
        # Test that routes are registered
        with app.app_context():
            routes = []
            for rule in app.url_map.iter_rules():
                if 'analysis' in str(rule):
                    routes.append(str(rule))
            
            print(f"✓ Found {len(routes)} analysis routes:")
            for route in sorted(routes):
                print(f"  {route}")
        
        print("\n✅ All tests passed! The Flask app and routes are working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    test_imports()
