#!/usr/bin/env python3
"""Test portfolio blueprint import and registration"""

import sys
import os
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Set up logging to see detailed errors
logging.basicConfig(level=logging.DEBUG)

try:
    print("Testing portfolio blueprint import...")
    
    from app import create_app
    app = create_app()
    
    with app.app_context():
        # Test direct portfolio import
        print("1. Testing direct portfolio import...")
        from app.routes.portfolio import portfolio
        print(f"   ✅ Portfolio blueprint imported: {portfolio}")
        print(f"   Blueprint name: {portfolio.name}")
        print(f"   URL prefix: {portfolio.url_prefix}")
        
        # Test routes in blueprint
        print("2. Testing blueprint routes...")
        for rule in app.url_map.iter_rules():
            if 'portfolio' in rule.endpoint:
                print(f"   Route: {rule.rule} -> {rule.endpoint}")
        
        # Test specific route access
        print("3. Testing route access...")
        with app.test_client() as client:
            # Test portfolio root
            response = client.get('/portfolio/')
            print(f"   /portfolio/ status: {response.status_code}")
            
            # Test portfolio overview
            response = client.get('/portfolio/overview')
            print(f"   /portfolio/overview status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"   Response data: {response.data[:500]}...")
        
        print("\n✅ Portfolio blueprint test completed successfully!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
