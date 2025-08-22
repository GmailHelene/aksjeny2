#!/usr/bin/env python3
"""
Simple Flask App Starter for Testing
"""

import os
import sys

def start_flask_app():
    """Start Flask app for testing"""
    print("🚀 STARTING FLASK APP FOR TESTING")
    print("=" * 50)
    
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        # Import and create the app
        from app import create_app
        
        print("✅ Successfully imported create_app")
        
        # Create app with development config
        app = create_app('development')
        print("✅ App created successfully")
        
        # Print some route info
        print(f"\n📍 Registered Routes ({len(list(app.url_map.iter_rules()))} total):")
        
        critical_routes = [
            '/achievements/api/update_stat',
            '/portfolio/watchlist',
            '/advanced/crypto-dashboard',
            '/analysis/screener',
            '/news-intelligence'
        ]
        
        found_routes = []
        for rule in app.url_map.iter_rules():
            if any(critical in str(rule) for critical in critical_routes):
                found_routes.append(str(rule))
        
        for route in found_routes[:10]:  # Show first 10 critical routes
            print(f"   ✅ {route}")
        
        if len(found_routes) > 10:
            print(f"   ... and {len(found_routes) - 10} more critical routes")
        
        print(f"\n🌐 Starting server on http://localhost:5000")
        print("   Press Ctrl+C to stop")
        
        # Start the app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    start_flask_app()
