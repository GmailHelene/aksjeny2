"""Quick test to ensure app loads without IndentationError"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing app creation...")
    from app import create_app
    
    print("✓ Imported create_app successfully")
    
    app = create_app()
    print("✓ Created app instance successfully")
    
    with app.app_context():
        print("✓ App context works")
        
        # Test importing the stocks blueprint specifically
        from app.routes.stocks import stocks
        print("✓ Imported stocks blueprint successfully")
        
        # Test all blueprints
        from app.routes.main import main
        from app.routes.auth import auth  
        from app.routes.portfolio import portfolio
        print("✓ All blueprints imported successfully")
        
    print("\n🎉 SUCCESS: No IndentationError - App loads correctly!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    pass
