#!/usr/bin/env python3
"""Test basic import functionality"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    print("Testing core imports...")
    from app import create_app
    print("✅ App creation import works")
    
    app = create_app()
    print("✅ App creation successful")
    
    with app.app_context():
        print("✅ App context works")
        
        # Test buffett service
        from app.services.buffett_analysis_service import BuffettAnalysisService
        print("✅ Buffett service import works")
        
        # Test analysis route
        from app.routes.analysis import analysis
        print("✅ Analysis blueprint import works")
        
    print("\n🎉 ALL IMPORTS WORKING!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
