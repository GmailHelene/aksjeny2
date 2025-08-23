#!/usr/bin/env python3
"""
Debug analysis blueprint registration
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from app import create_app
    
    app = create_app('development')
    
    with app.app_context():
        print("🔍 ANALYSIS BLUEPRINT DEBUG")
        print("=" * 50)
        
        # List all registered analysis routes
        analysis_routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith('analysis.'):
                analysis_routes.append(f"  ✅ {rule.endpoint} -> {rule.rule}")
        
        if analysis_routes:
            print(f"📊 REGISTERED ANALYSIS ROUTES ({len(analysis_routes)}):")
            for route in sorted(analysis_routes):
                print(route)
        else:
            print("❌ NO ANALYSIS ROUTES FOUND!")
        
        # Check specifically for market_overview
        market_routes = []
        for rule in app.url_map.iter_rules():
            if 'market' in rule.endpoint.lower():
                market_routes.append(f"  {rule.endpoint} -> {rule.rule}")
        
        if market_routes:
            print(f"\n🔍 MARKET-RELATED ROUTES:")
            for route in sorted(market_routes):
                print(route)
        
        # Test if we can import analysis blueprint directly
        print(f"\n🧪 TESTING DIRECT IMPORT:")
        try:
            from app.routes.analysis import analysis
            print(f"  ✅ Analysis blueprint imported successfully")
            print(f"  ✅ Blueprint name: {analysis.name}")
            print(f"  ✅ Blueprint url_prefix: {analysis.url_prefix}")
        except Exception as e:
            print(f"  ❌ Analysis blueprint import failed: {e}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
