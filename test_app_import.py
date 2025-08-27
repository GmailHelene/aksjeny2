#!/usr/bin/env python3
"""
Test script to verify the application can be imported without circular import errors
"""
import sys
import os

# Test imports
try:
    print("Testing import from app.__init__...")
    from app.__init__ import create_app
    print("✓ Successfully imported create_app from app.__init__")

    print("\nCreating app instance...")
    app = create_app('development')
    print("✓ Successfully created app instance")

    print("\nApplication can be imported and initialized correctly!")
    print("The circular import error has been fixed.")
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Type: {type(e).__name__}")
    print(f"Module: {e.__module__}")
    
    # Print traceback for debugging
    import traceback
    traceback.print_exc()
    
    sys.exit(1)

sys.exit(0)
