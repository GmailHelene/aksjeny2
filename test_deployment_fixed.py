#!/usr/bin/env python3
"""Test script to validate Flask app startup without errors"""

import sys
import os

try:
    # Test app creation
    print("Testing Flask app creation...")
    
    # Add current directory to path
    sys.path.insert(0, '.')
    
    # Try to create the app
    from app import create_app
    app = create_app('development')
    print("SUCCESS: Flask app created without errors!")
    
    # Test if routes are registered
    with app.app_context():
        rules = list(app.url_map.iter_rules())
        print(f"Number of routes registered: {len(rules)}")
        
        # Check for analysis routes
        analysis_routes = [rule for rule in rules if rule.rule.startswith('/analysis')]
        print(f"Analysis routes found: {len(analysis_routes)}")
        for route in analysis_routes[:5]:  # Show first 5
            print(f"  {route.rule} -> {route.endpoint}")
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
