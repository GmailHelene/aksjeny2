#!/usr/bin/env python3
"""
Route analysis script to understand URL mapping and potential conflicts
"""

import sys
import os

# Add the app directory to the path so we can import it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def analyze_routes():
    """Analyze the Flask application routes"""
    try:
        # Import Flask app
        from app import create_app
        
        print("🔍 Creating Flask application...")
        app = create_app()
        
        print("📋 Analyzing registered routes...")
        print("=" * 60)
        
        # Get all registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': rule.rule
            })
        
        # Sort routes by rule for easier reading
        routes.sort(key=lambda x: x['rule'])
        
        # Filter for our problematic endpoints
        problematic_patterns = [
            'watchlist',
            'profile', 
            'sentiment',
            'warren-buffett',
            'advanced-analysis',
            'alerts',
            'portfolio.*add'
        ]
        
        print("🎯 Routes matching our problematic patterns:")
        print("-" * 60)
        
        found_routes = []
        for route in routes:
            rule = route['rule']
            endpoint = route['endpoint']
            
            for pattern in problematic_patterns:
                if pattern in rule.lower() or pattern in endpoint.lower():
                    found_routes.append(route)
                    methods_str = ', '.join([m for m in route['methods'] if m not in ['OPTIONS', 'HEAD']])
                    print(f"  {rule:40} -> {endpoint:30} [{methods_str}]")
                    break
        
        print(f"\n📊 Found {len(found_routes)} potentially relevant routes")
        
        # Look specifically for advanced-analysis conflicts
        print("\n🔍 Advanced Analysis Route Analysis:")
        print("-" * 60)
        
        advanced_routes = []
        for route in routes:
            if 'advanced' in route['rule'].lower() and 'analysis' in route['rule'].lower():
                advanced_routes.append(route)
                methods_str = ', '.join([m for m in route['methods'] if m not in ['OPTIONS', 'HEAD']])
                print(f"  {route['rule']:40} -> {route['endpoint']:30} [{methods_str}]")
        
        if len(advanced_routes) > 1:
            print(f"⚠️  WARNING: Found {len(advanced_routes)} routes for advanced analysis - potential conflict!")
        elif len(advanced_routes) == 1:
            print(f"✅ Found exactly 1 advanced analysis route - no conflicts")
        else:
            print(f"❌ No advanced analysis routes found")
            
        # Check all routes to see the full picture
        print(f"\n📈 Total routes registered: {len(routes)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the correct directory and dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error analyzing routes: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🚀 Flask Route Analyzer")
    print("=" * 60)
    success = analyze_routes()
    sys.exit(0 if success else 1)
