#!/usr/bin/env python3
"""
Test script to debug portfolio blueprint import
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_portfolio_import():
    print("=== PORTFOLIO BLUEPRINT IMPORT TEST ===")
    
    try:
        print("1. Testing app creation...")
        from app import create_app
        app = create_app('development')
        print("✅ App created successfully")
        
        print("2. Testing portfolio blueprint import...")
        from app.routes.portfolio import portfolio
        print(f"✅ Portfolio blueprint imported: {portfolio}")
        print(f"   Blueprint name: {portfolio.name}")
        print(f"   URL prefix: {portfolio.url_prefix}")
        
        print("3. Testing routes in portfolio blueprint...")
        for rule in portfolio.deferred_functions:
            print(f"   - Deferred function: {rule}")
            
        print("4. Testing with app context...")
        with app.app_context():
            # Check if portfolio is registered
            registered_blueprints = list(app.blueprints.keys())
            print(f"Registered blueprints: {registered_blueprints}")
            
            if 'portfolio' in registered_blueprints:
                print("✅ Portfolio blueprint is registered!")
                
                # Check portfolio routes
                portfolio_routes = [rule for rule in app.url_map.iter_rules() if rule.endpoint.startswith('portfolio.')]
                print(f"Portfolio routes found: {len(portfolio_routes)}")
                for route in portfolio_routes:
                    print(f"   - {route.endpoint} -> {route.rule}")
            else:
                print("❌ Portfolio blueprint is NOT registered!")
        
    except ImportError as e:
        print(f"❌ ImportError: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_portfolio_import()
