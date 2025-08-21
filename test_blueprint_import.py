#!/usr/bin/env python3
"""
Minimal test to verify advanced_features blueprint can be imported
"""

def test_blueprint_import():
    """Test importing the advanced_features blueprint"""
    try:
        print("Testing advanced_features blueprint import...")
        
        # Test direct import of the blueprint
        from app.routes.advanced_features import advanced_features
        print("✅ Successfully imported advanced_features blueprint")
        
        # Test blueprint attributes
        if hasattr(advanced_features, 'name'):
            print(f"✅ Blueprint name: {advanced_features.name}")
        
        if hasattr(advanced_features, 'url_prefix'):
            print(f"✅ Blueprint URL prefix: {advanced_features.url_prefix}")
        
        # Test route registration
        print(f"✅ Blueprint has {len(advanced_features.deferred_functions)} routes")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_routes_init_import():
    """Test that routes/__init__.py properly imports advanced_features"""
    try:
        print("\nTesting routes/__init__.py import...")
        
        # Test the routes init import
        from app.routes import advanced_features
        print("✅ Successfully imported from app.routes")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import from routes/__init__.py failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=== BLUEPRINT IMPORT TEST ===")
    
    test1 = test_blueprint_import()
    test2 = test_routes_init_import()
    
    if test1 and test2:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ advanced_features blueprint can be imported and used")
        print("✅ Blueprint registration should work correctly")
    else:
        print("\n❌ TESTS FAILED!")
        print("Blueprint import or registration has issues")
