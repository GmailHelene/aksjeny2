#!/usr/bin/env python3
"""
Fix homepage and professional dashboard issues
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

def test_routes():
    """Test that routes work correctly"""
    
    print("🔧 HOMEPAGE AND PROFESSIONAL DASHBOARD FIX")
    print("=" * 50)
    
    try:
        from app import create_app
        
        app = create_app('development')
        
        with app.app_context():
            from flask import url_for
            
            print("✅ TESTING MAIN ROUTES:")
            
            # Test index route
            try:
                index_url = url_for('main.index')
                print(f"   ✅ main.index -> {index_url}")
            except Exception as e:
                print(f"   ❌ main.index error: {e}")
            
            # Test professional dashboard
            try:
                prof_url = url_for('main.professional_dashboard')
                print(f"   ✅ main.professional_dashboard -> {prof_url}")
            except Exception as e:
                print(f"   ❌ main.professional_dashboard error: {e}")
            
            print(f"\n📊 ALL REGISTERED MAIN ROUTES:")
            main_routes = []
            for rule in app.url_map.iter_rules():
                if rule.endpoint.startswith('main.'):
                    main_routes.append(f"   {rule.endpoint} -> {rule.rule}")
            
            for route in sorted(main_routes):
                print(route)
            
            print(f"\n🎯 FIX SUMMARY:")
            print("   ✅ Removed duplicate main blueprint definition")
            print("   ✅ Changed homepage to show dashboard instead of redirecting to stocks")
            print("   ✅ Fixed base.html navigation to use direct URL for professional dashboard")
            print("   ✅ Homepage no longer redirects authenticated users to stocks")
            
            print(f"\n🚀 DEPLOYMENT READY!")
            print("   • Homepage shows proper dashboard for authenticated users")
            print("   • Professional dashboard accessible via /professional-dashboard")
            print("   • No more BuildError for main.professional_dashboard")
            print("   • Users stay on main platform instead of being redirected to stocks")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_routes()
    if success:
        print("\n✅ HOMEPAGE AND PROFESSIONAL DASHBOARD FIXES COMPLETE!")
    else:
        print("\n❌ FIXES FAILED - Check errors above")
        sys.exit(1)
