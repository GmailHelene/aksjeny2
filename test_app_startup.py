#!/usr/bin/env python3
"""Test if the app can start without syntax errors"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing app startup...")
    
    # Try to import the app factory
    from app import create_app
    print("✅ App factory imported successfully")
    
    # Try to create the app
    app = create_app()
    print("✅ App created successfully")
    
    # Check if we can get the blueprint names
    blueprint_names = list(app.blueprints.keys())
    print(f"✅ Blueprints registered: {blueprint_names}")
    
    print("\n🎉 APP CAN START SUCCESSFULLY!")
    print("The syntax error has been fixed!")
    
except SyntaxError as e:
    print(f"❌ SYNTAX ERROR: {e}")
    print(f"File: {e.filename}")
    print(f"Line: {e.lineno}")
    print(f"Text: {e.text}")
    
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("This is expected in dev environment")
    
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
