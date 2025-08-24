#!/usr/bin/env python3
"""
Test script to verify Flask app routes after blueprint fixes
"""

def test_app_routes():
    try:
        from app import create_app
        
        print("Creating Flask app...")
        app = create_app()
        print("✅ App creation successful!")
        
        print("\n=== REGISTERED ROUTES ===")
        routes = []
        for rule in app.url_map.iter_rules():
            route_info = f"{rule.endpoint}: {rule.rule} [{' | '.join(sorted(rule.methods))}]"
            routes.append(route_info)
            print(route_info)
        
        print(f"\n📊 Total routes: {len(routes)}")
        
        # Check for specific problematic routes
        print("\n=== CHECKING PROBLEMATIC ENDPOINTS ===")
        problematic_endpoints = [
            '/watchlist/',
            '/profile',
            '/analysis/sentiment', 
            '/analysis/warren-buffett',
            '/advanced-analysis',
            '/pro-tools/alerts',
            '/portfolio/9/add'  # Fixed double prefix
        ]
        
        for endpoint in problematic_endpoints:
            # Find matching routes
            matches = [r for r in routes if endpoint in r]
            if matches:
                print(f"✅ {endpoint}: Found - {matches}")
            else:
                print(f"❌ {endpoint}: NOT FOUND")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_routes()
    exit(0 if success else 1)
