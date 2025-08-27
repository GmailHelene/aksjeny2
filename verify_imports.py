import os
import sys

# Check for circular imports in Flask app
print("Checking for circular imports in Flask app...")

try:
    # Try importing the create_app function
    print("Testing import of create_app...")
    from app.__init__ import create_app
    print("✓ Successfully imported create_app")
    
    # Try creating the app
    print("Testing app creation...")
    app = create_app('production')
    print("✓ Successfully created app")
    
    # Check if the app can run
    print("App ready to run")
    print("All imports verified successfully!")
    sys.exit(0)
except Exception as e:
    print(f"❌ Error detected: {e}")
    print(f"Type: {type(e).__name__}")
    
    # Suggest fix
    print("\nSuggested fix:")
    print("1. Run fix_circular_imports.sh (Linux/Mac) or fix_circular_imports.bat (Windows)")
    print("2. Deploy the app again")
    
    sys.exit(1)
