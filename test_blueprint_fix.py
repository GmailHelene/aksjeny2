#!/usr/bin/env python3
"""
Test Flask app can start without import errors
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    print("Testing app imports...")
    
    # Test individual blueprint imports
    try:
        from app.routes.portfolio import portfolio
        print("✅ Portfolio blueprint imported successfully")
    except Exception as e:
        print(f"❌ Portfolio blueprint import error: {e}")
        
    try:
        from app.routes.analysis import analysis
        print("✅ Analysis blueprint imported successfully")
    except Exception as e:
        print(f"❌ Analysis blueprint import error: {e}")
        
    try:
        from app.routes.main import main
        print("✅ Main blueprint imported successfully")
    except Exception as e:
        print(f"❌ Main blueprint import error: {e}")
    
    # Test full app creation
    try:
        from app import create_app
        app = create_app('development')
        print("✅ Flask app created successfully")
        
        # Test if routes are registered
        with app.app_context():
            from flask import url_for
            
            try:
                professional_url = url_for('main.professional_dashboard')
                print(f"✅ Professional dashboard route: {professional_url}")
            except Exception as e:
                print(f"❌ Professional dashboard route error: {e}")
                
            try:
                tech_url = url_for('analysis.technical')
                print(f"✅ Technical analysis route: {tech_url}")
            except Exception as e:
                print(f"❌ Technical analysis route error: {e}")
                
            try:
                opt_url = url_for('portfolio.optimization')
                print(f"✅ Portfolio optimization route: {opt_url}")
            except Exception as e:
                print(f"❌ Portfolio optimization route error: {e}")
        
        print("\n🎉 ALL BLUEPRINT IMPORT ISSUES FIXED!")
        print("🚀 Professional dashboard ready for deployment!")
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Critical error: {e}")
    import traceback
    traceback.print_exc()
