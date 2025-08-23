#!/usr/bin/env python3
"""
Debug script to check endpoint registration
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from app import create_app
    
    app = create_app('development')
    
    with app.app_context():
        print("🔍 REGISTERED ENDPOINTS:")
        
        # List all registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith('main.'):
                routes.append(f"  ✅ {rule.endpoint} -> {rule.rule}")
        
        if routes:
            print("\n📊 MAIN BLUEPRINT ROUTES:")
            for route in sorted(routes):
                print(route)
        else:
            print("❌ No main blueprint routes found!")
        
        # Check specifically for professional_dashboard
        found_professional = False
        for rule in app.url_map.iter_rules():
            if 'professional_dashboard' in rule.endpoint:
                print(f"\n✅ FOUND: {rule.endpoint} -> {rule.rule}")
                found_professional = True
        
        if not found_professional:
            print("\n❌ professional_dashboard endpoint NOT FOUND!")
            
        # Check for conflicts
        print(f"\n🔍 CHECKING FOR DASHBOARD CONFLICTS:")
        dashboard_routes = []
        for rule in app.url_map.iter_rules():
            if 'dashboard' in rule.endpoint:
                dashboard_routes.append(f"  {rule.endpoint} -> {rule.rule}")
        
        if dashboard_routes:
            print("📊 DASHBOARD ROUTES FOUND:")
            for route in sorted(dashboard_routes):
                print(route)
        else:
            print("❌ No dashboard routes found!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
