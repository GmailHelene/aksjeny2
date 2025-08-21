#!/usr/bin/env python3
"""
Debug script to test authentication system
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_auth_imports():
    """Test if auth modules can be imported"""
    print("🔍 TESTING AUTH SYSTEM IMPORTS")
    print("=" * 50)
    
    try:
        print("✓ Testing app creation...")
        from app import create_app
        print("✓ App factory imported successfully")
        
        print("✓ Testing auth blueprint import...")
        from app.auth import auth
        print("✓ Auth blueprint imported successfully")
        
        print("✓ Testing forms import...")
        from app.forms import LoginForm, RegistrationForm
        print("✓ Forms imported successfully")
        
        print("✓ Testing User model...")
        from app.models.user import User
        print("✓ User model imported successfully")
        
        print("✓ Testing extensions...")
        from app.extensions import db, login_manager
        print("✓ Extensions imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_creation():
    """Test if app can be created"""
    print("\n🔍 TESTING APP CREATION")
    print("=" * 50)
    
    try:
        from app import create_app
        app = create_app('development')
        print("✓ App created successfully")
        
        with app.app_context():
            print("✓ App context created")
            
            # Test database connection
            from app.extensions import db
            try:
                # Simple query to test connection
                result = db.session.execute(db.text("SELECT 1"))
                print("✓ Database connection working")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                
            # Test auth routes registration
            auth_routes = [rule for rule in app.url_map.iter_rules() if rule.endpoint and rule.endpoint.startswith('auth.')]
            print(f"✓ Auth routes found: {len(auth_routes)}")
            for route in auth_routes:
                print(f"  - {route.rule} -> {route.endpoint}")
        
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_existence():
    """Test if auth templates exist"""
    print("\n🔍 TESTING TEMPLATE EXISTENCE")
    print("=" * 50)
    
    import os
    template_dir = os.path.join(os.path.dirname(__file__), 'app', 'templates')
    
    required_templates = ['login.html', 'register.html', 'base.html']
    
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✓ {template} exists")
        else:
            print(f"❌ {template} missing at {template_path}")

def main():
    """Main test function"""
    print("🚀 AUTH SYSTEM DIAGNOSTIC TEST")
    print("=" * 50)
    
    # Test 1: Import tests
    if not test_auth_imports():
        print("\n❌ FAILED: Import test failed")
        return False
    
    # Test 2: App creation
    if not test_app_creation():
        print("\n❌ FAILED: App creation failed")
        return False
        
    # Test 3: Template existence
    test_template_existence()
    
    print("\n🎉 ALL TESTS COMPLETED")
    print("Check above for any ❌ errors that need fixing")
    return True

if __name__ == '__main__':
    main()
