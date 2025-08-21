#!/usr/bin/env python3
"""Test script to debug pro-tools route registration"""

import sys
import os
import traceback

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pro_tools_route():
    try:
        # Import Flask app
        from main import app
        
        with app.app_context():
            print("=== Flask Route Analysis ===")
            print(f"Flask app: {app}")
            
            # Check all routes containing 'pro-tools' or 'screener'
            pro_tools_routes = []
            all_routes = []
            
            for rule in app.url_map.iter_rules():
                all_routes.append(f"{rule.rule} - {rule.methods}")
                if 'pro-tools' in rule.rule or 'screener' in rule.rule:
                    pro_tools_routes.append(f"{rule.rule} - {rule.methods}")
            
            print(f"\nTotal routes registered: {len(all_routes)}")
            print(f"Pro-tools related routes: {len(pro_tools_routes)}")
            
            if pro_tools_routes:
                print("\n=== Pro-Tools Routes Found ===")
                for route in pro_tools_routes:
                    print(route)
            else:
                print("\n❌ No pro-tools routes found!")
                print("\nSearching for any routes containing 'pro':")
                for route in all_routes:
                    if 'pro' in route.lower():
                        print(route)
            
            # Test direct import of pro_tools blueprint
            print("\n=== Blueprint Import Test ===")
            try:
                from app.routes.pro_tools import pro_tools
                print(f"✅ Successfully imported pro_tools blueprint: {pro_tools}")
                print(f"Blueprint name: {pro_tools.name}")
                print(f"Blueprint url_prefix: {getattr(pro_tools, 'url_prefix', 'None')}")
                
                # Check blueprint routes
                blueprint_routes = []
                for rule in pro_tools.deferred_functions:
                    if hasattr(rule, 'rule'):
                        blueprint_routes.append(str(rule.rule))
                
                print(f"Blueprint routes: {blueprint_routes}")
                
            except ImportError as e:
                print(f"❌ Failed to import pro_tools blueprint: {e}")
                traceback.print_exc()
            
            # Test if the blueprint is actually registered
            print("\n=== Blueprint Registration Check ===")
            registered_blueprints = list(app.blueprints.keys())
            print(f"Registered blueprints: {registered_blueprints}")
            
            if 'pro_tools' in registered_blueprints:
                print("✅ pro_tools blueprint is registered")
                bp = app.blueprints['pro_tools']
                print(f"Blueprint URL prefix: {bp.url_prefix}")
            else:
                print("❌ pro_tools blueprint is NOT registered")
                
    except Exception as e:
        print(f"❌ Error during route testing: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_pro_tools_route()
