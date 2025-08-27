#!/usr/bin/env python3
"""
Simple test script to verify Flask app can start without errors
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

try:
    print("Testing app import...")
    from app import create_app
    print("✓ App import successful")

    print("Testing app creation...")
    app = create_app('development')
    print("✓ App creation successful")

    print("Testing blueprint registration...")
    with app.app_context():
        print("✓ App context created successfully")

    print("\n🎉 All tests passed! Flask app should start successfully.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
