#!/usr/bin/env python3
"""Simple test to verify pro_tools blueprint import and registration"""

def test_pro_tools_import():
    """Test if pro_tools blueprint can be imported successfully"""
    try:
        print("Testing pro_tools blueprint import...")
        
        # Try to import the blueprint directly
        from app.routes.pro_tools import pro_tools
        print(f"✅ Successfully imported pro_tools blueprint: {pro_tools}")
        print(f"Blueprint name: {pro_tools.name}")
        print(f"Blueprint url_prefix: {getattr(pro_tools, 'url_prefix', 'None')}")
        
        # Check that the blueprint has routes
        print(f"Blueprint has {len(pro_tools.deferred_functions)} deferred functions")
        
        # Test creating a minimal Flask app and registering the blueprint
        from flask import Flask
        test_app = Flask(__name__)
        test_app.register_blueprint(pro_tools)
        
        print(f"✅ Blueprint registered successfully in test app")
        
        # Check routes
        with test_app.app_context():
            pro_routes = [rule.rule for rule in test_app.url_map.iter_rules() 
                         if 'pro-tools' in rule.rule]
            print(f"Pro-tools routes in test app: {pro_routes}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ General error: {e}")
        return False

if __name__ == "__main__":
    success = test_pro_tools_import()
    if success:
        print("\n✅ pro_tools blueprint test passed!")
    else:
        print("\n❌ pro_tools blueprint test failed!")
